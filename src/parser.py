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
        self.ast = AST()

    def make_ast(self) -> AST:
        self.parse_block(self.tokens)
        return self.ast
    
    def parse_block(self, tokens: list[Token]) -> None:
        line_tokens = self.get_line_tokens(tokens)
        print(line_tokens)
        return None
    
    def get_line_tokens(self, tokens: list[Token]) -> list[list[Token]]:
        line_tokens = []
        for i in range(1, tokens[len(tokens)-1].ln+1):
            line_tokens.append([token for token in tokens if token.ln == i])

        return line_tokens
    
    
        
