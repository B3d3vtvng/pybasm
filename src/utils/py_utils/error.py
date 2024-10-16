class Error():
    def __init__(self, error_t, error_v, error_ln, file_n):
        self.error_t = error_t
        self.error_v = error_v
        self.error_ln = error_ln
        self.file_n = file_n

    def __str__(self):
        return f"{self.file_n}:{self.error_ln}  {self.error_t}: {self.error_v}"

    
class FileError():
    def __init__(self, error_v, file_n):
        super().__init__("FileError", error_v, -1, file_n)

    def __str__(self):
        return f"FileError: {self.error_v}    File: {self.file_n}"

    
class FlagError():
    def __init__(self, error_t, error_v, flag):
        self.error_t = error_t
        self.error_v = error_v
        self.flag = flag

    def __str__(self):
        return f"{self.error_t}: {self.error_v}: {self.flag}"
    

class SyntaxError(Error):
    def __init__(self, error_v, error_ln, file_n):
        super().__init__("SyntaxError", error_v, error_ln, file_n)
    
class IndentationError(Error):
    def __init__(self, error_v: str, error_ln: int, file_n: str) -> None:
        super().__init__("IndentationError", error_v, error_ln, file_n)

class TypeError(Error):
    def __init__(self, error_v, error_ln, file_n) -> None:
        super().__init__("TypeError", error_v, error_ln, file_n)

class NameError(Error):
    def __init__(self, error_v, error_ln, file_n) -> None:
        super().__init__("NameError", error_v, error_ln, file_n)