from src.utils.error import SyntaxError, IndentationError
from src.utils.operators import EXPR_OPERATORS, BIN_OP_OPERATORS, EXPR_MAP
from src.utils.tokens import Token
from src.nodes import *

class Parser():
    def __init__(self, tokens: list[Token], file_n: str) -> None:
        self.error = None
        self.tokens = tokens
        self.file_n = file_n
        self.indentation = None
        self.cur_block_indentation = None
        self.ast = AST()

    def make_ast(self) -> AST:
        if self.parse_block(self.tokens) == -1:
            return None
        return self.ast
    
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
    
    def parse_return_statement(self, line: list[Token]) -> int:
        cur_ln_num = line[0].ln
        line = line[1:]
        is_in_function = False
        cur_node_id = self.ast.cur_node.id
        while not isinstance(self.ast.cur_node, ASTBaseNode):
            if isinstance(self.ast.cur_node, FuncDefNode):
                is_in_function = True
                break
            self.ast.detraverse_node()
        if not is_in_function:
            self.error = SyntaxError("Return statement outside function", cur_ln_num, self.file_n)
            return -1
        self.ast.cur_node = self.ast.get_node_by_id(cur_node_id)
        new_node_id = self.ast.append_node(ReturnNode())
        self.ast.traverse_node_by_id(new_node_id)
        if self.parse_expression(line, "return_value", expr_4=False) == -1: return -1
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
        args = []
        cur_token = None
        for token in line:
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
        new_node_id = self.ast.append_node(FuncDefNode(func_identifier, args))
        self.ast.traverse_node_by_id(new_node_id)
        children_count = self.parse_children(cur_line_indentation, rem_line_tokens)
        self.ast.detraverse_node()
        return children_count

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
        if self.parse_expression(line, "iter", expr_0=False, expr_2=False, expr_4=False, expr_6=False, expr_8=False, expr_9=False) == -1: return -1
        child_count = self.parse_children(cur_line_indentation, rem_line_tokens)
        self.ast.detraverse_node()
        return child_count

    def parse_while_loop(self, line: list[Token], rem_line_tokens: list[list[Token]], cur_line_indentation: int) -> int:
        if line[len(line)-2].token_t != "TT_colon":
            self.error = SyntaxError("Expected colon", line[0].ln, self.file_n)
            return -1
        line = line[1:len(line)-2]
        new_node_id = self.ast.append_node(WhileLoopNode())
        self.ast.traverse_node_by_id(new_node_id)
        if self.parse_expression(line, "condition", expr_4=False) == -1: return -1
        child_count = self.parse_children(cur_line_indentation, rem_line_tokens)
        self.ast.detraverse_node()
        return child_count
        
    def parse_conditional_statement(self, line: list[Token], rem_line_tokens: list[list[Token]], cur_line_indentation: int) -> int:
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
        if self.parse_expression(line, "condition", expr_4=False) == -1: return -1, -1
        child_count = self.parse_children(cur_line_indentation, rem_line_tokens)
        self.ast.detraverse_node()
        return child_count

    def parse_children(self, parent_line_indentation: int, child_line_tokens: list[list[Token]]) -> int:
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

    def parse_func_call(self, line: list[Token]) -> int:
        name = line[0].token_v
        line = line[2:len(line)-2]
        new_line = []
        cur_arg_expr = []
        for token in line:
            if token.token_t == "TT_dquote" or token.token_t == "TT_squote":
                continue
            elif token.token_t == "TT_comma":
                new_line.append(cur_arg_expr)
                cur_arg_expr = []
            else:
                cur_arg_expr.append(token)
        new_line.append(cur_arg_expr)
        new_node_id = self.ast.append_node(FuncCallNode(name))
        self.ast.traverse_node_by_id(new_node_id)
        for arg_expr in new_line:
            if self.parse_expression(arg_expr, "args", expr_4=False) == -1: return -1
        self.ast.detraverse_node()
        return 0
    
    def parse_assign(self, line: list[Token]) -> int:
        new_node_id = self.ast.append_node(AssignNode(line[0].token_v))
        self.ast.traverse_node_by_id(new_node_id)
        if self.parse_expression(line[2:], "value", expr_4 = False) == -1: return -1
        self.ast.detraverse_node()
        return 0

    def parse_expression(self, tokens: list[Token], traversal_type: str, **kwargs: bool) -> ASTNode:
        cur_expr_map = EXPR_MAP
        for kw in kwargs.keys():
            kw_int = int(kw[-1])
            if kw_int not in EXPR_MAP:
                raise Exception("Invalid Argument for function 'parse_expression': Argument must be in scope of EXPR_MAP!")
            cur_expr_map[kw_int] = False
        self.ast.append_node(StringNode("This is an expression!!!"), traversal_type)
        return 0

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