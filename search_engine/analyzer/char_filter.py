from string import whitespace


class CharFilter:

    def process(self, char):
        '''
        returns corrected char, else returns None.
        '''
        raise NotImplementedError("Please Implement this method")


class WhitespcaesCharFilter(CharFilter):

    def __init__(self):
        self.whitespaces = {
            ord(char): 0
            for char in whitespace
        }
    
    def process(self, char):
        return chr(32) if ord(char) in self.whitespaces else char