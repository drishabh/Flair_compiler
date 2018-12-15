"""
    @author:       Rishabh Dalal
    @description:  LL1 parser for flair
    @since:        26 Sept. 2018

"""
from scanner import Scanner
from flr_token import Token, TokenType
import os

class NonTerminal:
    def __init__(self, val):
        self.val = val

    def getValue(self):
        return self.val

    def __eq__(self, obj):
        return self.val == obj.getValue()

    def __hash__(self):
        return hash(self.val)
    
class Stack:
    def __init__(self, termList):
        self.lst = []
        self.terminalList = termList

    def top(self):
        return self.lst.pop()

    def pop(self):
        self.lst.pop()

    def push(self, lst):
        for i in range(len(lst)-1,-1,-1):
            if i in self.terminalList:
                stack.append(Scanner(i).next())
            else:
                stack.append(NonTerminal(i.strip()))

    def size(self):
        return len(self.lst)

    def pushProper(self, obj):
        self.lst.append(obj)

class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.path = self.getPath()
        self.parseTable = {}
        self.terminalList = [""]
        self.createParseTable()
        self.stack = Stack(self.terminalList)
        self.prod = None
        #self.printParseTable()
            
    def getPath(self):
        path = os.getcwd()
        path = path.split("\\")
        path = "\\".join(path[:-1])
        path = path + "\doc\parsing_table.txt"
        return path
        
    def createParseTable(self):
        file = open(self.path, 'r')
        terminals = file.readline().split("|")
        for terminal in terminals:
            for junk in "\t \n":
                terminal = terminal.replace(junk, "")
            if terminal:
                self.terminalList.append(terminal)
        
        for line in file:
            if not line[0] == "-":
                line = line.split("|")
                prodRule = NonTerminal(line[0].strip())
                self.parseTable[prodRule] = {}
                for i in range(1, len(line)):
                    if line[i].strip():
                        term = Scanner(self.terminalList[i]).next()
                        #print("TYPE of term:", isinstance(term, Token))
                        data = line[i]
                        data = data.split()
                        cleanData = []
                        for j in data:
                            for junk in "\t \n":
                                j = j.replace(junk, "")
                            if j:
                                cleanData.append(j)
                        self.parseTable[prodRule][term] = cleanData
                        
    def parse(self):
        self.stack.pushProper(Token(TokenType.EOF))  
        self.stack.pushProper(NonTerminal("<PROGRAM>")) 
        
        while self.stack.size() > 0:
            A = self.stack.top()
            if isinstance(A, TokenType):
                t = self.scanner.next()
                if t.getValue() == A.getValue():
                    self.stack.pop()
                else:
                    msg = 'token mismatch: {} and {}'
                    raise ParseError(msg.format(A, t))
            elif isinstance(A, NonTerminal):
                t = self.scanner.peek()
                for j in self.parseTable[A]:
                    print(type(j))
                rule = self.parseTable[A][t]  ##error here
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
        
pr = "program countdown(number : integer); begin if number <= 1 \
	   then return 1 \
	   else return countdown(number-1) \
end"
sc = Scanner(pr)
p = Parser(sc)

