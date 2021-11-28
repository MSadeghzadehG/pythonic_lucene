from enum import Enum


class Tokenizer:

    def tokenize(self, char_stream):
        '''
        A Tokenizer is a TokenStream whose input is a Reader. 

        returns a token_graph.
        '''
        raise NotImplementedError("Please Implement this method")


class StandardTokenizer(Tokenizer):
    
    def __init__(self):
        self.token = ''
        self.delimiter = chr(32)

    def is_token(self, token):
        return token != ''

    def get_char(self,char_stream):
        try:
            return char_stream.__next__()
        except StopIteration:
            return None

    def get_word(self, char_stream):
        while True:
            char = self.get_char(char_stream)
            if char is not None:
                if char == self.delimiter and self.is_token(self.token):
                    o = self.token
                    self.token = ''
                    yield o
                self.token += char
            else:
                if self.is_token(self.token):
                    o = self.token
                    self.token = ''
                    yield o
                break

    def tokenize(self, char_stream):
        pos = 0
        pos_len = 0
        try:
            while True:
                word = self.get_word(char_stream).__next__()
                token = Token(word, pos, pos_len)
                pos += 1
                pos_len += 1
                yield token
        except StopIteration:
            pass


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
