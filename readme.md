# PAWCL

expression:
    | expression '+' term
    | expression '-' term
    | term

term:
    | term '*' factor
    | term '/' factor
    | factor

factor:
    | '(' expression ')'
    | atom

atom:
    | identifier
    | numeric_literal
