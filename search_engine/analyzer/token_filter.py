from hazm import Stemmer
from .token import Token


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
    

class PersianStopFilter(TokenFilter):
    
    def __init__(self, stop_file_addr):
        super(PersianStopFilter, self).__init__()
        with open(stop_file_addr, 'r') as f:
            self.stop_dict = {
                stop: 1
                for stop in f.readlines()
            }

    def process(self, token):
        if token is not None and token.value not in self.stop_dict:
            self.token_graph.add_token(token)
            return token


class PersianStemFilter(TokenFilter):
    
    def __init__(self):
        super(PersianStemFilter, self).__init__()
        self.stemmer = Stemmer()

    def process(self, token):
        if token is not None:
            return Token(self.stemmer.stem(token.value), token.position, token.length)
