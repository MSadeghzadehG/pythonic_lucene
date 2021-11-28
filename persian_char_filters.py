from search_engine.analyzer.char_filter import CharFilter


class PersianCharFilter(CharFilter):

    def __init__(self):
        persian = 'ءاآأإئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیةيك'
        self.persian_chars = {
            char: 1
            for char in persian
        }
        
    def process(self, char):
        return char if char in self.persian_chars else None


class BadCharFilter(CharFilter):

    def __init__(self):
        bad = '\\s.,;،؛!؟?"\'()[\\]{}“”«»\n'
        self.bad_chars = {
            char: 1
            for char in bad
        }
        
    def process(self, char):
        return None if char in self.bad_chars else char
