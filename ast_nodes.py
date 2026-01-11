# AST nodes
class Number:
    def __init__(self, value: int | float):
        self.value = value


class Var:
    def __init__(self, name: str):
        self.name = name


class Binding:
    def __init__(self, name: str, expr):
        self.name = name
        self.expr = expr


class FunctionDef_:
    def __init__(self, param: str, body):
        self.param = param
        self.body = body


class FunctionCall:
    def __init__(self, func: Var, arg):
        self.func = func
        self.arg = arg


class BinaryOp:
    def __init__(self, left, op: str, right):
        self.left = left
        self.op = op
        self.right = right


class IfExpr:
    def __init__(self, cond, then_expr, else_expr):
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr
