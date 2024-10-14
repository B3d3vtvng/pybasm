BIN_OP_OPERATORS = [
    "TT_plus", 
    "TT_sub", 
    "TT_mul",
    "TT_div"
]
EXPR_OPERATORS = [ 
    ("TT_equ", "TT_equ"),
    ("TT_greater", "TT_equ"),
    ("TT_less", "TT_equ"),
    ("TT_greater"), 
    ("TT_less")
]

EXPR_MAP = {
    0: True, #simple_literal
    1: True, #array_literal, includes str
    2: True, #simple_var
    3: True, #array_var, includes str
    4: True, #slice_expr
    5: True, #func_call
    6: True, #un_op_expr
    7: True, #bin_op_expr
    8: True, #log_expr
    9: True, #cond_expr
}