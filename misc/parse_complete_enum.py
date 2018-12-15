"""
    @author:       Rishabh Dalal
    @description:  LL1 parser for flair
    @since:        26 Sept. 2018

"""
from scanner import Scanner
from flr_token import Token, TokenType
import os
from enum import Enum
from error import ParseError

class NonTerminal(Enum):
    PROGRAM              =  0
    DEFINITIONS          =  1
    DEF                  =  2
    FORMALS              =  3
    NONEMPTYFORMALS      =  4
    NONEMPTY_F_REST      =  5
    FORMAL               =  6
    BODY                 =  7
    STATEMENT_LIST       =  8
    TYPE                 =  9
    EXPR                 =  10
    E_TAIL               =  11
    SIMPLE_EXPR          =  12
    SE_TAIL              =  13
    TERM                 =  14
    T_TAIL               =  15
    FACTOR               =  16
    ID                   =  17
    ID_REST              =  18
    ACTUALS              =  19
    NONEMPTYACTUALS      =  20
    NONEMPTY_A_REST      =  21
    LITERAL              =  22
    PRINT_STATEMENT      =  23
    
class Stack:
    def __init__(self, termList):
        self.lst = []
        self.terminalList = termList
        #print("TERMLIST")
        #print(self.terminalList)

    def top(self):
        if len(self.lst) <= 0:
            raise ValueError("Popping from empty stack")
        return self.lst[-1]

    def pop(self):
        if len(self.lst) <= 0:
            raise ValueError("Popping from empty stack")
        self.lst.pop()

    def pushRule(self, lst):
        for i in range(len(lst)-1,-1,-1):
            if lst[i] != "epsilon":
                if lst[i] in self.terminalList:
                    if lst[i] == "<IDENTIFIER>":
                        self.lst.append(TokenType.IDENTIFIER)
                    elif lst[i] == "<NUMBER>":
                        self.lst.append(TokenType.NUMBER)
                    elif lst[i] == "<BOOLEAN>":
                        self.lst.append(TokenType.KEYWORD)
                    else:
                        terminal = Scanner(lst[i]).next()
                        self.lst.append(terminal.getTokenType())
                else:
                    self.lst.append(getProdRule(lst[i]))

    def size(self):
        return len(self.lst)

    def pushProper(self, obj):
        self.lst.append(obj)

    def __str__(self):
        output = "\nStack:\n"
        for i in self.lst:
            output += str(i) + "\n"
        return output

class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.path = self.getPath()
        self.parseTable = {}
        self.terminalList = ["(", "(", ")", "=", "<IDENTIFIER>", "return", \
                             "<NUMBER>", "<", "*", "/", "function", "begin", \
                             "integer", "+", "else", "boolean", "then", ";", \
                             "<BOOLEAN>", "and", "end", "not", "$", "print", \
                             "if", "e", "-", ".", "or", "program", ",", ":"]
        ##^^ contains "(" twice since index start at 1.
        self.createParseTable()
        self.stack = Stack(self.terminalList)
    
    def getPath(self):
        ##Getting path of the grammar file to create the parse table
        
        path = os.getcwd()
        path = path.split("\\")
        path = "\\".join(path[:-1])
        path = path + "\doc\parsing_table.txt"
        return path
        
    def createParseTable(self):
        ##create parse table from the parsingTable.txt file
        
        file = open(self.path, 'r')
        terminals = file.readline().split("|")
        for terminal in terminals:
            ##Removing whitespace from the terminals
            for junk in "\t \n":
                terminal = terminal.replace(junk, "")
            if terminal:
                self.terminalList.append(terminal)
        
        for line in file:
            if not line[0] == "-":
                line = line.split("|")
                prodRule = getProdRule(line[0].strip())
                print("prodRULE", prodRule)
                for i in range(1, len(line)):
                    
                    if line[i].strip():
                        curr = self.terminalList[i]
                        if curr == "<IDENTIFIER>":
                            term = TokenType.IDENTIFIER
                        elif curr == "<NUMBER>":
                            term = (TokenType.NUMBER)
                        elif curr == "<BOOLEAN>":
                            term = (TokenType.KEYWORD)
                        else:
                            term = Scanner(curr).next().getTokenType()

                        data = line[i]
                        data = data.split()
                        cleanData = []
                        for j in data:
                            for junk in "\t \n":
                                j = j.replace(junk, "")
                            if j:
                                cleanData.append(j)
                        self.parseTable[(prodRule, term)] = cleanData
        file.close()
        
        
    def parse(self):
        ##LL1 parser for Flair
        
        self.stack.pushProper(TokenType.EOF)  
        self.stack.pushProper(NonTerminal.PROGRAM)
        
        while self.stack.size() > 0:
            print(self.stack)
            A = self.stack.top()
            #print("A", A)
            
            if isinstance(A, TokenType): 
                t = self.scanner.next().getTokenType()
                #print("AT:", A, t)                
                print((A,t))
                if t == A:
                    self.stack.pop()
                else:
                    msg = 'token mismatch: {} and {}'
                    raise ParseError(msg.format(A, t))
                
            elif isinstance(A, NonTerminal):
                t = self.scanner.peek().getTokenType()
                tup = (A, t)
                print(tup)
                rule = self.parseTable[tup]  #errorere
                print("RULE", rule)
                if rule:
                    self.stack.pop()
                    self.stack.pushRule(rule)
                    
                else:
                    msg = 'cannot expand {} on stack: {}'
                    raise ParseError(msg.format(A, t))
                
            else:
                msg = 'invalid item on stack: {}'
                raise ParseError(msg.format(A))

        if not t.isEOF():
            msg = 'unexpected token at end: {}'
            raise ParseError(msg.format(t))
        return True

    def getParseTable(self):
        return self.parseTable

