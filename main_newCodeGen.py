#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import sys
import os
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError, ParseError, SemanticError
from flr_parser import Parser
from type_checker import TypeChecker
from codeGen import CodeGenerator

try:
    filename = sys.argv[1]
    if not '.flr' in filename:
        filename += '.flr'
    myfile   = open(filename)
    program  = myfile.read()

    scanner  = Scanner(program)
    parser   = Parser(scanner)
    ast = parser.parse()
    t_checker = TypeChecker(ast)
    t_checker.type_check()
    err = t_checker.returnErrors()

    if len(err) > 0:
        print("Errors:")
        for i in err:
            print(i)
        print("The file does not contain a legal program.")
        
    else:
        t_checker.postprocess()
        print("Compiling...")
        c = CodeGenerator(ast, t_checker.get_symbol_table(), t_checker.get_symbol_table())
        c.generate()

except LexicalError as le:
    print('Lexical error: ' + str(le))
except ParseError as pe:
    print('Parse error: ' + str(pe))
except SemanticError as se:
    print('Semantic error: ' + str(se))
except Exception as exc:
    print('Something went wrong: ' + str(exc))
