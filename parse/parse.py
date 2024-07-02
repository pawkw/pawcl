from TokenBuffer import TokenBuffer, Token
from parseexpression import parse_expression

def parse(tokens: TokenBuffer, program: list[str], verbose: bool):
    parse_expression(tokens, program, verbose)
    return