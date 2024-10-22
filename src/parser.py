from src.utils.py_utils.error import *
from src.utils.py_utils.operators import BINOP_OPERATOR_PRECEDENCE_DICT, CONDITION_OPERATOR_PRECEDENCE_DICT, SLICE_OPERATOR_PRECEDENCE_DICT, EXPR_MAP
from src.utils.py_utils.tokens import Token
from src.utils.py_utils.list_util_funcs import get_sublists, get_combinations
from src.utils.py_utils.allowed_type_constants import *
from src.nodes import *
from src.lexer import get_token_ident

class Parser():
    def __init__(self, tokens: list[Token], file_n: str) -> None:
        self.error = None
        self.tokens = tokens
        self.file_n = file_n
        self.func_identifier_dict = {}
        self.var_identifier_dict = {}
        self.indentation = None
        self.cur_block_indentation = None
        self.ast = AST()

    def make_ast(self) -> AST:
        if self.parse_block(self.tokens) == -1:
            return None
        return self.ast
    
    #################################General Parsing######################################
    
    def parse_block(self, tokens: list[Token]) -> None:
        line_tokens = self.get_line_tokens(tokens)
        i = 0
        while i < len(line_tokens):
            if line_tokens[i][0].token_t == "TT_eof": break
            i = self.parse_line(i, line_tokens[i], line_tokens[i+1:])
            if i == -1:
                return i
        self.cur_block_indentation = None
        return 0
    
    def parse_line(self, i: int, line: list[Token], rem_line_tokens: list[list[Token]]) -> int:
        if len(line) == 1 and line[0].token_t == "TT_eof":
            return i+1
        
        cur_line_indentation = self.get_indentation(line[0])
        if cur_line_indentation == -1: return -1
        line = line[1:] if cur_line_indentation != 0 else line

        if line[0].token_t == "TT_identifier" and line[1].token_t == "TT_equ":
            if self.parse_assign(line) == -1: return -1
            return i+1
        elif line[0].token_t == "TT_identifier" and line[1].token_t == "TT_lparen" and line[len(line)-2].token_t == "TT_rparen":
            if self.parse_func_call(line) == -1: return -1
            return i+1
        elif line[0].token_t in ("TT_if", "TT_elif", "TT_else"):
            line_count = self.parse_conditional_statement(line, rem_line_tokens, cur_line_indentation)
            if line_count == -1: return -1
            return i+line_count+1
        elif line[0].token_t == "TT_while":
            line_count = self.parse_while_loop(line, rem_line_tokens, cur_line_indentation)
            if line_count == -1: return -1
            return i+line_count+1
        elif line[0].token_t == "TT_for":
            line_count = self.parse_for_loop(line, rem_line_tokens, cur_line_indentation)
            if line_count == -1: return -1
            return i+line_count+1
        elif line[0].token_t == "TT_def":
            line_count = self.parse_func_def(line, rem_line_tokens, cur_line_indentation)
            if line_count == -1: return -1
            return i+line_count+1
        elif line[0].token_t == "TT_ret":
            if self.parse_return_statement(line) == -1: return -1
            return i+1
        
        self.error = SyntaxError("Invalid Syntax", line[0].ln, self.file_n)
        return -1
    
    ###########################Control Flow and Statement Parsing################################
    
    def parse_return_statement(self, line: list[Token]) -> int:
        cur_ln_num = line[0].ln
        line = line[1:]
        #Looks for FuncDefNode as parent node because then it would be in a function
        parent_node = self.ast.get_parent_node(FuncDefNode)
        if parent_node == -1:
            self.error = SyntaxError("Return Statement outside function!", cur_ln_num, self.file_n)
            return -1
        new_node_id = self.ast.append_node(ReturnNode())
        self.ast.traverse_node_by_id(new_node_id)
        return_type = self.parse_expression(line, "return_value", cur_ln_num, expr_4=False)
        if return_type == -1: return -1
        self.ast.cur_node.type = return_type
        parent_node.return_type = return_type
        parent_node.return_node = self.ast.cur_node
        self.ast.detraverse_node()
        return 0
    
    def parse_func_def(self, line: list[Token], rem_line_tokens: list[list[Token]], cur_line_indentation: int) -> int:
        cur_ln_num = line[0].ln
        #if second last character not a colon: error
        if line[len(line)-2].token_t != "TT_colon":
            self.error = SyntaxError("Expected colon", cur_ln_num, self.file_n)
            return -1
        line = line[1:len(line)-2]
        if line[0].token_t != "TT_identifier":
            self.error = SyntaxError("Expected identifier", cur_ln_num, self.file_n)
            return -1
        func_identifier, line = line[0].token_v, line[1:]
        if line[0].token_t != "TT_lparen" or line[len(line)-1].token_t != "TT_rparen":
            self.error = SyntaxError("Expected parenthesis", cur_ln_num, self.file_n)
            return -1
        line = line[1:len(line)-1]
        args = self.parse_func_def_args(line, cur_ln_num)
        if args == -1: return args
        new_node_id = self.ast.append_node(FuncDefNode(func_identifier, args))
        self.ast.traverse_node_by_id(new_node_id)
        self.func_identifier_dict[func_identifier] = self.ast.cur_node
        self.ast.cur_node.arg_names = args
        self.ast.cur_node.indentation = cur_line_indentation
        #children can not be parsed yet because argument types are still unknown
        children_count, self.ast.cur_node.unparsed_children = self.get_children(rem_line_tokens, cur_line_indentation)
        self.ast.detraverse_node()
        return children_count
    
    def parse_func_def_args(self, tokens: list[Token], cur_ln_num: int) -> list[str] | int:
        if not tokens: return []
        args = []
        cur_token = None
        for token in tokens:
            cur_token = token
            if token.token_t == "TT_identifier":
                args.append(token.token_v)
                continue
            if token.token_t == "TT_comma":
                continue
            self.error = SyntaxError("Invalid Syntax", cur_ln_num, self.file_n)
            return -1
        if cur_token.token_t == "TT_comma":
            self.error = SyntaxError("Expected argument", cur_ln_num, self.file_n)
            return -1
        return args

    def parse_for_loop(self, line: list[Token], rem_line_tokens: list[list[Token]], cur_line_indentation: int) -> int:
        cur_ln_num = line[0].ln
        if line[len(line)-2].token_t != "TT_colon":
            self.error = SyntaxError("Expected colon", cur_ln_num, self.file_n)
            return -1
        line = line[1:len(line)-2]
        if line[0].token_t != "TT_identifier":
            self.error = SyntaxError("Expected identifier", cur_ln_num, self.file_n)
            return -1
        if line[1].token_t != "TT_in":
            self.error = SyntaxError("Invalid Syntax", line[0].ln, self.file_n)
            return -1
        iter_var_name = line[0].token_v
        new_node_id = self.ast.append_node(ForLoopNode(iter_var_name))
        line = line[2:]
        self.ast.traverse_node_by_id(new_node_id)
        expr_type = self.parse_expression(line, "iter", cur_ln_num, expr_2=False, expr_4=False, expr_6=False, expr_7=False, expr_8=False)
        if expr_type == -1: return -1
        if not self.is_valid_type(expr_type, ("str", "list")): 
            self.error = TypeError("Conditional Expressions must be of type bool!", cur_ln_num, self.file_n)
            return -1
        self.ast.append_node(AssignNode(iter_var_name))
        parent_node = self.ast.get_parent_node(FuncDefNode)
        if parent_node == -1:
            self.var_identifier_dict[iter_var_name] = self.ast.cur_node.children[0]
        else:
            parent_node.var_identifier_dict[iter_var_name] = self.ast.cur_node.children[0]
        self.ast.cur_node.children[0].type = self.get_array_types()
        child_count = self.parse_children(cur_line_indentation, rem_line_tokens)
        self.ast.detraverse_node()
        return child_count

    def parse_while_loop(self, line: list[Token], rem_line_tokens: list[list[Token]], cur_line_indentation: int) -> int:
        cur_ln_num = line[0].ln
        if line[len(line)-2].token_t != "TT_colon":
            self.error = SyntaxError("Expected colon", line[0].ln, self.file_n)
            return -1
        line = line[1:len(line)-2]
        new_node_id = self.ast.append_node(WhileLoopNode())
        self.ast.traverse_node_by_id(new_node_id)
        if self.parse_expression(line, "condition",cur_ln_num,  expr_4=False) != "bool":
            self.error = TypeError("Conditional Expression must be of type bool!", cur_ln_num, self.file_n)
            return -1
        child_count = self.parse_children(cur_line_indentation, rem_line_tokens)
        self.ast.detraverse_node()
        return child_count
        
    def parse_conditional_statement(self, line: list[Token], rem_line_tokens: list[list[Token]], cur_line_indentation: int) -> int:
        cur_ln_num = line[0].ln
        match line[0].token_t:
            case "TT_if": kw_node = IfNode()
            case "TT_elif": kw_node = ElifNode()
            case "TT_else": kw_node = ElseNode()
        new_node_id = self.ast.append_node(kw_node)
        self.ast.traverse_node_by_id(new_node_id)
        if line[0].token_t in ("TT_elif", "TT_else"):
            if self.get_prev_conditional_nodes(self.ast.cur_node) == -1: 
                self.error = SyntaxError("Expected conditional statement before 'else/elif'", line[0].ln, self.file_n)
                return -1
        if line[len(line)-2].token_t != "TT_colon":
            self.error = SyntaxError("Expected colon at end of conditional statement", line[0].ln, self.file_n)
            return -1, -1
        line = line[1:len(line)-2]
        if self.parse_expression(line, "condition", cur_ln_num, expr_4=False) == -1: return -1
        child_count = self.parse_children(cur_line_indentation, rem_line_tokens)
        self.ast.detraverse_node()
        return child_count

    def parse_children(self, parent_line_indentation: int, child_line_tokens: list[list[Token]] = None, block_to_parse: list[list[Token]] = None) -> int:
        if block_to_parse:
            children_count = len(block_to_parse)
        else: 
            children_count, block_to_parse = self.get_children(child_line_tokens, parent_line_indentation)
        block_to_parse = [token for line in block_to_parse for token in line]
        old_cur_block_indentation = self.cur_block_indentation
        self.cur_block_indentation = None
        if self.parse_block(block_to_parse) == -1: return -1
        self.cur_block_indentation = old_cur_block_indentation
        return children_count

    def get_prev_conditional_nodes(self, new_node: ASTNode) -> None:
        prev_cond_nodes = []
        while True:
            self.ast.prev_child_node()
            if prev_cond_nodes and self.ast.cur_node == prev_cond_nodes[-1]:
                break
            if not isinstance(self.ast.cur_node, (IfNode, ElifNode)):
                break
            prev_cond_nodes.append(self.ast.cur_node)
        if prev_cond_nodes == []:
            return -1
        self.ast.cur_node = new_node
        for node in prev_cond_nodes:
            self.ast.append_node(node, "prev_conditions")
        return 0

    def parse_func_call(self, line: list[Token], traversal_type: str="children", from_expr: bool = False) -> int:
        cur_ln_num = line[0].ln
        name = line[0].token_v
        if not from_expr:
            line = line[2:len(line)-2]
        else:
            line = line[2:len(line)-1]
        arg_exprs = self.parse_func_call_args(line)
        if isinstance(arg_exprs, int):
           return self.handle_arg_parsing_error(arg_exprs, cur_ln_num)
        new_node_id = self.ast.append_node(FuncCallNode(name), traversal_type)
        self.ast.traverse_node_by_id(new_node_id, traversal_type)
        new_node = self.ast.cur_node
        arg_types = []
        for arg_expr in arg_exprs:
            arg_type = self.parse_expression(arg_expr, "args", cur_ln_num, expr_4=False)
            if arg_type == -1: return -1
            arg_types.append(arg_type)
        if name not in self.func_identifier_dict.keys():
            self.error = NameError(f"Call to undefined function {name}()", cur_ln_num, self.file_n) 
            return -1
        last_func_def_node = self.func_identifier_dict[name]
        if len(arg_exprs) != len(last_func_def_node.arg_names):
            self.error = TypeError(f"{name}() takes {len(self.ast.cur_node.arg_names)} arguments but {len(arg_exprs)} were given!", cur_ln_num, self.file_n)
            return -1
        if last_func_def_node.func_call_nodes:
            last_func_def_node.func_call_nodes.append(new_node)
        else:
            last_func_def_node.func_call_nodes = [new_node]
        if not last_func_def_node.children:
            self.parse_func_def_children(arg_types, last_func_def_node, new_node)
        else:
            if arg_types != last_func_def_node.arg_types:
                self.error = TypeError("Invalidly typed function arguments", cur_ln_num, self.file_n)
                return -1
        self.ast.detraverse_node()
        return 0
    
    def handle_arg_parsing_error(self, error_code: int, cur_ln_num: int) -> int:
        match error_code:
            case -1: 
                    self.error = SyntaxError("'(' was never closed", cur_ln_num, self.file_n)
            case -2:
                    self.error = SyntaxError("'[' was never closed", cur_ln_num, self.file_n)
            case -3:
                    self.error = SyntaxError("Invalid Syntax", cur_ln_num, self.file_n)
        return -1

    def parse_func_def_children(self, arg_types: list[str], last_func_def_node: FuncDefNode, new_node: FuncCallNode) -> None:
        self.ast.cur_node = last_func_def_node
        self.ast.cur_node.arg_types = arg_types
        block_to_parse = self.ast.cur_node.unparsed_children
        for i in range(len(arg_types)):
            self.ast.append_node(AssignNode(self.ast.cur_node.arg_names[i]))
            self.ast.cur_node.var_identifier_dict[self.ast.cur_node.arg_names[i]] = self.ast.cur_node.children[i]
            self.ast.cur_node.children[i].type = arg_types[i]
        if self.parse_children(self.ast.cur_node.indentation, block_to_parse=block_to_parse) == -1: return -1
        self.ast.cur_node = new_node
    
    def parse_func_call_args(self, tokens: list[Token]) -> list[list[Token]]:
        if not tokens: return []
        arg_exprs = []
        cur_arg_expr = []
        paren_depth = 0
        bracket_depth = 0
        for token in tokens:
            if token.token_t in ("TT_lparen", "TT_rparen", "TT_lbracket", "TT_rbracket"):
                match token.token_t:
                    case "TT_lparen":
                        paren_depth += 1
                    case "TT_rparen":
                        if paren_depth == 0: return -1
                        paren_depth -= 1
                    case "TT_lbracket":
                        bracket_depth += 1
                    case "TT_rbracket":
                        if bracket_depth == 0: return -2
                        bracket_depth -= 1
                cur_arg_expr.append(token)
                continue
            if token.token_t == "TT_dquote" or token.token_t == "TT_squote":
                continue
            elif token.token_t == "TT_comma" and not paren_depth and not bracket_depth:
                arg_exprs.append(cur_arg_expr)
                cur_arg_expr = []
            else:
                cur_arg_expr.append(token)
        if cur_arg_expr == []:
            return -3
        arg_exprs.append(cur_arg_expr)
        return arg_exprs
    
    def parse_assign(self, line: list[Token]) -> int:
        cur_ln_num = line[0].ln
        line = line[:len(line)-1]
        new_node_id = self.ast.append_node(AssignNode(line[0].token_v))
        self.ast.traverse_node_by_id(new_node_id)
        var_type = self.parse_expression(line[2:], "value", cur_ln_num, expr_4 = False)
        if var_type == -1:
            return -1
        if self.is_valid_type(var_type, ("list",)):
            self.ast.traverse_node("value")
            self.ast.cur_node.children_types = self.get_array_types()
            print(self.ast.cur_node.children_types)
            if self.ast.cur_node.children_types == -1:
                return -1
            self.ast.detraverse_node()
            self.ast.cur_node.type = ("list",)
        self.ast.cur_node.type = var_type
        cur_var_identifier_dict = self.get_cur_scope_var_dict()
        cur_var_identifier_dict[line[0].token_v] = self.ast.cur_node
        self.ast.detraverse_node()
        return 0
    
    #################################Expression Parsing###############################

    def parse_expression(self, tokens: list[Token], traversal_type: str, ln_num: int, **kwargs: bool) -> str | int:
        tokens = [token for token in tokens if token.token_t != "TT_eol"]
        if not tokens:
            self.error = SyntaxError("Invalid Expression", ln_num, self.file_n)
            return -1
        cur_expr_map = EXPR_MAP.copy()
        for kw in kwargs.keys():
            kw_int = int(kw[-1])
            if kw_int not in EXPR_MAP:
                raise Exception("Invalid Argument for function 'parse_expression': Argument must be in scope of EXPR_MAP!")
            cur_expr_map[kw_int] = False
        if cur_expr_map[0] and len(tokens) == 1:
            return self.parse_simple_literal_and_var(tokens[0], traversal_type)
        if cur_expr_map[1] and self.is_array_literal(tokens):
            return self.parse_array_literal(tokens, traversal_type)
        if len(tokens) >= 3 and cur_expr_map[3] and tokens[0].token_t == "TT_identifier" and tokens[1].token_t == "TT_lbracket" and tokens[len(tokens)-1].token_t == "TT_rbracket" and self.is_array_literal(tokens):
            return self.parse_array_var(tokens, traversal_type)
        if len(tokens) >= 3 and cur_expr_map[5] and tokens[0].token_t == "TT_identifier" and tokens[1].token_t == "TT_lparen" and tokens[len(tokens)-1].token_t == "TT_rparen":
            if self.parse_func_call(tokens, traversal_type, from_expr=True) == -1: return -1
            return self.func_identifier_dict[tokens[0].token_v].return_type
        if cur_expr_map[6] and tokens[0].token_t in ("TT_sub", "TT_not"):
            return self.parse_un_op_expression(tokens, traversal_type)
        for i, token in enumerate(tokens):
            if i == 0 or i == len(tokens)-1:
                continue
            if cur_expr_map[8] and token.token_t in ("TT_equ", "TT_less", "TT_greater", "TT_and", "TT_or", "TT_dequ", "TT_gequ", "TT_lequ") or (token.token_t in ("TT_equ", "TT_less", "TT_greater") and tokens[i+1] == "TT_equ"):
                return self.parse_conditional_expression(tokens, traversal_type)
            if cur_expr_map[7] and token.token_t in ("TT_sub", "TT_plus", "TT_mul", "TT_div") and not [token for token in tokens if token.token_t in ("TT_equ", "TT_greater", "TT_less")]:
                return self.parse_binop_expression(tokens, traversal_type)
        if cur_expr_map[4] and [token for token in tokens if token.token_t == "TT_colon"]:
            return self.parse_slice_expression(tokens, traversal_type, ln_num)
        self.error = SyntaxError("Invalid Expression", ln_num, self.file_n)
        return -1

    def parse_slice_expression(self, tokens: list[Token], traversal_type: str, ln_num: int) -> str | int:
        if len(tokens) == 1:
            self.error = SyntaxError("Invalid syntax", tokens[0].token_t, self.file_n)
            return -1
        operator, operator_idx = self.get_operator_info(tokens, SLICE_OPERATOR_PRECEDENCE_DICT, is_slice_expr = True)
        if operator == -1: return -1
        new_node_id = self.ast.append_node(SliceExpressionNode(), traversal_type)
        self.ast.traverse_node_by_id(new_node_id, traversal_type)
        if operator_idx == len(tokens)-1 or operator_idx == 0:
            if operator_idx == 0:
                tokens_to_parse = tokens[1:]
                traversal_type = "right"
            else:
                tokens_to_parse = tokens[:len(tokens)-1]
                traversal_type = "left"
            expr_type = self.parse_expression(tokens_to_parse, traversal_type, ln_num)
        else:
            left = tokens[:operator_idx]
            right = tokens[operator_idx+1:]
            expr_type = self.parse_sides(left, right, SLICE_EXPRESSION_ALLOWED_TYPES, ":")
        if expr_type == -1: return -1
        if not self.is_valid_type(expr_type, SLICE_EXPRESSION_ALLOWED_TYPES):
            self.error = TypeError(f"Invalid type for slice expression: '{expr_type}'", tokens[0].token_t, self.file_n)
            return -1
        self.ast.detraverse_node()
        return expr_type

    def parse_conditional_expression(self, tokens: list[Token], traversal_type: str) -> str | int:
        if not [token for token in tokens if token.token_t in ("TT_dequ", "TT_gequ", "TT_jequ")]:
            tokens = self.merge_equ(tokens)
        operator, operator_idx = self.get_operator_info(tokens, CONDITION_OPERATOR_PRECEDENCE_DICT)
        if operator == -1: return -1
        operator_str = get_token_ident(operator.token_t)
        left = tokens[:operator_idx]
        right = tokens[operator_idx+1:]
        self.ast.append_node(ConditionExpressionNode(operator_str), traversal_type)
        self.ast.traverse_node(traversal_type)
        if operator.token_t in ("TT_and", "TT_or"):
            allowed_types = CONDITIONAL_EXPRESSION_LOGICAL_OPERATOR_ALLOWED_TYPES
        else:
            allowed_types = CONDITIONAL_EXPRESSION_CONDTIONAL_OPERATOR_AllOWED_TYPES
            if operator_str == "==":
                allowed_types += CONDITIONAL_EXPRESSION_DEQU_ALLOWED_TYPES
        expr_type = self.parse_sides(left, right, tokens[0].ln, allowed_types, operator_str)
        if expr_type == -1: return -1
        self.ast.cur_node.type = expr_type
        self.ast.detraverse_node()
        return expr_type
        
    def parse_binop_expression(self, tokens: list[Token], traversal_type: str) -> str | int:
        if tokens[0].token_t == "TT_lparen" and tokens[-1].token_t == "TT_rparen":
            tokens = tokens[1:-1]
        operator, operator_index = self.get_operator_info(tokens, BINOP_OPERATOR_PRECEDENCE_DICT)
        if operator == -1: return -1
        allowed_types = BINOP_EXPRESSION_BASE_ALLOWED_TYPES
        if operator.token_t == "TT_plus":
            allowed_types += BINOP_EXPRESSION_PLUS_ALLOWED_TYPES
        if operator.token_t in ("TT_mul"):
            allowed_types += BINOP_EXPRESSION_MUL_ALLOWED_TYPES
        left = tokens[:operator_index]
        right = tokens[operator_index+1:]
        self.ast.append_node(BinOpNode(get_token_ident(operator.token_t)), traversal_type)
        self.ast.traverse_node(traversal_type)
        expr_type = self.parse_sides(left, right, tokens[0].ln, allowed_types, get_token_ident(operator.token_t))
        if expr_type == -1: return -1    
        self.ast.cur_node.type = expr_type
        self.ast.detraverse_node()
        return expr_type
    
    def get_operator_info(self, tokens: list[Token], operator_precedence_dict: dict[str: int], is_slice_expr: bool = False) -> tuple[str | int, int]:
        operator_precedence = operator_precedence_dict
        best_operator = None
        paren_depth = 0
        bracket_depth = 0
        for i, token in enumerate(tokens):
            if token.token_t in ("TT_lparen", "TT_lbracket", "TT_rparen", "TT_rbracket"):
                match token.token_t:
                    case "TT_lparen":
                        paren_depth += 1
                    case "TT_lbracket":
                        bracket_depth += 1
                    case "TT_rparen":
                        paren_depth -= 1
                    case "TT_rbracket":
                        bracket_depth -= 1
                continue
            if paren_depth or bracket_depth or token.token_t not in operator_precedence.keys():
                continue
            if i == 0 or i == len(tokens)-1 and not is_slice_expr:
                self.error = SyntaxError("Invalid Syntax", tokens[0].ln, self.file_n)
                return -1, -1
            if operator_precedence[token.token_t] == 2:
                if not best_operator:
                    best_operator = token
                    continue
            best_operator = token
            break
        if not best_operator or paren_depth or bracket_depth:
            self.error = SyntaxError("Invalid Syntax", tokens[0].ln, self.file_n)
            return -1, -1
        return best_operator, tokens.index(best_operator)
    
    def parse_sides(self, left: list[Token], right: list[Token], ln_num: int, allowed_types: list[tuple[str, str]], operator: str) -> str | int:
        left_expr_type = self.parse_expression(left, "left", ln_num, expr_4=False)
        if left_expr_type == -1: return -1
        right_expr_type = self.parse_expression(right, "right", ln_num, expr_4=False)
        if right_expr_type == -1: return -1
        expr_type = self.resolve_types(left_expr_type, right_expr_type, operator, ln_num)
        if expr_type == -1: return -1
        if not self.is_valid_type(expr_type, allowed_types):
            self.error = TypeError("Invalid Expression type", ln_num, self.file_n)
            return -1
        return expr_type

    def parse_un_op_expression(self, tokens: list[Token], traversal_type) -> str | int:
        operator = "-" if tokens[0].token_t == "TT_min" else "not"
        self.ast.append_node(UnOpNode(operator))
        self.ast.traverse_node(traversal_type)
        expr_type = self.parse_expression(tokens[1:], "right", tokens[0].ln, expr_1=False, expr_3=False, expr_4=False, expr_6=False)
        if operator == "-" and not self.is_valid_type(expr_type, ("int", "float")):
            self.error = TypeError(f"Bad type for unary operator '-': {expr_type}", tokens[0].ln, self.file_n)
            return -1
        if operator == "not" and not self.is_valid_type(expr_type, ("bool")):
            self.error = TypeError(f"Bad type for unary operator 'not': {expr_type}", tokens[0].ln, self.file_n)
            return -1
        self.ast.detraverse_node()
        return expr_type
        
    def parse_array_var(self, tokens: list[Token], traversal_type: str) -> str | int:
        cur_ln_num = tokens[0].ln
        var_identifier = tokens[0].token_v
        cur_var_identifier_dict = self.get_cur_scope_var_dict()
        if var_identifier not in cur_var_identifier_dict:
            self.error = NameError(f"Name {var_identifier} is not defined", cur_ln_num, self.file_n)
            return -1
        var_dec_node = cur_var_identifier_dict[var_identifier]
        if not self.is_valid_type(var_dec_node.type, ("str", "list")):
            self.error = TypeError(f"{var_dec_node.type} object is not subscriptable", cur_ln_num, self.file_n)
            return -1
        tokens = tokens[2:len(tokens)-1]
        if not tokens:
            self.error = SyntaxError("Invalid Syntax", cur_ln_num, self.file_n)
            return -1
        node_id = self.ast.append_node(ArrayVarNode(var_identifier), traversal_type)
        self.ast.traverse_node_by_id(node_id, traversal_type)
        expr_type = self.parse_expression(tokens, "content", cur_ln_num, expr_1=False, expr_3=False, expr_8=False)
        if expr_type == -1: return -1
        if not self.is_valid_type(expr_type, ("int",)):
            self.error = TypeError(f"list indices must be of type int, not {expr_type}", cur_ln_num, self.file_n)
            return -1
        var_types  = self.get_array_types()
        self.ast.detraverse_node()
        return var_types
        
    def parse_array_literal(self, tokens: list[Token], traversal_type: str) -> str | int:
        tokens = tokens[1:len(tokens)-1]
        if tokens == []:
            self.ast.append_node(ArrayNode(), traversal_type)
            return ("list",)
        arr_element_expressions = []
        cur_arr_element_expression = []
        paren_depth = 0
        for token in tokens:
            if token.token_t in ("TT_lparen", "TT_lbracket"):
                paren_depth += 1
            if token.token_t in ("TT_rparen", "TT_rbracket"):
                if paren_depth == 0:
                    self.error = SyntaxError("Invalid Syntax", tokens[0].token_t, self.file_n)
                    return -1
                paren_depth -= 1
            if token.token_t == "TT_comma" and not paren_depth:
                if cur_arr_element_expression:
                    arr_element_expressions.append(cur_arr_element_expression)
                    cur_arr_element_expression = []
                    continue
                else:
                    self.error = SyntaxError("Invalid Syntax", token.ln, self.file_n)
                    return -1
            cur_arr_element_expression.append(token)
        if not cur_arr_element_expression:
            self.error = SyntaxError("Invalid Syntax", token.ln, self.file_n)
            return -1
        arr_element_expressions.append(cur_arr_element_expression)
        node_id = self.ast.append_node(ArrayNode(), traversal_type)
        self.ast.traverse_node_by_id(node_id, traversal_type)
        for arr_element_expression in arr_element_expressions:
            if self.parse_expression(arr_element_expression, "children", tokens[0].ln, expr_4=False) == -1: return -1
        self.ast.detraverse_node()
        return ("list",)
        
    def parse_simple_literal_and_var(self, token: Token, traversal_type: str) -> str | int:
        if token.token_t in ("TT_int", "TT_float"):
            new_node_id = self.ast.append_node(NumberNode(token.token_v), traversal_type)
            self.ast.traverse_node_by_id(new_node_id, traversal_type)
            self.ast.cur_node.type = token.token_t[3:]
            self.ast.detraverse_node()
            return (token.token_t[3:],)
        if token.token_t == "TT_bool":
            self.ast.append_node(BoolNode(token.token_v), traversal_type)
            return ("bool",)
        if token.token_t == "TT_str":
            self.ast.append_node(StringNode(token.token_v), traversal_type)
            return ("str",)
        if token.token_t == "TT_identifier":
            cur_var_identifier_dict = self.get_cur_scope_var_dict()
            if token.token_v not in cur_var_identifier_dict.keys():
                self.error = NameError(f"Unknown Identifier: '{token.token_v}'", token.ln, self.file_n)
                return -1
            new_node_id = self.ast.append_node(VarNode(token.token_v), traversal_type)
            self.ast.traverse_node_by_id(new_node_id, traversal_type)
            cur_node_type = cur_var_identifier_dict[token.token_v].type
            self.ast.cur_node.type = cur_node_type
            self.ast.detraverse_node()
            return cur_node_type
            
        self.error = SyntaxError("Invalid Literal", token.ln, self.file_n)
        return -1
    
    ########################################Misc########################################

    def get_cur_scope_var_dict(self) -> dict:
        parent_func_def_node = self.ast.get_parent_node(FuncDefNode)
        if parent_func_def_node == -1:
            return self.var_identifier_dict
        else:
            return parent_func_def_node.var_identifier_dict
    
    def resolve_types(self, left_expr_type: tuple[str], right_expr_type: tuple[str], operator: str, ln_num: int) -> tuple[str]:
        types = []
        if left_expr_type == right_expr_type:
            if operator in ("==" or "!="):
                return ("bool",)
            return left_expr_type if isinstance(left_expr_type, tuple) else (left_expr_type,)
        if len(left_expr_type) == len(right_expr_type) and len(left_expr_type) == 1:
            expr_type = (left_expr_type[0], right_expr_type[0])
            if operator == "==":
                return ("bool",)
            if self.is_valid_type(expr_type, ("int", "str")):
                if operator == "*": return ("str",)
                self.error = TypeError("Invalid combination of types 'int', 'str'", ln_num, self.file_n)
                return -1
            if self.is_valid_type(expr_type, ("float", "int")): 
                return ("float")
            self.error = TypeError(f"Invalid combination of types: '{expr_type[0]}', '{expr_type[1]}'", ln_num, self.file_n)
            return -1
        combinations = get_combinations(left_expr_type, right_expr_type)
        for combination in combinations:
            combination_type = self.resolve_types((combination[0],), (combination[1],), operator, ln_num)
            if combination_type == -1: return -1
            types += list(combination_type)
        return tuple(set(types))

    def is_valid_type(self, t1: tuple[str], t2: tuple[str]) -> bool:
        if len(t1) > len(t2):
            return False
        if len(t1) > 1:
            t1 = tuple(sorted(t1))
        if len(t2) > 1:
            t2 = tuple(sorted(t2))
        if t1 not in get_sublists(t2):
            return False
        return True

    def is_array_literal(self, tokens: list[Token]) -> bool:
        if tokens[0].token_t != "TT_lbracket" or tokens[-1].token_t != "TT_rbracket":
            return False
        bracket_depth = 0
        for i, token in enumerate(tokens):
            match token.token_t:
                case "TT_lbracket":
                    bracket_depth += 1
                case "TT_rbracket":
                    if bracket_depth != 1 or i == len(tokens)-1:
                        bracket_depth -= 1
                    else:
                        return False
        return True
    
    def get_array_types(self) -> list[str]:
        cur_node = self.ast.cur_node
        array_nodes = self.get_iter_nodes()
        self.ast.cur_node = cur_node
        if array_nodes == -1: return -1
        if isinstance(array_nodes, tuple):
            return array_nodes
        types = []
        for array_node in array_nodes:
            if array_node.children:
                for child in array_node.children:
                    types.append(child.type)
        return tuple(types)
    
    def get_iter_nodes(self) -> list[ASTNode] | tuple[str]:
        if isinstance(self.ast.cur_node, ForLoopNode):
            if isinstance(self.ast.cur_node.iter, ArrayNode):
                return [self.ast.cur_node.iter]
            self.ast.traverse_node("iter")
            return self.get_iter_nodes()
        if isinstance(self.ast.cur_node, ArrayNode):
            return [self.ast.cur_node]
        if isinstance(self.ast.cur_node, AssignNode):
            if not self.ast.cur_node.value:
                parent_func_def_node = self.ast.get_parent_node(FuncDefNode)
                arg_index = parent_func_def_node.arg_names.index(self.ast.cur_node.name)
                self.ast.cur_node = parent_func_def_node.func_call_nodes[0].args[arg_index]
                return self.get_iter_nodes()
            return self.ast.cur_node.children_types if self.ast.cur_node.children_types else []
        if isinstance(self.ast.cur_node, VarNode):
            cur_var_identifier_dict = self.get_cur_scope_var_dict()
            self.ast.cur_node = cur_var_identifier_dict[self.ast.cur_node.name]
            return self.get_iter_nodes()
        if isinstance(self.ast.cur_node, BinOpNode):
            nodes = []
            cur_node = self.ast.cur_node
            self.ast.traverse_node("left")
            right_types = self.get_iter_nodes()
            if right_types == -1: return -1
            nodes += right_types
            self.ast.cur_node = cur_node
            self.ast.traverse_node("right")
            left_types = self.get_iter_nodes()
            if left_types == -1: return -1
            nodes += left_types
            self.ast.cur_node = cur_node
            return nodes
        if isinstance(self.ast.cur_node, FuncCallNode):
            self.ast.cur_node = self.func_identifier_dict[self.ast.cur_node.name]
            self.ast.traverse_node("return_node")
            self.ast.traverse_node("return_value")
            return self.get_iter_nodes()
        return []


    def merge_equ(self, tokens: list[Token]) -> list[Token]:
        tokens_merged_equ = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if i == len(tokens)-1:
                tokens_merged_equ.append(token)
                break
            next_token = tokens[i+1]
            if token.token_t not in ("TT_equ", "TT_greater", "TT_less"):
                tokens_merged_equ.append(token)
                i += 1
                continue
            if next_token.token_t != "TT_equ":
                tokens_merged_equ.append(token)
                i += 1
                continue
            if token.token_t == "TT_equ" and next_token.token_t == "TT_equ":
                token.token_t = "TT_dequ"
            elif token.token_t == "TT_greater" and next_token.token_t == "TT_equ":
                token.token_t = "TT_gequ"
            elif token.token_t == "TT_less" and next_token.token_t == "TT_equ":
                token.token_t == "TT_lequ"
            elif token.token_t == "TT_exclam":
                token.token_t == "TT_nequ"
            tokens_merged_equ.append(token)
            i += 2
        return tokens_merged_equ
    
    def get_children(self, child_line_tokens: list[Token], parent_line_indentation: int) -> int:
        if child_line_tokens == []:
            self.error = SyntaxError("Expected Block after statement", self.tokens[-1].ln-1, self.file_n)
            return -1
        cur_indentation = None
        block_to_parse = []
        for line in child_line_tokens:
            if line[0].token_t != "TT_pind":
                break
            pind_token = line[0]
            if not self.indentation:
                self.indentation = pind_token.token_v
            if not cur_indentation:
                if pind_token.token_v == parent_line_indentation + self.indentation:
                    cur_indentation = pind_token.token_v
                else:
                    self.error = IndentationError("Indent does not match previous Indents", pind_token.ln, self.file_n)
                    return -1
            if pind_token.token_v < cur_indentation:
                if pind_token.token_v % self.indentation == 0:
                    break
                self.error = IndentationError("Unindent does not match previous Indent", line[0].ln, self.file_n)
            block_to_parse.append(line)
        if block_to_parse == []:
            self.error = IndentationError("Expected Indent", line[0].ln, self.file_n)
            return -1
        children_count = len(block_to_parse)
        return children_count, block_to_parse
    
    def get_indentation(self, pind_token: Token) -> int:
        if pind_token.token_t != "TT_pind":
            return 0
        if not self.cur_block_indentation:
            self.cur_block_indentation = pind_token.token_v
        if pind_token.token_v != self.cur_block_indentation:
            self.error = IndentationError("Unexpected Indent", pind_token.ln, self.file_n)
            return -1
        return pind_token.token_v
    
    def get_line_tokens(self, tokens: list[Token]) -> list[list[Token]]:
        if not tokens: return [tokens]
        raw_line_tokens = []
        line_tokens = []
        for i in range(tokens[0].ln, tokens[len(tokens)-1].ln+1):
            raw_line_tokens.append([token for token in tokens if token.ln == i and token.token_t not in ("TT_squote", "TT_dquote")])
        for line in raw_line_tokens:
            if line[0].token_t != "TT_eol":
                line_tokens.append(line)

        return line_tokens