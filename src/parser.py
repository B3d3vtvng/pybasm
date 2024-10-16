from utils.py_utils.error import *
from utils.py_utils.operators import EXPR_OPERATORS, BIN_OP_OPERATORS, EXPR_MAP
from utils.py_utils.tokens import Token
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
        self.ast.detraverse_node()
        return 0
    
    def parse_func_def(self, line: list[Token], rem_line_tokens: list[list[Token]], cur_line_indentation: int) -> int:
        cur_ln_num = line[0].ln
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
        children_count, self.ast.cur_node.children = self.get_children(rem_line_tokens, cur_line_indentation)
        self.ast.detraverse_node()
        return children_count
    
    def parse_func_def_args(self, tokens: list[Token], cur_ln_num: int) -> list[str] | int:
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
            self.error = SyntaxError("Expected indentifier", cur_ln_num, self.file_n)
            return -1
        if line[1].token_t != "TT_in":
            self.error = SyntaxError("Invalid Syntax", line[0].ln, self.file_n)
            return -1
        new_node_id = self.ast.append_node(ForLoopNode(line[0].token_v))
        line = line[2:]
        self.ast.traverse_node_by_id(new_node_id)
        if self.parse_expression(line, "iter", cur_ln_num, expr_0=False, expr_2=False, expr_4=False, expr_6=False, expr_8=False, expr_9=False) != "bool": 
            self.error = TypeError("Conditional Expressions must be of type bool!", cur_ln_num, self.file_n)
            return -1
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
            if self.get_prev_conditional_nodes(new_node_id) == -1: 
                self.error = SyntaxError("Expected conditional statement before 'else/elif'", line[0].ln, self.file_n)
                return -1
        if line[len(line)-2].token_t != "TT_colon":
            self.error = SyntaxError("Expected colon at end of conditional statement", line[0].ln, self.file_n)
            return -1, -1
        line = line[1:len(line)-2]
        if self.parse_expression(line, "condition", cur_ln_num, expr_4=False) != "bool":
            self.error = TypeError("Conditional Expression must be of type bool", cur_ln_num, self.file_n)
            return -1
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

    def get_prev_conditional_nodes(self, new_node_id: int) -> None:
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
        self.ast.cur_node = self.ast.get_node_by_id(new_node_id)
        for node in prev_cond_nodes:
            self.ast.append_node(node, "prev_conditions")
        return 0

    def parse_func_call(self, line: list[Token], traversal_type: str="children") -> int:
        cur_ln_num = line[0].ln
        name = line[0].token_v
        line = line[2:len(line)-2]
        arg_exprs = self.parse_func_call_args(line)
        new_node_id = self.ast.append_node(FuncCallNode(name), traversal_type)
        self.ast.traverse_node_by_id(new_node_id)
        new_node = self.ast.cur_node
        arg_types = []
        for arg_expr in arg_exprs:
            arg_type = self.parse_expression(arg_expr, "args", cur_ln_num, expr_4=False)
            if arg_type == -1:
                return -1
            arg_types.append(arg_type)
        if name not in self.func_identifier_dict.keys():
            self.error = NameError(f"Call to undefined function {name}()", cur_ln_num, self.file_n) 
            return -1
        last_func_def_node = self.func_identifier_dict[name]
        if len(arg_exprs) != len(last_func_def_node.arg_names):
            self.error = TypeError(f"{name}() takes {len(self.ast.cur_node.arg_names)} arguments but {len(arg_exprs)} were given!", cur_ln_num, self.file_n)
            return -1
        if not isinstance(last_func_def_node.children[0], ASTNode):
            self.ast.cur_node = last_func_def_node
            self.ast.cur_node.arg_types = arg_types
            block_to_parse = self.ast.cur_node.children
            for i in range(len(arg_types)):
                self.ast.append_node(AssignNode(self.ast.cur_node.arg_names[i]))
                self.ast.cur_node.children[i].type = arg_types[i]
            if self.parse_children(self.ast.cur_node.indentation, block_to_parse=block_to_parse) == -1: return -1
            self.ast.cur_node = new_node
        else:
            if arg_types != last_func_def_node.arg_types:
                self.error = TypeError("Invalidly typed function arguments", cur_ln_num, self.file_n)
                return -1
        last_func_def_node.func_call_nodes.append(new_node)
        self.ast.detraverse_node()
        return 0
    
    def parse_func_call_args(self, tokens: list[Token]) -> list[list[Token]]:
        arg_exprs = []
        cur_arg_expr = []
        for token in tokens:
            if token.token_t == "TT_dquote" or token.token_t == "TT_squote":
                continue
            elif token.token_t == "TT_comma":
                arg_exprs.append(cur_arg_expr)
                cur_arg_expr = []
            else:
                cur_arg_expr.append(token)
        if cur_arg_expr == []:
            return -1
        arg_exprs.append(cur_arg_expr)
        return arg_exprs
    
    def parse_assign(self, line: list[Token]) -> int:
        new_node_id = self.ast.append_node(AssignNode(line[0].token_v))
        self.ast.traverse_node_by_id(new_node_id)
        var_type = self.parse_expression(line[2:], "value", line[0].ln, expr_4 = False)
        if var_type == -1:
            return -1
        self.ast.cur_node.type = var_type
        self.var_identifier_dict[line[0].token_v] = self.ast.cur_node
        self.ast.detraverse_node()
        return 0
    
    #################################Expression Parsing###############################

    def parse_expression(self, tokens: list[Token], traversal_type: str, ln_num: int, **kwargs: bool) -> str | int:
        if not tokens:
            self.error = SyntaxError("Invalid Expression", ln_num, self.file_n)
            return -1
        cur_expr_map = EXPR_MAP
        for kw in kwargs.keys():
            kw_int = int(kw[-1])
            if kw_int not in EXPR_MAP:
                raise Exception("Invalid Argument for function 'parse_expression': Argument must be in scope of EXPR_MAP!")
            cur_expr_map[kw_int] = False
        if cur_expr_map[0] and len(tokens) == 1:
            return self.parse_simple_literal_and_var(tokens[0], traversal_type)
        if tokens[0].token_t == "TT_lbracket" and tokens[len(tokens)-1].token_t == "TT_rbracket":
            return self.parse_array_literal(tokens, traversal_type)
        if tokens[0].token_t == "TT_identifier" and tokens[1].token_t == "TT_lbracket" and tokens[len(tokens)-1].token_t == "TT_rbracket":
            return self.parse_array_var(tokens, traversal_type)
        if tokens[0].token_t == "TT_identifier" and tokens[1].token_t == "TT_lparen" and tokens[len(tokens)-1].token_t == "TT_rparen":
            if self.parse_func_call(tokens, traversal_type) == -1: return -1
            return self.func_identifier_dict[tokens[0].token_t].return_type
        if tokens[0].token_t in ("TT_sub", "TT_not"):
            return self.parse_un_op_expression(tokens, traversal_type)
        for i, token in enumerate(tokens):
            if i == 0 or i == len(tokens)-1:
                continue
            if token.token_t in ("TT_sub", "TT_plus", "TT_mul", "TT_div"):
                return self.parse_binop_expression(tokens, traversal_type)
            if token.token_t in ("TT_equ", "TT_less", "TT_greater") or (token.token_t in ("TT_equ", "TT_less", "TT_greater") and tokens[i+1] == "TT_equ"):
                return self.parse_conditional_expression(tokens, traversal_type)
            if token.token_t in ("TT_or", "TT_and"):
                return self.parse_logical_expression(tokens, traversal_type)
        if [token for token in tokens if token.token_t == "TT_colon"]:
            return self.parse_slice_expression(tokens, traversal_type)
        self.error = SyntaxError("Invalid Expression", ln_num, self.file_n)
        return -1
    
    def parse_conditional_expression()
        
    def parse_binop_expression(self, tokens: list[Token], traversal_type: str) -> str:
        operator, operator_index = self.get_operator_info(tokens)
        if operator == -1: return -1
        allowed_types = [("int", "int")]
        if operator.token_t == "TT_plus":
            allowed_types.append(("str", "str"))
            allowed_types.append(("list", "list"))
        if operator.token_t in ("TT_mul"):
            allowed_types.append(("str", "int"), ("int", "str"))
        left = tokens[:operator_index]
        right = tokens[operator_index+1:]
        new_node_id = self.ast.append_node(BinOpNode(get_token_ident(operator.token_v)))
        self.ast.traverse_node_by_id(new_node_id, traversal_type)
        expr_type = self.parse_sides(left, right, tokens[0].ln, allowed_types=allowed_types)
        if expr_type == -1: return -1
        self.ast.cur_node.type = expr_type
        self.ast.detraverse_node()
        return expr_type
    
    def get_operator_info(self, tokens: list[Token]) -> tuple[str, int] | int:
        if tokens[0].token_t == "TT_lparen" and tokens[len(tokens)-1].token_t == "TT_rparen":
            tokens = tokens[1:len(tokens)-2]
        highest_priority_operator = None
        add_sub_operators = []
        parens = []
        for token in tokens:
            if token.token_t not in ("TT_plus", "TT_sub", "TT_mul", "TT_div", "TT_lparen", "TT_rparen"):
                continue
            if token.token_t == "TT_lparen":
                parens.append(True)
                continue
            if token.token_t == "TT_rparen":
                if parens:
                    parens = parens[:len(parens)-2] if len(parens) > 1 else []
                else:
                    self.error = SyntaxError("Invalid Syntax", tokens[0].ln, self.file_n)
                    return -1, -1
            if parens:
                continue
            if token.token_t in ("TT_mul", "TT_div"):
                highest_priority_operator = token
                break
        if parens:
            self.error = SyntaxError("Invalid Syntax", tokens[0].ln, self.file_n)
            return -1, -1
        operator_index = tokens.index(token)
        if operator_index == len(tokens)-1  or ( operator_index == 0 and highest_priority_operator.token_t in ("TT_mul", "TT_div")):
            self.error = SyntaxError("Invalid syntax", tokens[0].ln, self.file_n)
            return -1, -1
        if operator_index == 0:
            highest_priority_operator = add_sub_operators[1]
        return highest_priority_operator, operator_index
    
    def parse_sides(self, left: list[Token], right: list[Token], ln_num: int, allowed_types: list[tuple[str, str]]) -> str:
        left_expr_type = self.parse_expression(left, "left", ln_num, expr_4=False)
        right_expr_type = self.parse_expression(right, "right", ln_num, expr_4=False)
        expr_type = (left_expr_type, right_expr_type)
        if expr_type not in allowed_types:
            self.error = TypeError("Invalid expression type", left[0].ln, self.file_n)
            return -1
        if expr_type[0] == expr_type[1]:
            return expr_type[0]
        if "int" in expr_type and "str" in expr_type:
            return "str"
        raise Exception("Invalid args!!!")

    def parse_un_op_expression(self, tokens: list[Token], traversal_type) -> str:
        operator = "-" if tokens[0].token_t == "TT_min" else "not"
        new_node_id = self.ast.append_node(UnOpNode(operator))
        self.ast.traverse_node_by_id(new_node_id, traversal_type)
        expr_type = self.parse_expression(tokens[1:], "right", tokens[0].ln, expr_1=False, expr_3=False, expr_4=False, expr_6=False)
        if operator == "-" and expr_type not in ("int", "float"):
            self.error = TypeError(f"Bad type for unary operator '-': {expr_type}", tokens[0].ln, self.file_n)
            return -1
        if operator == "not" and expr_type != "bool":
            self.error = TypeError(f"Bad type for unary operator 'not': {expr_type}", tokens[0].ln, self.file_n)
            return -1
        self.ast.detraverse_node()
        return expr_type
        
    def parse_array_var(self, tokens: list[Token], traversal_type: str) -> str:
        cur_ln_num = tokens[0].ln
        var_identifier = tokens[0].token_v
        if var_identifier not in self.var_identifier_dict:
            self.error = NameError(f"Name {var_identifier} is not defined", cur_ln_num, self.file_n)
            return -1
        var_type = self.var_identifier_dict[var_identifier]
        if var_type not in ("str", "list"):
            self.error = TypeError(f"{var_type} object is not subscriptable", cur_ln_num, self.file_n)
            return -1
        tokens = tokens[2:len(tokens)-1]
        if not tokens:
            self.error = SyntaxError("Invalid Syntax", cur_ln_num, self.file_n)
            return -1
        node_id = self.ast.append_node(ArrayVarNode(var_identifier), traversal_type)
        self.ast.traverse_node_by_id(node_id, traversal_type)
        expr_type = self.parse_expression(tokens, "content", cur_ln_num, expr_1=False, expr_3=False, expr_4=False, expr_8=False, expr_9=False)
        if expr_type == -1: return -1
        if expr_type != "int":
            self.error = TypeError(f"list indices must be of type int, not {expr_type}", cur_ln_num, self.file_n)
            return -1
        self.ast.detraverse_node()
        return var_type
        
    def parse_array_literal(self, tokens: list[Token], traversal_type: str) -> str:
        tokens = tokens[1:len(tokens)-1]
        if tokens == []:
            self.ast.append_node(ArrayNode(), traversal_type)
            return 0
        arr_element_expressions = []
        cur_arr_element_expression = []
        for token in tokens:
            if token.token_t == "TT_comma":
                if cur_arr_element_expression:
                    arr_element_expressions.append(cur_arr_element_expression)
                    continue
                else:
                    self.error = SyntaxError("Invalid Syntax", token.ln, self.file_n)
                    return -1
            cur_arr_element_expression.append(token)
        if not cur_arr_element_expression:
            self.error = SyntaxError("Invalid Syntax", token.ln, self.file_n)
            return -1
        arr_element_expressions.append(cur_arr_element_expression)
        node_id = self.ast.append_node(ArrayNode())
        self.ast.traverse_node_by_id(node_id, traversal_type)
        for arr_element_expression in arr_element_expressions:
            if self.parse_expression(arr_element_expression, "children", tokens[0].ln, expr_4=False) == -1: return -1
        self.ast.detraverse_node()
        return "list"
        
    def parse_simple_literal_and_var(self, token: Token, traversal_type: str) -> str:
        if token.token_t in ("TT_int", "TT_float"):
            new_node_id = self.ast.append_node(NumberNode(token.token_v), traversal_type)
            self.ast.traverse_node_by_id(new_node_id, traversal_type)
            self.ast.cur_node.type = token.token_t[3:]
            self.ast.detraverse_node()
            return token.token_t[3:]
        if token.token_t == "TT_bool":
            self.ast.append_node(BoolNode(token.token_v), traversal_type)
            return "bool"
        if token.token_t == "TT_str":
            self.ast.append_node(StringNode(token.token_v), traversal_type)
            return "str"
        if token.token_t == "TT_identifier":
            if token.token_v not in self.var_identifier_dict.keys():
                self.error = NameError("Unknown Identifier", token.ln, self.file_n)
                return -1
            new_node_id = self.ast.append_node(VarNode(token.token_v), traversal_type)
            self.ast.traverse_node_by_id(new_node_id, traversal_type)
            cur_node_type = self.var_identifier_dict[token.token_v].type
            self.ast.cur_node.type = cur_node_type
            self.ast.detraverse_node()
            return cur_node_type
            
        self.error = SyntaxError("Invalid Literal", token.ln, self.file_n)
        return -1
    
    ########################################Misc########################################
        
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
        raw_line_tokens = []
        line_tokens = []
        for i in range(tokens[0].ln, tokens[len(tokens)-1].ln+1):
            raw_line_tokens.append([token for token in tokens if token.ln == i])
        for line in raw_line_tokens:
            if line[0].token_t != "TT_eol":
                line_tokens.append(line)

        return line_tokens