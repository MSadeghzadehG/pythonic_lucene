class TokenGraph:
    def __init__(self):
        self.tokens = []

    def add_token(self, token):
        self.tokens.append(token)

    def get_tokens(self):
        return self.tokens


class TokenFilter:
    '''
    A TokenFilter is a TokenStream whose input is another TokenStream.
    This is an abstract class; subclasses must override process().
    
    Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/analysis/TokenFilter.html
    Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/analysis/TokenFilter.java
    '''

    def __init__(self):
        self.token_graph = TokenGraph()
    
    def process(self, token):
        raise NotImplementedError("Please Implement this method")

    def get_tokens_list(self):
        return self.token_graph.get_tokens()

    def get_tokens_str_list(self):
        return [t.get_val() for t in self.token_graph.get_tokens()]
