from hazm import Stemmer, Normalizer
from search_engine.analyzer.token import Token
from search_engine.analyzer.token_filter import TokenFilter


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


class PersianNormalizeFilter(TokenFilter):
    
    def __init__(self):
        super(PersianNormalizeFilter, self).__init__()
        self.normalizer = Normalizer()

    def process(self, token):
        if token is not None:
            return Token(self.normalizer.normalize(token.value), token.position, token.length)
