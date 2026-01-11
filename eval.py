import math
import sys

from ast_nodes import *


# Environment: immutable dictionary mapping names -> values
class Env(dict):
    def extend(self, name, value):
        new_env = Env(self)
        new_env[name] = value
        return new_env


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

# Evaluator
def eval_expr(expr, env):
    if isinstance(expr, Number):
        return env, expr.value

    elif isinstance(expr, Var):
        if expr.name in env:
            return env, env[expr.name]
        elif expr.name in BUILTINS:
            return env, BUILTINS[expr.name]
        else:
            print(f"[mfp] Unknown variable: {expr.name}", file=sys.stderr)
            return env, None

    elif isinstance(expr, Binding):
        _, value = eval_expr(expr.expr, env)
        if expr.name in env:
            print(f"[mfp] Redeclaration of variable: {expr.name}", file=sys.stderr)
            return env, None
        return env.extend(expr.name, value), None

    elif isinstance(expr, FunctionDef_):
        param = expr.param
        body = expr.body
        def func(param_value):
            local_env = env.extend(param, param_value)
            return eval_expr(body, local_env)[1]
        return env, func

    elif isinstance(expr, FunctionCall):
        _, func = eval_expr(expr.func, env)
        _, arg = eval_expr(expr.arg, env)
        return env, func(arg)

    elif isinstance(expr, BinaryOp):
        _, left = eval_expr(expr.left, env)
        _, right = eval_expr(expr.right, env)
        op_func = BUILTINS[expr.op]
        return env, op_func(left, right)

    elif isinstance(expr, IfExpr):
        _, cond = eval_expr(expr.cond, env)
        _, t_val = eval_expr(expr.then_expr, env)
        _, f_val = eval_expr(expr.else_expr, env)
        return env, builtin_if(cond, t_val, f_val)

    else:
        raise Exception(f"Unknown expression type: {type(expr)}")


def main():
    # Build AST
    env = Env()

    # a := f -> f(0) / 2
    # b := x -> 3*x
    # a(b)

    env = eval_expr(
        Binding('a',
            FunctionDef_('f',
                BinaryOp( FunctionCall(Var('f'), Number(0)), '/', Number(2) )
            )
        ),
        env
    )

    env = eval_expr(
        Binding('b',
            FunctionDef_('x',
                BinaryOp( Number(3), '*', Var('x') )
            )
        ),
        env
    )

    result = eval_expr(
        FunctionCall( Var('a'), Var('b')),
        env
    )

    print("Result:", result)  # Should print 0


if __name__ == "__main__":
    main()
