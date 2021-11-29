from search_engine.analyzer.char_filter import CharFilter


class PersianCharFilter(CharFilter):

    def __init__(self):
        self.persian_chars = {
            ord(char): 0
            for char in '\u200c ءاآأإئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیةيك'
        }
        
    def process(self, char):
        if char is not None:
            return char if ord(char) in self.persian_chars else None


class BadCharFilter(CharFilter):

    def __init__(self):
        bad = '،؛؟\\“”«»!\"#$%&\'()*+,-./:;<=>?@[]^_`{|}~'
        self.bad_chars = {
            ord(char): 1
            for char in bad
        }
        
    def process(self, char):
        return chr(32) if ord(char) in self.bad_chars else char
