import sys

from token import *


class Lexer:
    def __init__(self, _input):
        self.source = _input + '\n'  # Source code to lex as string. Append newline to simplify lex/pars last token
        self.curr_char = ''  # Current char in string
        self.curr_pos = -1  # Current pos in string
        self.next_char()

    # Process next character
    def next_char(self):
        self.curr_pos += 1
        if self.curr_pos >= len(self.source):
            self.curr_char = '\0'  # EOF
        else:
            self.curr_char = self.source[self.curr_pos]

    # Return the lookahead character
    def peek(self):
        if self.curr_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curr_pos + 1]

    def check_eq(self, _type, _type_2=None, fallback="abort"):
        if self.peek() == '=':
            las_char = self.curr_char
            self.next_char()
            return Token(las_char + self.curr_char, _type)
        else:
            return Token(self.curr_char, _type_2) if _type_2 is not None else fallback

    def check_type(self):
        return "num" if self.curr_char.isdigit() else "alpha"

    # Invalid token found, print error message and exit
    @staticmethod
    def abort(message):
        sys.exit(f"Lexing error. {message}")

    # Skip whitespaces except newlines, which will signify end of statement
    def skip_whitespace(self):
        while self.curr_char in [' ', '\t', '\r']:
            self.next_char()

    # Skip comments in the code
    def skip_comment(self):
        if self.curr_char == '#':
            while self.curr_char != '\n':
                self.next_char()

    # Return the next token
    def get_token(self):
        """Check the first character of this token to see if we can decide what it is. If it is a multiple character
        operator (e.g., !=), number, identifier, or keyword then we will process the rest. """
        self.skip_whitespace()
        self.skip_comment()

        token = None
        curr = self.curr_char

        match curr:
            case '+':
                token = Token(self.curr_char, TokenType.PLUS)
            case '-':
                token = Token(self.curr_char, TokenType.MINUS)
            case '*':
                token = Token(self.curr_char, TokenType.ASTERISK)
            case '/':
                token = Token(self.curr_char, TokenType.SLASH)
            case '\n':
                token = Token(self.curr_char, TokenType.NEWLINE)
            case '\0':
                token = Token('', TokenType.EOF)
            case '=':
                token = self.check_eq(TokenType.EQEQ, TokenType.EQ)
            case '>':
                token = self.check_eq(TokenType.GTEQ, TokenType.GT)
            case '<':
                token = self.check_eq(TokenType.LTEQ, TokenType.LT)
            case '!':
                res = self.check_eq(TokenType.NOTEQ)
                if res == "abort":
                    self.abort(f"Expected !=, got !{self.peek()} instead.")
                token = res
            case '\"':
                # Get characters between quotations.
                self.next_char()
                start_pos = self.curr_pos

                while self.curr_char != '\"':
                    # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                    # We will be using C's printf on this string.
                    if self.curr_char in ['\r', '\n', '\t', '\\', '%']:
                        self.abort("Illegal character in string.")
                    self.next_char()

                tok_text = self.source[start_pos: self.curr_pos]  # Get the substring.
                token = Token(tok_text, TokenType.STRING)
            case _:
                match self.check_type():
                    case "num":
                        # Leading character is a digit, so this must be a number.
                        # Get all consecutive digits and decimal if there is one.
                        start_pos = self.curr_pos
                        while self.peek().isdigit():
                            self.next_char()
                        if self.peek() == '.':  # Decimal!
                            self.next_char()

                            # Must have at least one digit after decimal.
                            if not self.peek().isdigit():
                                # Error!
                                self.abort("Illegal character in number.")
                            while self.peek().isdigit():
                                self.next_char()

                        tok_text = self.source[start_pos: self.curr_pos + 1]  # Get the substring.
                        token = Token(tok_text, TokenType.NUMBER)
                    case "alpha":
                        # Leading character is a letter, so this must be an identifier or a keyword.
                        # Get all consecutive alphanumeric characters.
                        start_pos = self.curr_pos
                        while self.peek().isalnum():
                            self.next_char()

                            # Check if the token is in the list of keywords.
                        tok_text = self.source[start_pos: self.curr_pos + 1]  # Get the substring.
                        keyword = Token.check_if_keyword(tok_text)
                        if keyword is None:  # Identifier
                            token = Token(tok_text, TokenType.IDENT)
                        else:  # Keyword
                            token = Token(tok_text, keyword)
                    case _:
                        self.abort(f"Unknown token: {self.curr_char}")

        self.next_char()
        return token
