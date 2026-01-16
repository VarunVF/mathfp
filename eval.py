import math
import sys

from ast_nodes import *
from env import Env


# Built-in functions
def builtin_add(x, y): return x + y
def builtin_mul(x, y): return x * y
def builtin_sub(x, y): return x - y
def builtin_div(x, y): return x / y
def builtin_gt(x, y): return x > y
def builtin_if(cond, t, f): return t if cond else f

BUILTINS = {
    '+': builtin_add,
    '*': builtin_mul,
    '-': builtin_sub,
    '/': builtin_div,
    '>': builtin_gt,
    'if': builtin_if,

    'print': print,

    # Math functions
    "exp": math.exp,
    "ln": math.log,
    "sin": math.sin,
    "cos": math.cos,
}


class Evaluator(ASTVisitor):
    def visit_program(self, env: Env, node: Program):
        for node in node.exprs:
            env, result = node.accept(env, self)
        return env, result
    
    def visit_number(self, env: Env, node: Number):
        return env, node.value
    
    def visit_var(self, env, node):
        if node.name in env:
            return env, env[node.name]
        elif node.name in BUILTINS:
            return env, BUILTINS[node.name]
        else:
            print(f"[mfp] Unknown variable: {node.name}", file=sys.stderr)
            return env, None

    def visit_binding(self, env: Env, node: Binding):
        _, value = node.expr.accept(env, self)
        if node.name in env:
            print(f"[mfp] Redeclaration of variable: {node.name}", file=sys.stderr)
            return env, None
        return env.extend(node.name, value), None
    
    def visit_functiondef(self, env: Env, node: FunctionDef_):
        param = node.param
        body = node.body
        def func(param_value):
            local_env = env.extend(param, param_value)
            return body.accept(local_env, self)[1]
        return env, func
    
    def visit_functioncall(self, env: Env, node: FunctionCall):
        _, func = node.func.accept(env, self)
        _, arg = node.arg.accept(env, self)
        return env, func(arg)
    
    def visit_binaryop(self, env: Env, node: BinaryOp):
        _, left = node.left.accept(env, self)
        _, right = node.right.accept(env, self)
        op_func = BUILTINS[node.op]
        return env, op_func(left, right)
    
    def visit_ifexpr(self, env: Env, node: IfExpr):
        _, cond = node.cond.accept(env, self)
        _, t_val = node.then_expr.accept(env, self)
        _, f_val = node.else_expr.accept(env, self)
        return env, builtin_if(cond, t_val, f_val)


def main():
    ## Build AST
    # a := f -> f(0) / 2
    # b := x -> 3*x
    # a(b)

    exprs: list[ASTNode] = [
        Binding('a',
            FunctionDef_('f',
                BinaryOp( FunctionCall(Var('f'), Number(0)), '/', Number(2) )
            )
        ),
        Binding('b',
            FunctionDef_('x',
                BinaryOp( Number(3), '*', Var('x') )
            )
        ),
        FunctionCall( Var('a'), Var('b') ),
    ]
    visitor = Evaluator()
    env = Env()
    for expr in exprs:
        env, res = expr.accept(env, visitor)

    print(res)  # Should print 0


if __name__ == "__main__":
    main()
