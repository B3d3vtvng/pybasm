TOKEN_TYPES = {
    "EOF": ("TT_eof", ""), 
    "EOL": ("TT_eol", ""),
    "PIND": ("TT_pind", ""),
    "BOOL": ("TT_bool", ""),
    "FLOAT": ("TT_FLOAT", ""),
    "INT": ("TT_INT", ""),
    "STR": ("TT_str", ""),
    "IDENTIFIER": ("TT_identifier", ""),
    "CMND": ("TT_cmnd", "#"), 
    "LPAREN": ("TT_lparen", "("),
    "RPAREN": ("TT_rparen", ")"),
    "LBRACKET": ("TT_lbracket", "["),
    "RBRACKET": ("TT_rbracket", "]"),
    "PLUS": ("TT_plus", "+"),
    "SUB": ("TT_sub", "-"),
    "MUL": ("TT_mul", "*"),
    "DIV": ("TT_div", "/"),
    "MOD": ("TT_mod", "%"),
    "EQU": ("TT_equ", "="),
    "NEQU": ("TT_nequ", "!="),
    "GREATER": ("TT_greater", ">"),
    "LESS": ("TT_less", "<"),
    "COMMA": ("TT_comma", ","),
    "COLON": ("TT_colon", ":"),
    "DQUOTE": ("TT_dquote", '"'),
    "SQUOTE": ("TT_squote", "'"),
    "DEF": ("TT_def", "def"),
    "RET": ("TT_ret", "return"),
    "IF": ("TT_if", "if"),
    "NOT": ("TT_not", "not"),
    "ELIF": ("TT_elif", "elif"),
    "ELSE": ("TT_else", "else"),
    "WHILE": ("TT_while", "while"),
    "FOR": ("TT_for", "for"), 
    "IN": ("TT_in", "in")
    }    

KEYWORDS = [
    "DEF",
    "RET", 
    "IF", 
    "NOT", 
    "ELIF", 
    "ELSE", 
    "WHILE", 
    "FOR", 
    "IN"
]

SPECIAL_TOKENS = [
    "==", 
    "!=", 
    "+=", 
    "-=",
    "*=",
    "/="
]