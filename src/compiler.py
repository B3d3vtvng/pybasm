from src.lexer import Lexer

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
        tokens = lexer.lex()
        if lexer.error:
            print(lexer.error)
        else:
            print(tokens)
            print("Sucess")
            
