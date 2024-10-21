from src.cmdl_handler import CommandlineHandler
from src.compiler import Compiler

def compile():
    cmdl_handler = CommandlineHandler()
    file_n, flags = cmdl_handler.handle_args()
    if cmdl_handler.error:
        print(cmdl_handler.error)
        exit(1)
    compiler = Compiler(file_n, flags)
    compiler.compile()
    print("Sucess!")

compile()