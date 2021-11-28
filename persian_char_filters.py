from search_engine.analyzer.char_filter import CharFilter


class PersianCharFilter(CharFilter):

    def __init__(self):
        persian = [' ','\u200c','آ','ا','ب','پ','ت','ث','ج','چ','ح','خ','د','ذ','ر','ز','ژ','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ک','گ','ل','م','ن','و' ,'ه','ی']
        self.persian_chars = {
            char: 1
            for char in persian
        }
        
    def process(self, char):
        return char if char in self.persian_chars else None
