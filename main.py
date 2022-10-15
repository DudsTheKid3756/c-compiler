from parse import *
from emit import *

if __name__ == '__main__':
    print("To 'C' Compiler!")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as input_file:
        _input = input_file.read()

    lexer = Lexer(_input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.write_file()
    print("Parsing completed.")
