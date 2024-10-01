from src.tokens import Token
from src.nodes import *

class Parser():
    def __init__(self, tokens: list[Token], file_n: str) -> None:
        self.error = None
        self.tokens = tokens
        self.file_n = file_n

    def make_ast(self) -> AST:
        tokens_lits_as_nodes = self.make_literal_nodes()
        return tokens_lits_as_nodes
    
    def make_literal_nodes(self) -> list[Token | ASTNode]:
        tokens_lits_as_nodes = []
        for token in self.tokens:
            match token.token_t:
                case "TT_int" | "TT_float":
                    tokens_lits_as_nodes.append(NumberNode(token.token_v))
                case "TT_str":
                    tokens_lits_as_nodes.append(StringNode(token.token_v))
                case _:
                    tokens_lits_as_nodes.append(token)

        return tokens_lits_as_nodes