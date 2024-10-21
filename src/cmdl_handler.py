from src.utils.py_utils.error import FileError, FlagError
import sys

HELP_MSG = "Usage: python3 main.py [-b <name of output file>](Specifies output file)\n[--legacy](Changes the output file into legacy mode, providing no I/O but printing out pre-run and post-run variable state)\n[--help](Prints usage guide)\n<input file name>"

class CommandlineHandler():
    def __init__(self):
        self.flag_dict = {"-b": (True, self.handle_b), "--legacy": (False, self.handle_lgc)}
        self.argv = sys.argv[1:]
        self.error = None

    def handle_args(self):
        if self.argv == []:
            self.error = FileError("No file is specified!", "")
            return None, None
        if self.argv[0] == "--help":
            self.error = HELP_MSG
            return None, None
        try:
            open(self.argv[-1], "r")
        except Exception:
            self.error = FileError("The given file was not found or has an invalid file extension", self.argv[-1])
            return None, None
        if len(self.argv) == 1:
            return self.argv[0], {}
        file_n = self.argv.pop(-1)
        flag_found = False
        flags = {}
        for i, arg in enumerate(self.argv):
            if flag_found:
                flag_found = False
                if i+1 < len(self.argv): break
            else:
                next_arg = self.argv[i+1] if i+1 < len(self.argv) else ""
                if arg not in self.flag_dict:
                    self.error = FlagError("InvalidFlagError", "The given flag does not exist", arg)
                    return None, None
                if self.flag_dict[arg][0] and next_arg != "" and next_arg.strip()[0] == '-':
                    self.error = FlagError("MissingFlagArgumentError", "The given Flag requires an argument", arg)
                    return None, None
                self.error, flag_arg = self.flag_dict[arg][1](next_arg) if len(self.argv) < i+1 or self.flag_dict[arg][0] else self.flag_dict[arg][1]()
                flag_found = True if self.flag_dict[arg][0] else False
                flags[arg] = flag_arg

        return file_n, flags

    def handle_b(self, arg):
        if arg.strip() == "":
            return FlagError("MissingFlagArgumentError", "The given Flag requires an argument", "-b"), None
        if '.' not in arg:
            arg += (".bs")
        return None, arg
    
    def handle_lgc(self):
        return None, None
        