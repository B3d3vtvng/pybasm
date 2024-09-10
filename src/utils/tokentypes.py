import re


TOKEN_TYPES = {
    "EOF": ("TT_eof", ""), 
    "BOOL": ("TT_bool", ""),
    "FLOAT": ("TT_FLOAT", r""),
    "INT": ("TT_INT", r"^(?!['\"].*['\"]$)\d+$"),
    "STR": ("TT_str", r"^(?:'[^']*'|\"[^\"]*\")$"),
    "IDENTIFIER": ("TT_identifier", r"^(?!def |DEF |return |RETURN |if |IF |not |NOT |elif |ELIF |else |ELSE |while |WHILE |for |FOR |in |IN )(?!.*(\)|\(|\]|\[|\+|-|\*|/|%|=|!|<|>|,|:))(?!^\d+$).*[^\d].*$"), 
    "LPAREN": ("TT_lparen", r"\)"),
    "RPAREN": ("TT_rparen", r"\("),
    "LBRACKET": ("TT_lbracket", r"\]"),
    "RBRACKET": ("TT_rbracket", r"\["),
    "PLUS": ("TT_plus", r"\+"),
    "SUB": ("TT_sub", r"-"),
    "MUL": ("TT_mul", r"\*"),
    "DIV": ("TT_div", r"/"),
    "MOD": ("TT_mod", r"%"),
    "EQU": ("TT_equ", r"="),
    "DEQU": ("TT_dequ", r"=="),
    "NEQU": ("TT_nequ", r"!=|/="),
    "GREATER": ("TT_greater", r">"),
    "LESS": ("TT_less", r"<"),
    "GEQU": ("TT_gequ", r">="), 
    "LEQU": ("TT_lequ", r"<="),
    "COMMA": ("TT_comma", r","),
    "COLON": ("TT_colon", r":"),
    "DEF": ("TT_def", r"def|DEF"),
    "RET": ("TT_ret", r"return|RETURN"),
    "IF": ("TT_if", r"if|IF"),
    "NOT": ("TT_not", r"not|NOT"),
    "ELIF": ("TT_elif", r"elif|ELIF"),
    "ELSE": ("TT_else", r"else|ELSE"),
    "WHILE": ("TT_while", r"while|WHILE"),
    "FOR": ("TT_for", r"for|FOR"), 
    "IN": ("TT_in", r"in|IN")
    }    

"""
while True:
    user_input = input(">>>")
    user_input = user_input.split()
    new_user_input = []
    for part in user_input:
        if "(" in part:
            part.split("(")
            part[1] = "(" + part[1]
            new_user_input.append(part[0])
            new_user_input.append(part[1])
    user_input = new_user_input + user_input

    tokens = []
    for part in user_input:
        for token in TOKEN_TYPES.keys():
            token_type, token_regex = TOKEN_TYPES[token]
            if token_regex == "":
                continue

            match = re.search(token_regex, part)
            if not match:
                continue
            start_idx, end_idx = match.start(), match.end()
            print(start_idx, end_idx, token)
"""
