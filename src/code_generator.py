from src.nodes import *

class CodeGenerator():
    def __init__(self, ast: AST, new_file_n: str) -> None:
        self.ast = ast
        #self.new_file = open(new_file_n, "x")
        self.error = None

    def generate_code(self) -> None:
        pass
        