class Error():
    def __init__(self, error_t, error_v, error_ln, file_n):
        self.error_t = error_t
        self.error_v = error_v
        self.error_ln = error_ln
        self.file_n = file_n

    def __str__(self):
        return f"{self.file_n}:{self.error_ln}  {self.error_t}: {self.error_v}"
    
class FileError():
    def __init__(self, error_t, error_v, file_n):
        self.error_t = error_t
        self.error_v = error_v
        self.file_n = file_n

    def __str__(self):
        return f"{self.error_t}: {self.error_v}    File: {self.file_n}"
    
class FlagError():
    def __init__(self, error_t, error_v, flag):
        self.error_t = error_t
        self.error_v = error_v
        self.flag = flag

    def __str__(self):
        return f"{self.error_t}: {self.error_v}: {self.flag}"