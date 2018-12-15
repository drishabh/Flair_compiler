#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import sys
import os
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError, ParseError, SemanticError
from flr_parser import Parser
from type_checker import TypeChecker

try:
    filename = sys.argv[1]
    myfile   = open(filename)
    program  = myfile.read()
    scanner  = Scanner(program)
    parser   = Parser(scanner)
    ast = parser.parse()
    print("AST\n", ast, "\n\n\n")
    t_checker = TypeChecker(ast)
    t_checker.type_check()
    t_checker.pretty_print()

except LexicalError as le:
    print('Lexical error: ' + str(le))
except ParseError as pe:
    print('Parse error: ' + str(pe))
except SemanticError as se:
    print('Semantic error: ' + str(se))
except Exception as exc:
    print('Something went wrong: ' + str(exc))
