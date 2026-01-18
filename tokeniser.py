import sys


class Token:
    # Token Types

    IDENTIFIER = 0
    MAPS_TO = 1
    END_LINE = 2
    BINDING = 3
    LEFT_PAREN = 4
    RIGHT_PAREN = 5

    PLUS = 6
    MINUS = 7
    STAR = 8
    SLASH = 9
    GREATER_THAN = 10

    NUMBER = 11

    IF = 12
    THEN = 13
    ELSE = 14

    def __init__(self, lexeme: str, token_type: int) -> None:
        self.token_type = token_type
        self.lexeme = lexeme


class Tokeniser:
    def __init__(self, source: str):
        self.index: int = 0
        self.tokens: list[Token] = []
        self.source: str = source
        self.had_error: bool = False

    def current_char(self) -> str:
        return self.source[self.index]

    def advance_char(self):
        self.index += 1

    def next_char(self):
        return self.source[self.index + 1]

    def advance_chars(self, count: int):
        self.index += count

    def expect(self, char: str):
        if self.index + 1 >= len(self.source):
            raise RuntimeError(f"Unexpected EOF after character '{self.current_char()}'")
        
        if self.source[self.index + 1] != char:
            raise RuntimeError(f"Expected character '{char}' but found '{self.current_char()}'")
    
    def expect_str(self, lexeme: str):
        if self.index + len(lexeme) >= len(self.source):
            raise RuntimeError(f"Unexpected EOF after '{lexeme}'")
        
        i = 0
        while i < len(lexeme):
            if self.source[self.index + i] != lexeme[i]:
                wrong_lexeme = self.source[self.index:self.index+len(lexeme)]
                raise RuntimeError(f"Expected sequence '{lexeme}' but found '{wrong_lexeme}'")
            i += 1

    def is_within_bounds(self):
        return self.index < len(self.source)

    def scan_number(self):
        number = ''
        while self.is_within_bounds() and self.current_char().isdigit():
            number += self.current_char()
            self.advance_char()
            if self.is_within_bounds() and self.current_char() == '.':
                number += self.current_char()
                self.advance_char()
                while self.is_within_bounds() and self.current_char().isdigit():
                    number += self.current_char()
                    self.advance_char()
        return number

    def scan_identifier(self):
        identifier = ''
        while self.is_within_bounds() and (
                self.current_char().isalpha()
                or self.current_char().isdigit()
                or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance_char()
        return identifier
    
    def current_starts_with(self, needle: str):
        haystack: str = self.source[self.index:]
        if len(haystack) < len(needle):
            return False
        for i, ch in enumerate(needle):
            if haystack[i] != ch:
                return False
        return True

    def tokenise(self):
        while self.is_within_bounds():
            if self.current_char() == '\n':
                self.tokens.append(Token('\n', Token.END_LINE))
                self.advance_char()
            elif self.current_char() == ':':
                self.expect('=')
                self.tokens.append(Token(':=', Token.BINDING))
                self.advance_chars(2)
            elif self.current_char() == '|':
                self.expect_str('|->')
                self.tokens.append(Token('|->', Token.MAPS_TO))
                self.advance_chars(3)
            elif self.current_char() == '(':
                self.tokens.append(Token('(', Token.LEFT_PAREN))
                self.advance_char()
            elif self.current_char() == ')':
                self.tokens.append(Token(')', Token.RIGHT_PAREN))
                self.advance_char()
            
            elif self.current_char() == '+':
                self.tokens.append(Token('+', Token.PLUS))
                self.advance_char()
            elif self.current_char() == '-':
                self.tokens.append(Token('-', Token.MINUS))
                self.advance_char()
            elif self.current_char() == '*':
                self.tokens.append(Token('*', Token.STAR))
                self.advance_char()
            elif self.current_char() == '/':
                self.tokens.append(Token('/', Token.SLASH))
                self.advance_char()
            elif self.current_char() == '>':
                self.tokens.append(Token('>', Token.GREATER_THAN))
                self.advance_char()

            elif self.current_starts_with('if'):
                self.tokens.append(Token('if', Token.IF))
                self.advance_chars(2)
            elif self.current_starts_with('then'):
                self.tokens.append(Token('then', Token.THEN))
                self.advance_chars(4)
            elif self.current_starts_with('else'):
                self.tokens.append(Token('else', Token.ELSE))
                self.advance_chars(4)

            elif self.current_char().isalpha():
                identifier = self.scan_identifier()
                self.tokens.append(Token(identifier, Token.IDENTIFIER))
            
            elif self.current_char().isdigit():
                number = self.scan_number()
                self.tokens.append(Token(number, Token.NUMBER))
            
            elif self.current_char() in (' ', '\t'):
                self.advance_char()

            # Skip '#' comments
            elif self.current_char() == '#':
                while self.is_within_bounds() and self.current_char() != '\n':
                    self.advance_char()

            else:
                self.had_error = True
                print(f"Unexpected character '{self.current_char()}' in source", file=sys.stderr)
                self.advance_char()


def main():
    source = 'fact := n |-> if n > 0 then n*fact(n-1) else 1\n'

    tk = Tokeniser(source)
    tk.tokenise()
    print([token.lexeme for token in tk.tokens])


if __name__ == '__main__':
    main()
