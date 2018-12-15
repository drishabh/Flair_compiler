#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

import sys
import os
from flr_token import Token, TokenType
from scanner import Scanner
from error import LexicalError, ParseError, SemanticError, FileNotFound
from flr_parser import Parser
from type_checker import TypeChecker
from codeGen import CodeGenerator
from preprocess import Preprocess


try:
    main_program = None
    filename = sys.argv[1]
    ast_trees = []
    imports = []
    
    while True:

        if not '.flr' in filename:
            filename += '.flr'
        print('filename', filename)
        try:
            myfile   = open(filename)
        except:
            raise FileNotFound('Invalid import. File does not exist.')
        program  = myfile.read()
        handle_imports = Preprocess(program)
        program, impt = handle_imports.process()

        for i in impt:
            imports.append(i)
            
        if not main_program:
            main_program = program

        scanner  = Scanner(program)
        parser   = Parser(scanner)
        ast = parser.parse()
        ast_trees.append(ast)

        if len(imports) <= 0:
            break

        print('improts', imports)
        filename = filename.split('/')
        filename[-1] = imports.pop(0)
        filename = '/'.join(filename)
        
    ast = Preprocess('').combine_ast(ast_trees)

    #print("FINAL AST")
    #print('='*20)
    
    t_checker = TypeChecker(ast)
    t_checker.type_check()

    #print(ast)
    err = t_checker.returnErrors()

    if len(err) > 0:
        print("Errors:")
        for i in err:
            print(i)
        print("The file does not contain a legal program.")

    else:
        t_checker.postprocess()
        #t_checker.pretty_print()
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
