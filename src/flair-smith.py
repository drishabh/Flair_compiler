from flr_stack import Stack
import random
from flr_token import TokenType
from flr_parser import NonTerminal

class Flair_Smith:
    def __init__(self):

        self.parse_table = {
            ( NonTerminal.PROGRAM , TokenType.PROGRAM ) : [TokenType.PROGRAM,TokenType.IDENTIFIER,TokenType.LEFT_PAREN,
                                                           NonTerminal.FORMALS,TokenType.RIGHT_PAREN,
                                                           TokenType.SEMI_COLON,NonTerminal.DEFINITIONS, NonTerminal.BODY,TokenType.PERIOD],
            ( NonTerminal.DEFINITIONS  , TokenType.FUNCTION ) : [NonTerminal.DEF, NonTerminal.DEFINITIONS ],
            ( NonTerminal.DEFINITIONS  , TokenType.BEGIN ) : ["epsilon"],
            ( NonTerminal.DEF , TokenType.FUNCTION ) : [TokenType.FUNCTION,TokenType.IDENTIFIER,TokenType.LEFT_PAREN,NonTerminal.FORMALS,TokenType.RIGHT_PAREN,TokenType.COLON,NonTerminal.TYPE
                                                        ,NonTerminal.BODY,TokenType.SEMI_COLON],
            ( NonTerminal.FORMALS , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.FORMALS , TokenType.IDENTIFIER ) : [NonTerminal.NONEMPTYFORMALS],
            ( NonTerminal.NONEMPTYFORMALS , TokenType.IDENTIFIER ) : [NonTerminal.FORMAL,NonTerminal.NONEMPTY_F_REST],
            ( NonTerminal.NONEMPTY_F_REST , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.NONEMPTY_F_REST , TokenType.COMMA ) : [TokenType.COMMA,NonTerminal.FORMAL,NonTerminal.NONEMPTY_F_REST],
            ( NonTerminal.FORMAL , TokenType.IDENTIFIER ) : [TokenType.IDENTIFIER,TokenType.COLON,NonTerminal.TYPE],
            ( NonTerminal.BODY , TokenType.BEGIN ) : [TokenType.BEGIN,NonTerminal.STATEMENT_LIST, TokenType.END],
            ( NonTerminal.STATEMENT_LIST , TokenType.RETURN ) : [TokenType.RETURN,NonTerminal.EXPR],
            ( NonTerminal.STATEMENT_LIST , TokenType.PRINT ) : [NonTerminal.PRINT_STATEMENT,NonTerminal.STATEMENT_LIST],
            ( NonTerminal.TYPE , TokenType.INTEGER ) : [TokenType.INTEGER],
            ( NonTerminal.TYPE , TokenType.BOOLEANLITERAL ) : [TokenType.BOOLEANLITERAL],
            ( NonTerminal.EXPR , TokenType.LEFT_PAREN ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.EXPR , TokenType.IDENTIFIER ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.EXPR , TokenType.NUMBER ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.EXPR , TokenType.TRUE ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.EXPR , TokenType.FALSE ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.EXPR , TokenType.NOT ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.EXPR , TokenType.IF ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.EXPR , TokenType.SUBTRACT ) : [NonTerminal.SIMPLE_EXPR,NonTerminal.E_TAIL],
            ( NonTerminal.E_TAIL , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.EQUAL ) : [TokenType.EQUAL,NonTerminal.SIMPLE_EXPR, NonTerminal.E_TAIL],
            ( NonTerminal.E_TAIL , TokenType.LESSTHAN ) : [TokenType.LESSTHAN, NonTerminal.SIMPLE_EXPR, NonTerminal.E_TAIL],
            ( NonTerminal.E_TAIL , TokenType.MULTIPLY ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.DIVIDE ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.ADD ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.AND ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.END ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.SUBTRACT ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.OR ) : ["epsilon"],
            ( NonTerminal.E_TAIL , TokenType.COMMA ) : ["epsilon"],
            ( NonTerminal.SIMPLE_EXPR , TokenType.LEFT_PAREN ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.IDENTIFIER ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.NUMBER ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.TRUE ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.FALSE ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.NOT ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.IF ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SIMPLE_EXPR , TokenType.SUBTRACT ) : [NonTerminal.TERM,NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.EQUAL ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.LESSTHAN ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.MULTIPLY ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.DIVIDE ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.ADD ) : [TokenType.ADD,NonTerminal.TERM, NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.AND ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.END ) : ["epsilon"],
            ( NonTerminal.SE_TAIL , TokenType.SUBTRACT ) : [TokenType.SUBTRACT,NonTerminal.TERM, NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.OR ) : [TokenType.OR, NonTerminal.TERM, NonTerminal.SE_TAIL],
            ( NonTerminal.SE_TAIL , TokenType.COMMA ) : ["epsilon"],
            ( NonTerminal.TERM , TokenType.LEFT_PAREN ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.IDENTIFIER ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.NUMBER ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.TRUE ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.FALSE ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.NOT ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.IF ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.TERM , TokenType.SUBTRACT ) : [NonTerminal.FACTOR,NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.EQUAL ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.OR ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.LESSTHAN ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.MULTIPLY ) : [TokenType.MULTIPLY,NonTerminal.FACTOR, NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.DIVIDE ) : [TokenType.DIVIDE,NonTerminal.FACTOR, NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.ADD ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.AND ) : [TokenType.AND,NonTerminal.FACTOR, NonTerminal.T_TAIL],
            ( NonTerminal.T_TAIL , TokenType.END ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.SUBTRACT ) : ["epsilon"],
            ( NonTerminal.T_TAIL , TokenType.COMMA ) : ["epsilon"],
            ###( NonTerminal.FACTOR , TokenType.LEFT_PAREN ) : [TokenType.LEFT_PAREN,NonTerminal.EXPR,TokenType.RIGHT_PAREN, AstAction.MakeNestedExpr],
            ( NonTerminal.FACTOR , TokenType.LEFT_PAREN ) : [TokenType.LEFT_PAREN,NonTerminal.EXPR,TokenType.RIGHT_PAREN],
            ( NonTerminal.FACTOR , TokenType.IDENTIFIER ) : [NonTerminal.ID],
            ( NonTerminal.FACTOR , TokenType.NUMBER ) : [NonTerminal.LITERAL],
            ( NonTerminal.FACTOR , TokenType.TRUE ) : [NonTerminal.LITERAL],
            ( NonTerminal.FACTOR , TokenType.FALSE ) : [NonTerminal.LITERAL],
            ( NonTerminal.FACTOR , TokenType.NOT ) : [TokenType.NOT,NonTerminal.FACTOR],
            ( NonTerminal.FACTOR , TokenType.IF ) : [TokenType.IF,NonTerminal.EXPR,TokenType.THEN,NonTerminal.EXPR,TokenType.ELSE,NonTerminal.EXPR],
            ( NonTerminal.FACTOR , TokenType.SUBTRACT ) : [TokenType.SUBTRACT,NonTerminal.FACTOR],
            ( NonTerminal.ID , TokenType.IDENTIFIER ) : [TokenType.IDENTIFIER,NonTerminal.ID_REST],
            ( NonTerminal.ID_REST , TokenType.LEFT_PAREN ) : [TokenType.LEFT_PAREN,NonTerminal.ACTUALS,TokenType.RIGHT_PAREN],
            ( NonTerminal.ID_REST , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.EQUAL ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.LESSTHAN ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.MULTIPLY ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.DIVIDE ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.ADD ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.ELSE ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.THEN ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.END ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.SUBTRACT ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.OR ) : ["epsilon"],
            ( NonTerminal.ID_REST , TokenType.COMMA ) : ["epsilon"],
            ( NonTerminal.ACTUALS , TokenType.LEFT_PAREN ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.ACTUALS , TokenType.IDENTIFIER ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.NUMBER ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.TRUE ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.FALSE ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.NOT ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.IF ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.ACTUALS , TokenType.SUBTRACT ) : [NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.LEFT_PAREN ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.IDENTIFIER ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.NUMBER ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.TRUE ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.FALSE ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.NOT ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.IF ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTYACTUALS , TokenType.SUBTRACT ) : [NonTerminal.EXPR,NonTerminal.NONEMPTY_A_REST],
            ( NonTerminal.NONEMPTY_A_REST , TokenType.RIGHT_PAREN ) : ["epsilon"],
            ( NonTerminal.NONEMPTY_A_REST , TokenType.COMMA ) : [TokenType.COMMA,NonTerminal.NONEMPTYACTUALS],
            ( NonTerminal.LITERAL , TokenType.NUMBER ) : [TokenType.NUMBER],
            ( NonTerminal.LITERAL , TokenType.TRUE ) : [TokenType.TRUE],
            ( NonTerminal.LITERAL , TokenType.FALSE ) : [TokenType.FALSE],
            ( NonTerminal.PRINT_STATEMENT , TokenType.PRINT ) : [TokenType.PRINT,TokenType.LEFT_PAREN,NonTerminal.EXPR,TokenType.RIGHT_PAREN,
                                                                 TokenType.SEMI_COLON]
        }
        
        self.parse_helper = {
            NonTerminal.PROGRAM         : [TokenType.PROGRAM],
            NonTerminal.DEFINITIONS     : [TokenType.FUNCTION, TokenType.BEGIN],
            NonTerminal.DEF             : [TokenType.FUNCTION],
            ##NonTerminal.FORMALS         : [TokenType.RIGHT_PAREN, TokenType.IDENTIFIER],
            NonTerminal.FORMALS         : [TokenType.RIGHT_PAREN],
            NonTerminal.NONEMPTYFORMALS : [TokenType.IDENTIFIER],
            NonTerminal.NONEMPTY_F_REST : [TokenType.RIGHT_PAREN,  TokenType.COMMA],
            NonTerminal.FORMAL          : [TokenType.IDENTIFIER],
            NonTerminal.BODY            : [TokenType.BEGIN],
            NonTerminal.STATEMENT_LIST  : [TokenType.RETURN, TokenType.PRINT],
            NonTerminal.TYPE            : [TokenType.INTEGER, TokenType.BOOLEANLITERAL],
            NonTerminal.EXPR            : [TokenType.LEFT_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                           TokenType.TRUE, TokenType.FALSE, TokenType.NOT, TokenType.IF,
                                           TokenType.SUBTRACT],
            NonTerminal.E_TAIL          : [TokenType.RIGHT_PAREN, TokenType.EQUAL, TokenType.LESSTHAN,
                                           TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.ADD,
                                           TokenType.ELSE, TokenType.THEN, TokenType.AND, TokenType.END,
                                           TokenType.SUBTRACT, TokenType.OR, TokenType.COMMA],
            NonTerminal.SIMPLE_EXPR     : [TokenType.LEFT_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                           TokenType.TRUE, TokenType.FALSE, TokenType.NOT, TokenType.IF,
                                           TokenType.SUBTRACT],
            NonTerminal.SE_TAIL         : [TokenType.RIGHT_PAREN, TokenType.EQUAL, TokenType.LESSTHAN,
                                           TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.ADD, TokenType.ELSE,
                                           TokenType.THEN, TokenType.AND, TokenType.END, TokenType.SUBTRACT,
                                           TokenType.OR, TokenType.COMMA],
            NonTerminal.TERM            : [TokenType.LEFT_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                           TokenType.TRUE, TokenType.FALSE, TokenType.NOT, TokenType.IF,
                                           TokenType.SUBTRACT],
            NonTerminal.T_TAIL          : [TokenType.RIGHT_PAREN, TokenType.EQUAL, TokenType.OR,
                                           TokenType.LESSTHAN, TokenType.MULTIPLY, TokenType.DIVIDE,
                                           TokenType.ADD, TokenType.ELSE, TokenType.THEN, TokenType.AND,
                                           TokenType.END, TokenType.SUBTRACT, TokenType.COMMA],
            NonTerminal.FACTOR          : [TokenType.LEFT_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                           TokenType.TRUE, TokenType.FALSE, TokenType.NOT, TokenType.IF,
                                           TokenType.SUBTRACT],
            NonTerminal.ID              : [TokenType.IDENTIFIER],
            NonTerminal.ID_REST         : [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN, TokenType.EQUAL,
                                           TokenType.LESSTHAN, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.ADD,
                                           TokenType.ELSE, TokenType.THEN, TokenType.END, TokenType.SUBTRACT,
                                           TokenType.OR, TokenType.COMMA],
            NonTerminal.ACTUALS         : [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN, TokenType.IDENTIFIER,
                                           TokenType.NUMBER, TokenType.TRUE,TokenType.FALSE, TokenType.NOT,
                                           TokenType.IF, TokenType.SUBTRACT],
            NonTerminal.NONEMPTYACTUALS : [TokenType.LEFT_PAREN, TokenType.IDENTIFIER, TokenType.NUMBER,
                                           TokenType.TRUE, TokenType.FALSE, TokenType.NOT, TokenType.IF,
                                           TokenType.SUBTRACT],
            NonTerminal.NONEMPTY_A_REST : [TokenType.RIGHT_PAREN, TokenType.COMMA],
            NonTerminal.LITERAL         : [TokenType.NUMBER, TokenType.TRUE, TokenType.FALSE],
            NonTerminal.PRINT_STATEMENT : [TokenType.PRINT]
        }


    def generate(self):
        stack = Stack()
        program = []
        stack.pushProper(NonTerminal.PROGRAM)

        while stack.size() != 0:
            curr = stack.pop()
            if not curr == ['epsilon']:
                if isinstance(curr, TokenType):
                    program.append(curr)
                elif isinstance(curr, NonTerminal):
                   rand_number = self.get_random_helper(curr)
                   token = self.parse_helper[curr][rand_number]

                   unit = self.parse_table[(curr, token)]

                   stack.pushRule(unit)
                else:
                   print("Dont know how to handle", curr)
            #if len(program) > 20:
            #    break
            #print("STACK", stack)
        return self.postprocess(program)

    def postprocess(self, i):
        ans = []
        for lst in i:
            print("LST", lst)
            if lst == TokenType.IDENTIFIER:
                ans.append('identifier')
            elif lst == TokenType.LEFT_PAREN:
                ans.append('(')
            elif lst == TokenType.COLON:
                ans.append(':')

            elif lst == TokenType.COMMA:
                ans.append(',')
            elif lst == TokenType.RIGHT_PAREN:
                ans.append(')')

            elif lst == TokenType.SEMI_COLON:
                ans.append(';')
            elif lst == TokenType.NUMBER:
                ans.append(random.randint(0, (2**32) - 1))

            elif lst == TokenType.BOOLEANLITERAL:
                ans.append(['true', 'false'][random.randint(0,1)])
                           
            elif lst == TokenType.PERIOD:
                ans.append('.')

            elif lst == TokenType.INTEGER:
                ans.append('integer')
            elif lst == TokenType.TRUE:
                ans.append('true')

            elif lst == TokenType.FALSE:
                ans.append('false')
            elif lst == TokenType.IF:
                ans.append('if')

            elif lst == TokenType.THEN:
                ans.append('then')
            elif lst == TokenType.ELSE:
                ans.append('else')

            elif lst == TokenType.NOT:
                ans.append('not')
            elif lst == TokenType.OR:
                ans.append('or')


            elif lst == TokenType.AND:
                ans.append('and')
            elif lst == TokenType.PRINT:
                ans.append('print')

            elif lst == TokenType.PROGRAM:
                ans.append('program')
            elif lst == TokenType.FUNCTION:
                ans.append('function')

            elif lst == TokenType.RETURN:
                ans.append('return')
            elif lst == TokenType.BEGIN:
                ans.append('begin')

            elif lst == TokenType.END:
                ans.append('end')
            elif lst == TokenType.ADD:
                ans.append('+')

            elif lst == TokenType.SUBTRACT:
                ans.append('-')
            elif lst == TokenType.DIVIDE:
                ans.append('/')

            elif lst == TokenType.MULTIPLY:
                ans.append('*')
            elif lst == TokenType.EQUAL:
                ans.append('=')
            elif lst == TokenType.LESSTHAN:
                ans.append('<')
            else:
                ans.append(lst)
        return ans
                           
            

    def get_random_helper(self, val):
        length =  len(self.parse_helper[val])
        return random.randint(0, length-1)

smith = Flair_Smith()
pr = smith.generate()
for i in pr:
    print(i)
