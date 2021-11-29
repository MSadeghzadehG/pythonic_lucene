from hazm import Stemmer, Normalizer, stopwords_list
from search_engine.analyzer.token import Token
from search_engine.analyzer.token_filter import TokenFilter


class RemoveSpaceFilter(TokenFilter):

    def process(self, token):
        if token is not None:
            return Token(token.value.replace(' ',''), token.position, token.length)


class PersianStopFileFilter(TokenFilter):
    
    def __init__(self, stop_file_addr):
        with open(stop_file_addr, 'r') as f:
            self.stop_dict = {
                stop.replace('\n', ''): 1
                for stop in f.readlines()
            }

    def process(self, token):
        if token is not None and token.value not in self.stop_dict:
            return token


class PersianStopHazmFilter(TokenFilter):
    
    def __init__(self):
        self.stop_dict = {
            stop: 1
            for stop in stopwords_list()
        }

    def process(self, token):
        if token is not None and token.value not in self.stop_dict:
            return token


class PersianStemFilter(TokenFilter):
    
    def __init__(self):
        self.stemmer = Stemmer()

    def process(self, token):
        if token is not None:
            return Token(self.stemmer.stem(token.value), token.position, token.length)


class PersianNormalizeFilter(TokenFilter):
    
    def __init__(self):
        self.normalizer = Normalizer()

    def process(self, token):
        if token is not None:
            return Token(self.normalizer.normalize(token.value), token.position, token.length)
