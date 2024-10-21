from src.lexer import Lexer
from src.parser import Parser
from src.code_generator import CodeGenerator

class Compiler():
    def __init__(self, file_n, flags):
        self.flags = flags
        self.file_n = file_n
        self.new_file_n = self.get_new_file_n()

    def get_new_file_n(self):
        if not self.flags or "-bs" not in self.flags:
            raw_file_n = self.file_n.split('.')[1]
            return raw_file_n+".bs"
        else:
            return self.flags["-bs"]
        
    def compile(self):
        lexer = Lexer(self.file_n)
        tokens = lexer.make_tokens()
        print(tokens)
        if lexer.error:
            print(lexer.error)
            exit(1)
        parser = Parser(tokens, self.file_n)
        ast = parser.make_ast()
        if parser.error:
            print(parser.error)
            exit(2)
        print(ast)
        code_generator = CodeGenerator(ast, self.new_file_n)
        code_generator.generate_code()
        if code_generator.error:
            print(code_generator.error)
            exit(3)
        return 0

