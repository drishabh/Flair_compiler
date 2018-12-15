from flr_ast import *

class Preprocess:
    def __init__(self, string):
        self.program = string

    def process(self):
        string = self.program
        string = string.split(';')
        imports = []
        program = ''
        for i in range(len(string)):
            j = string[i].split()
            if j[0] == 'include':
                if len(j) > 2:
                    raise ImportError('Import statement:', ''.join(j) + ';', \
                                      'incorrect')
                else:
                    imports.append(j[1])
            elif j[0] == 'program':
                program = ';'.join(string[i:])
                print("Returning imports", imports)
                print("Returning program", program)
                return  program, imports

    def combine_ast(self, lst):
        if len(lst) == 0:
            raise ValueError('Something went wrong')
        elif len(lst) == 1:
            return lst[0]
        else:
            main_ast = lst[0]
            for i in lst[1:]:
                definitions = i.definitions().value()
                for j in definitions:
                    main_ast.addDefinition(j)
                print(1)
                fn_name = i.identifier()
                formals = i.formals()
                type = '_none'
                body = i.body()
                def_node = Definition_Node(fn_name, formals, type, body)
                main_ast.addDefinition(def_node)
            return main_ast
