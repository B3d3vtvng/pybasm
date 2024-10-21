BINOP_OPERATOR_PRECEDENCE_DICT = {
    "TT_plus": 2,
    "TT_sub": 2,
    "TT_mul": 1,
    "TT_div": 1
}

CONDITION_OPERATOR_PRECEDENCE_DICT = {
    "TT_greater": 2,
    "TT_less": 2,
    "TT_gequ": 2,
    "TT_lequ": 2,
    "TT_dequ": 2,
    "TT_and": 1,
    "TT_or": 1,
}

SLICE_OPERATOR_PRECEDENCE_DICT = {
    "TT_colon": 1
}

EXPR_MAP = {
    0: True, #simple_literal
    1: True, #array_literal
    2: True, #simple_var
    3: True, #array_var, includes str
    4: True, #slice_expr
    5: True, #func_call
    6: True, #un_op_expr
    7: True, #bin_op_expr
    8: True, #cond_expr
}