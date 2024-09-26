class Token():
    def __init__(self, ln, token_idx, token_t, token_v=None):
        self.ln = ln
        self.token_idx = token_idx
        self.token_t = token_t
        self.token_v = token_v

    def __str__(self):
        return f"{self.ln}:{self.token_idx}: {self.token_t}:{self.token_v}"