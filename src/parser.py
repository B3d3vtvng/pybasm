from src.utils.error import SyntaxError
from src.utils.operators import EXPR_OPERATORS, BIN_OP_OPERATORS
#from src.utils.node_handlers import NODE_HANDLERS
from src.tokens import Token
from src.nodes import *

class Parser():
    def __init__(self, tokens: list[Token], file_n: str) -> None:
        self.error = None
        self.tokens = tokens
        self.file_n = file_n

    def make_ast(self) -> AST:
        ast = self.make_top_structure()
        return ast
    
    def make_top_structure(self, tokens: list[Token]) -> AST:
        ast = AST()
        token_lines = []
        for i in range(1, tokens[len(tokens)-2]):
            token_lines.append([token for token in tokens if token.ln == i])
        for token_line in token_lines:
            if self.is_literal(token_line):
                node = self.make_literal_node(token_line)
            elif self.is_arr_literal(token_line):
                node = self.make_array_literal_node()
            elif self.is_expression(token_line):
                node = self.make_expression_node(token_line)
            elif self.is_function_dec(token_line):
                node = self.make_function_dec_node(token_lines)
            elif self.is_function_call(token_line):
                node = self.make_function_call_node(token_line)
            elif self.is_var_dec(token_line):
                node = self.make_var_dec_node(token_line)
            elif self.is_var(token_line):
                node = self.make_var_node(token_line)
            elif self.is_array_var(token_line):
                node = self.make_array_var_node(token_line)
            elif self.is_binop(token_line):
                node = self.make_binop_node(token_line)
            elif self.is_for_loop(token_line):
                node = self.make_for_loop_node(token_lines)
            elif self.is_while_loop(token_line):
                node = self.make_while_loop_node(token_lines)
            elif self.is_if(token_line):
                node = self.make_if_node(token_lines)
            elif self.is_elif(token_line):
                node = self.make_elif_node(token_lines)
            elif self.is_else(token_line):
                node = self.make_else_node(token_lines)
            else:
                self.error = SyntaxError("Invalid Syntax \nHint: Some Python features are currently not supported, please look at https://github.com/B3d3vtvng/pybasm/blob/main/README.md for more info.")
                return None
            if self.error:
                return None
            ast.append_node(node)
        return ast
    
    def is_literal(self, token_line: list[Token]) -> bool:
        token_line = token_line[:len(token_line)-1]
        if len(token_line) == 1 and token_line[0].token_t == "TT_str" | "TT_int" | "TT_float" | "TT_bool":
            return True
        return False

    def make_literal_node(self, token_line: list[Token]) -> StringNode | NumberNode | None:
        match token_line[0].token_t:
            case "TT_int" | "TT_float":
                return NumberNode(token_line[0].token_v)
            case "TT_str":
                return StringNode(token_line[0].token_v)
            case "TT_bool":
                return BoolNode(token_line[0].token_v)
            
    def is_arr_literal(self, token_line: list[Token]) -> bool:
        token_line = token_line[:len(token_line)-1]
        if token_line[0] != "TT_lbracket" and token_line[len(token_line)-1] != "TT_rbracket":
            return False
        return True
    
    def make_arr_literal_node(self, token_line: list[Token]) -> ArrayNode:
        token_line = token_line[1:len(token_line)-2]
        arr_elements = []
        last_comma_idx = 0
        for i, token in enumerate(token_line):
            if token.token_t == "TT_comma":
                arr_elements.append([token_line[last_comma_idx:i]])
                last_comma_idx = i+1
        if arr_elements == []:
            arr_elements = [token_line]
        return ArrayNode(arr_elements)
    
    def is_expression(self, token_line: list[Token]) -> ExpressionNode:
        pass
        