def getProdRule(string):
    #print("PROD RULE:", string)
    if string == "<PROGRAM>":
        return NonTerminal.PROGRAM
    
    elif string == "<DEFINITIONS>":
        return NonTerminal.DEFINITIONS
    
    elif string == "<DEF>":
        return NonTerminal.DEF

    elif string == "<FORMALS>":
        return NonTerminal.FORMALS

    elif string == "<NONEMPTYFORMALS>":
        return NonTerminal.NONEMPTYFORMALS

    elif string == "<NONEMPTY-F-REST>":
        return NonTerminal.NONEMPTY_F_REST

    elif string == "<FORMAL>":
        return NonTerminal.FORMAL

    elif string == "<BODY>":
        return NonTerminal.BODY

    elif string == "<STATEMENT-LIST>":
        return NonTerminal.STATEMENT_LIST

    elif string == "<TYPE>":
        return NonTerminal.TYPE

    elif string == "<EXPR>":
        return NonTerminal.EXPR

    elif string == "<E-TAIL>":
        return NonTerminal.E_TAIL

    elif string == "<SIMPLE-EXPR>":
        return NonTerminal.SIMPLE_EXPR

    elif string == "<SE-TAIL>":
        return NonTerminal.SE_TAIL

    elif string == "<TERM>":
        return NonTerminal.TERM

    elif string == "<T-TAIL>":
        return NonTerminal.T_TAIL

    elif string == "<FACTOR>":
        return NonTerminal.FACTOR

    elif string == "<ID>":
        return NonTerminal.ID

    elif string == "<ID-REST>":
        return NonTerminal.ID_REST

    elif string == "<ACTUALS>":
        return NonTerminal.ACTUALS

    elif string == "<NONEMPTYACTUALS>":
        return NonTerminal.NONEMPTYACTUALS

    elif string == "<NONEMPTY-A-REST>":
        return NonTerminal.NONEMPTY_A_REST

    elif string == "<LITERAL>":
        return NonTerminal.LITERAL

    elif string == "<PRINT-STATEMENT>":
        return NonTerminal.PRINT_STATEMENT
        
pr = "program is_special( n : integer ); \
  function count(bit : integer, n : integer) : integer \
  begin \
    return 0         { TODO } \
  end; \
  function divides(x : integer, n : integer) : boolean \
  begin \
    return false     { TODO } \
  end; \
  function apply_definition(binary_n : integer) : boolean \
  begin \
    return divides(count(1, binary_n), n) \
       and divides(count(0, binary_n), n) \
  end; \
  function to_binary(n : integer) : integer \
  begin \
    return n         { TODO } \
  end; \
begin \
  return apply_definition(to_binary(n)) \
end." 
sc = Scanner(pr)
p = Parser(sc)
p.parse()
