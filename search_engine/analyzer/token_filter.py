class TokenGraph:
    def __init__(self):
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def get_tokens(self):
        return self.tokens


class TokenFilter:

    def __init__(self):
        self.token_graph = TokenGraph()
    
    def process(self, token):
        raise NotImplementedError("Please Implement this method")

    def get_tokens_list(self):
        return self.token_graph.get_tokens()

    def get_tokens_str_list(self):
        return [t.get_val() for t in self.token_graph.get_tokens()]


class StandardTokenFilter(TokenFilter):

    def process(self, token):
        self.token_graph.add_token(token)
        return token
