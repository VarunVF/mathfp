# MathFP

A small functional, math-oriented language with immutable values and first-class functions.

## Features

- First-class and higher-order functions: Functions can accept and return functions
- Immutable values
- Recursion
- Lambdas
- Conditional expressions
- File inclusion using `!include` macro
- Math-focused syntax
- REPL for interactive use

## Example

Function definition syntax:
```mfp
f := x |-> 2*x*x + 3*x - 1
print( f(0) )  # -1
```

Conditionals:
```mfp
# Absolute value function
abs := x |-> if x > 0 then x else 0 - x
print( abs(6) )   # 6
print( abs(-5) )  # 5
```

Higher-order functions:
```mfp
# Checks if a function is positive at x
is_positive := f |-> x |-> if f(x) then 1 else 0

check_f := is_positive(f)

print( check_f(0) )
print( check_f(-1) )
print( check_f(2) )
```

See more in the `examples/` directory.
