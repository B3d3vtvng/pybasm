from cmdl_handler import CommandlineHandler
from compiler import Compiler

def compile():
    cmdl_handler = CommandlineHandler()
    compiler = Compiler()
    file_n, flags = cmdl_handler.handle_args()
    if cmdl_handler.error:
        return cmdl_handler.error
    compiler.compile(file_n, flags)