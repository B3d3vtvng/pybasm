from src.lexer import Lexer
from src.parser import Parser

class Compiler():
    def __init__(self, file_n, flags):
        self.flags = flags
        self.file_n = file_n
        self.new_file_n = self.get_new_file_n()
        self.tokens = []

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
            exit(1)
        for token in ast:
            print(token)
            print("\n")
            
