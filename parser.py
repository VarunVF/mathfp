from ast_nodes import *
from tokeniser import Token, Tokeniser


class Parser:
    def __init__(self, tokens: list[Token]):
        self.index = 0
        self.tokens = tokens
        self.ast = Program()
    
    def is_at_end(self):
        return self.index >= len(self.tokens)
    
    def current_token(self):
        return self.tokens[self.index]

    def can_lookahead(self):
        return self.index + 1 < len(self.tokens)

    def lookahead(self):
        if self.index + 1 < len(self.tokens):
            return self.tokens[self.index + 1]
        else:
            raise RuntimeError("Unexpected end of input")

    def advance(self, count: int = 1):
        self.index += count

    def consume(self, expected_type: int):
        tk_type = self.current_token().token_type
        if tk_type != expected_type:
            raise RuntimeError(f"Expected a token of type {expected_type} but found {tk_type}")
        previous = self.current_token()
        self.advance()
        return previous

    def parse(self):
        self.program()

    # Grammar rules.

    def program(self):
        while not self.is_at_end():
            expr = self.expression()
            if expr is not None:
                self.ast.add_expression(expr)
        return self.ast
    
    def expression(self):
        if self.can_lookahead():
            if self.lookahead().token_type == Token.BINDING:
                return self.binding()
            elif self.lookahead().token_type == Token.MAPS_TO:
                return self.function_def()
        if self.current_token().token_type == Token.IF:
            return self.if_expr()
        return self.binary_expr()

    def function_def(self):
        param = self.current_token().lexeme
        self.advance()
        self.consume(Token.MAPS_TO)
        body = self.expression()
        return FunctionDef_(param, body)
    
    def function_call(self):
        func_name = self.current_token().lexeme
        func = Var(func_name)
        self.advance()
        self.consume(Token.LEFT_PAREN)
        argument = self.expression()
        self.consume(Token.RIGHT_PAREN)
        return FunctionCall(func, argument)
    
    def binding(self):
        var_name = self.current_token().lexeme
        self.advance()
        self.consume(Token.BINDING)
        value = self.expression()
        return Binding(var_name, value)
    
    def if_expr(self):
        self.consume(Token.IF)
        cond_expr = self.expression()
        self.consume(Token.THEN)
        then_expr = self.expression()
        self.consume(Token.ELSE)
        else_expr = self.expression()
        return IfExpr(cond_expr, then_expr, else_expr)
    
    def identifier(self):
        var = Var(self.current_token().lexeme)
        self.advance()
        return var
    
    def number(self):
        numeric_value = int(self.current_token().lexeme)
        self.advance()
        return Number(numeric_value)

    def binary_expr(self):
        lhs = self.term()

        while (not self.is_at_end()) and self.current_token().token_type in (Token.PLUS, Token.MINUS):
            op = self.current_token().lexeme
            self.advance()
            rhs = self.term()
            lhs = BinaryOp(lhs, op, rhs)

        return lhs

    def term(self):
        lhs = self.factor()

        while (not self.is_at_end()) and self.current_token().token_type in (Token.STAR, Token.SLASH, Token.GREATER_THAN):
            op = self.current_token().lexeme
            self.advance()
            rhs = self.factor()
            lhs = BinaryOp(lhs, op, rhs)

        return lhs

    def factor(self):
        token = self.current_token()

        if token.token_type == Token.NUMBER:
            self.consume(Token.NUMBER)
            if token.lexeme.find(".") != -1:
                return Number(float(token.lexeme))
            else:
                return Number(int(token.lexeme))

        if token.token_type == Token.IDENTIFIER:
            if self.index + 1 >= len(self.tokens):
                return self.identifier()
            elif self.lookahead().token_type == Token.LEFT_PAREN:
                return self.function_call()
            else:
                return self.identifier()

        if token.token_type == Token.LEFT_PAREN:
            self.consume(Token.LEFT_PAREN)
            expr = self.expression()
            self.consume(Token.RIGHT_PAREN)
            return expr

        if token.token_type == Token.END_LINE:
            self.advance()
            return None

        else:
            raise Exception(f"Unexpected token: '{token.lexeme}'")

    def call_or_var(self):
        name = self.consume(Token.IDENTIFIER).lexeme

        if self.current_token().lexeme == "(":
            self.consume(Token.LEFT_PAREN)
            arg = self.binary_expr()
            self.consume(Token.RIGHT_PAREN)
            return FunctionCall(Var(name), arg)

        return Var(name)


def main():
    source = (
        'sign := x |-> 1 if x > 0 else -1\n'
    )

    tokeniser = Tokeniser(source)
    tokeniser.tokenise()

    print([token.lexeme for token in tokeniser.tokens])
    
    parser = Parser(tokeniser.tokens)
    parser.parse()

    print(parser.ast)

if __name__ == "__main__":
    main()
