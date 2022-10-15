import enum


class Token:
    def __init__(self, token_text, token_type):
        self.text = token_text
        self.type = token_type

    @staticmethod
    def check_if_keyword(token_text):
        for _type in TokenType:
            # Relies on all keyword enum values being 1XX.
            if _type.name == token_text and 100 <= int(str(_type.value)) < 200:
                return _type
        return None


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
