from enum import Enum
from hazm import word_tokenize, Normalizer


class Tokenizer:

    def tokenize(self, char_stream):
        '''
        A Tokenizer is a TokenStream whose input is a Reader. 

        returns a token_graph.
        '''
        raise NotImplementedError("Please Implement this method")


class PersianTokenizer(Tokenizer):

    def __init__(self):
        self.normalizer = Normalizer()

    def tokenize(self, char_stream):
        token_graph = TokenGraph()
        pos = 0
        pos_len = 0
        for word in word_tokenize(self.normalizer.normalize(char_stream)):
            token_graph.add_token(Token(word, pos, pos_len))
            pos += 1
            pos_len += 1
        return token_graph


class TokenGraph:
    def __init__(self):
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def get_tokens_list(self):
        return self.tokens

    def get_tokens_str_list(self):
        return [t.get_val() for t in self.tokens]


class TokenType(Enum):
    ALPHA = 1
    ALPHANUM = 2
    DIGIT = 3
    LOWER = 4
    SUBWORD_DELIM = 5
    UPPER = 6


class Token:
    def __init__(self, value, position, length, token_type=TokenType.ALPHANUM):
        self.value = value
        self.position = position
        self.token_type = token_type
        self.length = length
    
    def get_val(self):
        return self.value
