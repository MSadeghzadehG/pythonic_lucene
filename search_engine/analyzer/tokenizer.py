from .token import Token


class Tokenizer:
    '''
    A Tokenizer is a TokenStream whose input is a CharStream. 

    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/analysis/Tokenizer.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/analysis/Tokenizer.java    
    '''

    def tokenize(self, char_stream):
        '''
        returns a token generator.
        '''
        raise NotImplementedError("Please Implement this method")


class StandardTokenizer(Tokenizer):
    
    def __init__(self):
        self.token = ''
        self.delimiter = chr(32)

    def is_token(self, token):
        return token != ''

    def get_word(self, char_stream):
        while True:
            try:
                char = char_stream.__next__()
                if char is not None:
                    if char == self.delimiter and self.is_token(self.token):
                        o = self.token
                        self.token = ''
                        yield o
                    self.token += char
            except StopIteration:
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
