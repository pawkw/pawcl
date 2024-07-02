from TokenBuffer import TokenBuffer as tb
from tokenizer import Token
import sys

def display_help(program_name):
    indent = '    '
    print()
    print('Usage:')
    print('{program_name} <input file(s)> <options>')
    print('Options:')
    print(f'{indent}-? --help: This help display.')
    print(f'{indent}-o output_file: The default name is out.s. Use this option\n{indent}{indent}to change that.')
    print(f'{indent}-v: Verbose. This will display every token processed\n{indent}{indent}and all assembler lines emitted.')
    print(f'{indent}-t: Terse. Do not display any messages.')
    print(f'{indent}-- or -stdout: Output the resulting program to stdout instead\n{indent}{indent}of a file. This automatically turns on terse mode.')
    print()


def main(assembly_program: list, input_files: list, output_file: str, verbose: bool, stdin: bool, stdout: bool):
    patterns = {
        "INTEGER": r"\d+",
        "OPERATOR": r"[\+\-\*\/\(\)]"
    }
    buffer = tb.TokenBuffer()

    if input_files:
        buffer.load_files(input_files)
        
    if stdin:
        program_lines = []
        for line in sys.stdin:
            program_lines.append(line)
        buffer.add_lines('stdin', program_lines)
   

    buffer.init_patterns(patterns)
    buffer.config(skip_white_space = True, skip_EOF = False, skip_EOL = False)
    buffer.tokenize()

    while not buffer.out_of_tokens():
        parse_expression(buffer, assembly_program, verbose)

    with sys.stdout if stdout else open(output_file, 'w') as file:
        for line in program:
            file.write(line+'\n')

    return buffer.line


if __name__ == '__main__':
    if len(sys.argv) < 2:
        display_help(sys.argv[0])
        exit(0)
    get_output_file = False
    verbose = False
    terse = False
    output_file = 'out.s'
    input_files = []
    program = []
    for arg in sys.argv[1:]:
        if arg[0] == '-':
            match arg[1:]:
                case 'o':
                    get_output_file = True
                case 'v':
                    verbose = True
                case '?' | '-help':
                    display_help(sys.argv[0])
                    exit(0)
                case 't':
                    terse = True
                case 'stdout' | '-':
                    stdout = True
                    terse = True
                case 'stdin':
                    stdin = True
        else:
            if get_output_file:
                output_file = arg
                get_output_file = False
            else:
                input_files.append(arg)

    result = main(program, input_files, output_file, verbose, stdin, stdout)

    if not terse:
        print(f'Successfully compiled {result} lines to "{output_file}".')