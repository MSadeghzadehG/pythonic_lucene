from enum import Enum


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
