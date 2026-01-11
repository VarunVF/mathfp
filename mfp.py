import sys
import os

from tokeniser import Tokeniser
from parser import Parser
from eval import eval_expr, Env


def run_repl():
    print("MathFP REPL. Type 'exit' to quit.")
    env = Env()
    while True:
        line = input(">>> ")
        if line.strip() == "exit":
            break
        lexer = Tokeniser(line)
        lexer.tokenise()
        parser = Parser(lexer.tokens)
        parser.parse()
        if not lexer.had_error:
            for expr in parser.ast.exprs:
                env, result = eval_expr(expr, env)
                if result is not None:
                    print(result)


def print_usage():
    print("Usage: mfp.py MFP_SOURCE")
    print("    MFP_SOURCE: path to source file")


def run_file(filepath: str):
    if os.path.exists(filepath):
        with open(filepath) as f:
            source = f.read()
    else:
        print(f"No such file: {filepath}", file=sys.stderr)
        exit(1)

    lexer = Tokeniser(source)
    lexer.tokenise()
    parser = Parser(lexer.tokens)
    parser.parse()
    env = Env()
    if not lexer.had_error:
        for expr in parser.ast.exprs:
            env, result = eval_expr(expr, env)


def main():
    argc = len(sys.argv)

    if argc == 1:
        run_repl()
    elif argc == 2:
        run_file(sys.argv[1])
    else:
        print_usage()
        exit(1)


if __name__ == '__main__':
    main()
