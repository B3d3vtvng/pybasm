from src.lexer import Lexer
from src.parser import Parser
from src.ast_optimization_pass import ASTOptimizationPass
from src.code_generator import CodeGenerator

class Compiler():
    def __init__(self, file_n, flags):
        self.flags = flags
        self.file_n = file_n
        self.new_file_n = self.get_new_file_n()

    def get_new_file_n(self):
        if not self.flags or "-o" not in self.flags:
            raw_file_n = self.file_n.split('.')[0]
            return raw_file_n+".c"
        else:
            return self.flags["-o"]
        
    #wrapper function to handle errors in a clean way :)
    def run_component(self, component: object, function: callable, error_code, *args) -> any:
        output = function(*args)
        if component.error:
            print(component.error)
            exit(error_code)
        return output
        
    def compile(self):
        lexer = Lexer(self.file_n)
        tokens = self.run_component(lexer, lexer.make_tokens, 1)
        parser = Parser(tokens, self.file_n)
        ast = self.run_component(parser, parser.make_ast, 2)
        print(ast)
        ast_optimizer = ASTOptimizationPass(ast)
        ast = self.run_component(ast_optimizer, ast_optimizer.optimize_ast, 3)
        code_generator = CodeGenerator(ast, self.new_file_n)
        self.run_component(code_generator, code_generator.generate_code, 4)
        return 0

