from src.tokens import Token
from src.nodes import AST

class Parser():
    def __init__(self, tokens: list[Token], file_n: str) -> None:
        self.error = None
        self.tokens = tokens
        self.file_n = file_n

    def make_ast(self) -> AST:
        return "AST"