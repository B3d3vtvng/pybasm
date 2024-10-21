from src.utils.py_utils.tokentypes import TOKEN_TYPES, KEYWORDS 
from src.utils.py_utils.error import SyntaxError
from src.utils.py_utils.tokens import Token
from src.utils.py_utils.sort_tokens import sort_tokens
from src.utils.py_utils.lrange import lrange

class Lexer():
    def __init__(self, file_n: str) -> None:
        self.file_n = file_n
        self.error = None
        self.raw_code = self.get_raw_code()

    def get_raw_code(self) -> None:
        with open(self.file_n, "r") as file:
            return file.readlines()
        
    def make_tokens(self) -> list:
        for i, line in enumerate(self.raw_code):
            if "#" in line:
                line = line[:line.index('#')]
                self.raw_code.pop(i)
                self.raw_code[i] = line
        kw_tokens = self.make_kw_tokens()
        res = self.make_typed_tokens(kw_tokens)
        if not res:
            return None
        
        typed_tokens, new_kw_tokens = res
        tokens = new_kw_tokens + typed_tokens
        tokens = sort_tokens(tokens)
        return tokens

    
    def make_kw_tokens(self) -> list[Token]:
        tokens = []
        for i, line in enumerate(self.raw_code):
            redo_tokens = []
            for token_type in TOKEN_TYPES:
                token_name, token_ident = TOKEN_TYPES[token_type]
                if token_ident == "":
                    continue

                if token_ident not in line:
                    continue

                token_idx = line.index(token_ident)
                token = self.make_kw_token(i+1, token_idx, line, token_ident, token_name, is_keyword=self.is_keyword(token_ident))
                if not token:
                    continue

                token_end_idx = line.index(token_ident)+len(token_ident)
                if token_ident in line[token_end_idx:]:
                    redo_tokens.append([token_type, token_end_idx])
                tokens.append(token)

            tokens.append(Token(i+1, len(line), "TT_eol", None))

            while redo_tokens != []:
                for token_type, token_end_idx in redo_tokens:
                    new_line = line[token_end_idx:]
                    token_name, token_ident = TOKEN_TYPES[token_type]

                    token_idx = new_line.index(token_ident) + token_end_idx
                    token = self.make_kw_token(i+1, token_idx, new_line, token_ident, token_name, is_keyword=self.is_keyword(token_ident))
                    if not token: continue

                    new_token_end_idx = token_end_idx + new_line.index(token_ident)+len(token_ident)
                    if token_ident not in line[new_token_end_idx:]:
                        redo_tokens.pop(redo_tokens.index([token_type, token_end_idx]))
                    else:
                        redo_tokens[redo_tokens.index([token_type, token_end_idx])][1] = new_token_end_idx

                    tokens.append(token)
                    
        tokens = sort_tokens(tokens)
        if tokens:
            tokens.append(Token(tokens[-1].ln+1, -1, "TT_eof", None))
        else:
            tokens = [Token(0, 0, "TT_eof", None)]
        return tokens
    
    def make_typed_tokens(self, kw_tokens: list[Token]) -> tuple[list[Token]]:
        tokens = []
        for i, line in enumerate(self.raw_code):
            if line[0] == "#":
                continue
            pind_token = self.get_indentation(line, i+1)
            if pind_token:
                tokens.append(pind_token)

            line_tokens = [token for token in kw_tokens if token.ln == i+1]
            res = self.make_str_tokens(i+1, line, line_tokens)
            if res == "ERROR":
                return None
            if res:
                if res[0] != []:
                    for token in res[0]:
                        tokens.append(token)
                new_line_tokens = res[1]
                if new_line_tokens != line_tokens:
                    kw_tokens = [token for token in kw_tokens if token.ln != i+1]
                    kw_tokens += new_line_tokens
                line_tokens = new_line_tokens
                line_tokens += res[0]
                line_tokens = sort_tokens(line_tokens)
            occ_idxs = self.get_occ_idxs(line_tokens)

            non_token_code = self.get_non_token_code(occ_idxs, line)

            if not non_token_code:
                continue
            
            for non_token, non_token_idx in non_token_code:
                if non_token.strip() == "":
                    continue
                token = self.make_typed_token(i+1, non_token_idx, non_token.strip())
                if not token:
                    return None
                tokens.append(token)

        return tokens, kw_tokens
    
    def make_str_tokens(self, line_num: int, line: str, line_tokens: list[Token]) -> tuple[list[Token], list[Token]]:
        str_tokens = []
        new_line_tokens = line_tokens
        quote_idxs = self.get_quote_idxs(line_tokens)
        if quote_idxs == "ERROR":
            self.error = SyntaxError("Unclosed Quotes", line_num, self.file_n)
            return "ERROR"
        elif quote_idxs == []:
            return None
        for start_idx, end_idx in quote_idxs:
            res = self.make_str_token(line, line_tokens, line_num, start_idx, end_idx)
            str_tokens.append(res[0])
            new_line_tokens = res[1]
        return str_tokens, new_line_tokens
    
    def make_str_token(self, line: str, line_tokens: list[Token], line_num: int, start_idx: int, end_idx: int) -> tuple[Token, list[Token]]:
        string_value = line[start_idx:end_idx]
        new_line_tokens = [token for token in line_tokens if token.token_idx < start_idx or token.token_idx >= end_idx]
        return Token(line_num, start_idx, "TT_str", string_value), new_line_tokens
    
    def get_quote_idxs(self, line_tokens: list[Token]) -> list[tuple[int, int]]:
        quote_idxs = []
        cur_quote_idx = None
        cur_quote_idx_type = None
        for token in line_tokens:
            if token.token_t[4:] == "quote":
                if not cur_quote_idx_type:
                    cur_quote_idx_type = token.token_t
                    cur_quote_idx = token.token_idx
                elif cur_quote_idx_type == token.token_t:
                    quote_idxs.append((cur_quote_idx+1, token.token_idx))
                    cur_quote_idx = None
                    cur_quote_idx_type = None

        if cur_quote_idx:
            return "ERROR"
        
        new_quote_idxs = []
        for quote_idx in quote_idxs:
            if quote_idx[0] != quote_idx[1]:
                new_quote_idxs.append(quote_idx)
                
        return new_quote_idxs
    
    def get_non_token_code(self, occ_idxs: list[int], line: str) -> list[str]:
        non_token_code = []
        if len(occ_idxs) == 0:
            last_occ_idx = 0
        else:
            last_occ_idx = occ_idxs[len(occ_idxs)-1]
        line_occ_idxs = lrange(len(line[:last_occ_idx])+1)
        if occ_idxs == line_occ_idxs and len(line.strip()) == len(line_occ_idxs):
            return non_token_code

        if occ_idxs == []:
            return [(line, 0)]
        
        first_occ_idx = occ_idxs[0]
        if len(occ_idxs) == 1:
            non_token_code.append((line[first_occ_idx+1:], first_occ_idx+1))
            if first_occ_idx != 0:
                non_token_code = [(line[:first_occ_idx], 0)] + non_token_code
            return non_token_code
        elif first_occ_idx != 0:
            non_token_code.append((line[0:first_occ_idx], 0))
        for idx, occ_idx in enumerate(occ_idxs):
            if len(occ_idxs) != idx+1 and occ_idx+1 != occ_idxs[idx+1]:
                non_token_code.append((line[occ_idx+1:occ_idxs[idx+1]].strip(), occ_idx+1))
        if occ_idx != len(line)-1:
            if non_token_code[len(non_token_code)-1][1] != occ_idx:
                non_token_code.append((line[occ_idx+1:], occ_idx+1))

        return non_token_code
    
    def get_indentation(self, line: str, line_idx: int) -> None | Token:
        space = " "
        highest_pind = None
        for i in range(1, 40):
            check_str = space * i
            if line[:i] == check_str:
                highest_pind = i
        if highest_pind:
            return Token(line_idx, -1, "TT_pind", highest_pind)
        return None
    
    def get_occ_idxs(self, line_tokens: list[Token]) -> list[int]:
        occ_idxs = []
        for token in line_tokens:
            if token.token_t == "TT_eol":
                continue
            if token.token_t != "TT_str":
                occ_idxs += range(token.token_idx, token.token_idx + len(get_token_ident(token.token_t)))
            else:
                occ_idxs += range(token.token_idx, token.token_idx + len(token.token_v))
        return occ_idxs
    
    def make_typed_token(self, ln: int, non_token_idx: int, non_token: str) -> Token:
        if non_token.isdigit():
            token = Token(ln, non_token_idx, "TT_int", int(non_token))
        elif self.isfloat(non_token):
            token = self.make_float_token(ln, non_token_idx, non_token)
        elif non_token == "True" or non_token == "False":
            bool_value = True if non_token == "True" else False
            token = Token(ln, non_token_idx, "TT_bool", bool_value)
        else:
            token = Token(ln, non_token_idx, "TT_identifier", non_token)

        return token
    
    def isfloat(self, non_token: str) -> bool:
        non_token = non_token.strip()
        dot_found = False
        for char in non_token:
            if not char.isdigit() and char != ".":
                return False
            elif not char.isdigit() and char == "." and dot_found:
                return False
            elif not char.isdigit() and char == "." and not dot_found:
                return True
            elif not char.isdigit():
                return False
        return False
    
    def make_float_token(self, ln: int, non_token_idx: int, non_token: str) -> Token:
        float_val_left, float_val_right = non_token.split(".")
        float_val = int(float_val_left)
        float_val += int(float_val_right) / pow(10, len(float_val_right))
        return Token(ln, non_token_idx, "TT_float", float_val)


    def get_token_count(self, tokens: list[Token], token_t: str) -> int:
        return len([token for token in tokens if token.token_t == token_t])

    def make_kw_token(self, ln_num: int, token_idx: int, line: str, token_ident, token_name: str, is_keyword: bool=False) -> Token:
        if is_keyword:
            is_valid = self.validate_keyword(token_ident, line.index(token_ident), line)
            if not is_valid: return None
        return Token(ln_num, token_idx, token_name, None)

    def is_keyword(self, token_ident: str) -> bool:
        return token_ident.upper() in KEYWORDS

    def validate_keyword(self, token_ident: str, token_idx: int, line: str):
        line = line.strip()
        if line == token_ident: return True

        real_token_idx = line.index(token_ident)
        pre_token_idx = real_token_idx-1 if real_token_idx != 0 else 0
        post_token_idx = real_token_idx + len(token_ident)

        if real_token_idx == 0 and len(line) > post_token_idx and line[post_token_idx] == " " or line[post_token_idx] == ":":
            return True
        
        if line[pre_token_idx] == " " and post_token_idx == len(line):
            return True
        
        if line[pre_token_idx] == " " and line[post_token_idx] == " " or line[post_token_idx] == ":":
            return True
        
        return False
    
def get_token_ident(token_name: str) -> str:
    match token_name:
        case "TT_dequ": return "=="
        case "TT_gequ": return ">="
        case "TT_lequ": return "<="
        case "TT_nequ": return "!="
        case _:
            return TOKEN_TYPES[token_name[3:].upper()][1]