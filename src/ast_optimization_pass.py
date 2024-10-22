from src.nodes import *

class ASTOptimizationPass():
    def __init__(self, ast: AST) -> None:
        self.ast = ast
        self.error = None

    def optimize_ast(self) -> AST:
        pass