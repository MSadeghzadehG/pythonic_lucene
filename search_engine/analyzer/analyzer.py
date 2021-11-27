class Analyzer:

    def __init__(self, char_filters, tokenizer, token_filters):
        '''
        An Analyzer builds TokenStreams, which analyze text. It thus represents a policy for extracting index terms from text. 

        Doc: https://lucene.apache.org/core/8_11_0/core/org/apache/lucene/analysis/Analyzer.html
        Code: https://github.com/apache/lucene/blob/main/lucene/core/src/java/org/apache/lucene/analysis/Analyzer.java
        
        filters order is importrant.
        '''
        self.char_filters = char_filters
        self.tokenizer = tokenizer
        self.token_filters = token_filters

    def analyze_val(self, val):
        '''
        returns TokenGraph
        '''
        char_stream = self.process_chars(val)
        token_stream = self.tokenizer.tokenize(char_stream)
        processed_tokens = self.process_tokens(token_stream)
        return processed_tokens

    def process_chars(self, char_stream):
        '''
        char_stream: string.
        '''
        filtered_stream = list(char_stream)
        for char_filter in self.char_filters:
            filtered_stream = list(map(char_filter.process, filtered_stream))
        return ''.join(
            [c for c in filtered_stream if c is not None]
        )

    def process_tokens(self, token_stream):
        '''
        token_stream: TokenGraph.
        '''
        filtered_tokens = token_stream
        for token_filter in self.token_filters:
            filtered_tokens = list(map(token_filter.process, filtered_tokens))
        return filtered_tokens
