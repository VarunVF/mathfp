from env import Env


# Visitor interface
class ASTVisitor:
    def visit_number(self, env: Env, node: Number):
        pass

    def visit_var(self, env: Env, node: Var):
        pass

    def visit_binding(self, env: Env, node: Binding):
        pass

    def visit_functiondef(self, env: Env, node: FunctionDef_):
        pass

    def visit_functioncall(self, env: Env, node: FunctionCall):
        pass

    def visit_binaryop(self, env: Env, node: BinaryOp):
        pass

    def visit_ifexpr(self, env: Env, node: IfExpr):
        pass


# Element interface
class ASTNode:
    def accept(self, env: Env, visitor: ASTVisitor):
        pass


# AST nodes (call the specific visitor method)

class Number(ASTNode):
    def __init__(self, value: int | float):
        self.value = value

    def accept(self, env: Env, visitor: ASTVisitor):
        return visitor.visit_number(env, self)


class Var(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def accept(self, env: Env, visitor: ASTVisitor):
        return visitor.visit_var(env, self)


class Binding(ASTNode):
    def __init__(self, name: str, expr: ASTNode):
        self.name = name
        self.expr = expr

    def accept(self, env: Env, visitor: ASTVisitor):
        return visitor.visit_binding(env, self)


class FunctionDef_(ASTNode):
    def __init__(self, param: str, body: ASTNode):
        self.param = param
        self.body = body

    def accept(self, env: Env, visitor: ASTVisitor):
        return visitor.visit_functiondef(env, self)


class FunctionCall(ASTNode):
    def __init__(self, func: Var, arg: ASTNode):
        self.func = func
        self.arg = arg

    def accept(self, env: Env, visitor: ASTVisitor):
        return visitor.visit_functioncall(env, self)


class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, env: Env, visitor: ASTVisitor):
        return visitor.visit_binaryop(env, self)


class IfExpr(ASTNode):
    def __init__(self, cond: ASTNode, then_expr: ASTNode, else_expr: ASTNode):
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

    def accept(self, env: Env, visitor: ASTVisitor):
        return visitor.visit_ifexpr(env, self)
