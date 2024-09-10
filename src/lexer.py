from src.utils.tokentypes import TOKEN_TYPES

class Lexer():
    def __init__(self, file_n):
        self.file_n = file_n
        self.error = None
        self.raw_code = self.get_raw_code()

    def get_raw_code(self):
        with open(self.file_n, "r") as file:
            return file.readlines()
        
    def lex(self):
        pass
        
print(TOKEN_TYPES)