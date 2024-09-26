from src.cmdl_handler import CommandlineHandler
from src.compiler import Compiler

def compile():
    cmdl_handler = CommandlineHandler()
    file_n, flags = cmdl_handler.handle_args()
    if cmdl_handler.error:
        return cmdl_handler.error
    compiler = Compiler(file_n, flags)
    compiler.compile()

compilation_result = compile()