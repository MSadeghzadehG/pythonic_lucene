class CharFilter:

    def process(self, char):
        '''
        returns corrected char if char is valid, else returns None.
        '''
        raise NotImplementedError("Please Implement this method")


class PersianCharFilter(CharFilter):

    def __init__(self):
        persian = [' ','\u200c','آ','ا','ب','پ','ت','ث','ج','چ','ح','خ','د','ذ','ر','ز','ژ','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ک','گ','ل','م','ن','و' ,'ه','ی']
        self.persian_chars = {}
        for i in range(len(persian)):
            self.persian_chars[persian[i]] = i

    def process(self, char):
        return char #if char in self.persian_chars else None
