"""
    @author         :  Phu Vijaranakorn, Sai Herng, Rishabh Dalal
    @description    :  Scanner for language Flair
    @since          :  12 Sept. 2018
 
"""

from enum import Enum
from flr_token import Token, TokenType
from error import LexicalError
from collections import OrderedDict
import string

RESERVED_WORDS = ["program", "function", "begin", "end", "print", "or", \
                  "and", "if", "then", "else", "not", "return", "integer", "boolean",\
                  "true", "false"]
ARITHMETIC_OPR = "<=*/-+"
COMMENT = ["{", "}"]
PUNCT = "().,;:<=*/-+"

HIGH_RANGE = (2**32) - 1
IDENTIFIER_LIMIT = 256

class State(Enum):
    looking    = 1
    number     = 2
    string     = 3
    comment    = 4
    zero       = 5
    punct      = 6
    error      = 7

class Scanner:
    def __init__(self, programStr):
        self.programStr  = programStr
        self.index       = 0
        self.linenumber  = 1
        self.length      = len(self.programStr)
        self.char_sums   = 1
        self.state       = State.looking
        self.accum       = ""
        self.peektoken   = None
        self.map         = self.initializeTable()

    ##----------------------PUBLIC---------------------------
        
    def peek(self):
        ##for peeking a token
        
        if not self.peektoken:
            self.peektoken = self.get_next_token()
        return self.peektoken


    def next_token(self):
        ## for returning the next token
        
        if self.peektoken:
            token = self.peektoken
            self.peektoken = None

            return token 
        else:

            return self.get_next_token()

    ##------------PRIVATE-------------------------------------
        
    def get_next_token(self):
        ##getting the next token to return
        
        self.accum = ''
        while self.index < self.length:
            ch = self.programStr[self.index]

            if self.is_whitespace(ch):
                self.state = State.looking
                self.index += 1

            print("Setting state:", self.map[ch][self.state])
            self.state = self.map[ch][self.state]
            if self.state == State.string:
                if ch.isalpha() or ch.isdigit() or ch == "_":
                    self.accum += ch
                    self.index += 1
                else:
                    return self.handleStringState()
                
        if self.accum:
            if self.state == State.number:
                number, self.accum = self.accum, ""
                return self.handleNumber(number)                
            elif self.state == State.string:
                string, self.accum = self.accum, ""
                return self.handleString(string)
            else:
                msg = "Invalid state at position {}, line {}.  How did that happen?".format(self.index%self.char_sums, self.linenumber)
                raise LexicalError(msg)
        return Token(TokenType.EOF)
            
    def is_whitespace(self, ch):
        ##Checking to see if a character is considered whitespace
        
        if '\n' in ch:
            self.linenumber += 1
            self.char_sums = self.index
        return ch in "\n\t\r "

    def is_arith_op(self, ch):
        ##checking to see if a character is considered an arithmetic opr
        
        return ch in ARITHMETIC_OPR

    def handleComment(self):
        ch = self.programStr[self.index]
        while ch != "}":
            self.index += 1
        self.index += 1
        self.state = State.looking
        
    def handleString(self, string):
        ##Returning appropriate string token
        
        if string in RESERVED_WORDS:
            return Token(TokenType.KEYWORD, string)
        
        if len(string) > IDENTIFIER_LIMIT:
            msg = "Maximum identifier length surpassed in line {}".format(string, self.linenumber)
            raise LexicalError(msg)
        return Token(TokenType.IDENTIFIER, string)

    def handleNumber(self, number):
        ##Handling number edge cases
        
        print("2")
        number = int(number)
        if number <= HIGH_RANGE:
            return Token(TokenType.NUMBER, int(number))
        else:
            msg = "Integer {} out of bounds in line {}".format(number, self.linenumber)
            raise LexicalError(msg)

    def handleInitialState(self, ch):
        ##Taking care of initial state

        print("1")
        if self.is_whitespace(ch):
            self.index += 1
    
        elif ch.isdigit() and ch != "0":
            self.state = State.number
            self.index += 1
            self.accum = ch

        elif ch.isalpha():
            self.state = State.string
            self.accum = ch
            self.index += 1

        elif ch in PUNCT:
            self.state = State.punct
            
        elif ch == "{":
            self.state = State.comment
            self.index += 1

        elif ch == "0":
            self.state = State.zero
            self.index += 1

        elif ch == "{":
            self.state = State.comment
            self.state += 1
            
        else:
            msg = 'invalid characters at position {}, line {}'.format(self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    def handleNumberState(self):
        ##Taking care of number state

        print("3")
        if self.is_whitespace(self.programStr[self.index]):
            number, self.accum = self.accum, ""
            self.state = State.looking
            return self.handleNumber(number)

        elif self.programStr[self.index] in PUNCT:
            number, self.accum = self.accum, ""
            self.state = State.punct
            return self.handleNumber(number)

        elif self.programStr[self.index] == "{":
            number, self.accum = self.accum, ""
            self.state = State.comment
            return self.handleNumber(number)
        
        else:
            msg = 'invalid character at position {}, line {}'.format(self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    def handleZeroState(self):
        ##Taking care of zero state

        print("4")
        ch = self.programStr[self.index]
        if self.is_whitespace(ch):
            self.index += 1
            self.state = State.looking
            return Token(TokenType.NUMBER, 0)
        elif ch in PUNCT:
            self.state = State.punct
            return Token(TokenType.NUMBER, 0)
        elif ch == "{":
            self.state = State.comment
            self.index += 1
            return Token(TokenType.NUMBER, 0)    
        else:
            if ch.isdigit():        
                msg = "Integer cannot start with 0 in line {}".format(self.index%self.char_sums, self.linenumber)
            else:
                msg = "Invalid character {} at position {}, line {}".format(ch, self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    def handlePunctState(self):
        ##Taking care of punctuation state

        print("5")
        self.state = State.looking
        ch = self.programStr[self.index]
        if ch == ".":
            self.index += 1
            return Token(TokenType.PERIOD)
        
        elif ch == ",":
            self.index += 1
            return Token(TokenType.COMMA)

        elif ch == "(":
            self.index += 1
            return Token(TokenType.LEFT_PAREN)

        elif ch == ")":
            self.index += 1
            return Token(TokenType.RIGHT_PAREN)

        elif ch == ":":
            self.index += 1
            return Token(TokenType.COLON)

        elif ch == ";":
            self.index += 1
            return Token(TokenType.SEMI_COLON)

        elif self.is_arith_op(self.programStr[self.index]):
            self.index += 1
            return Token(TokenType.ARITH_OPR, self.programStr[self.index-1])

        else:
            msg = 'Invalid character {} at position {}, line {}'.format(ch, self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    def handleStringState(self):
        ##Taking care of string state

        print("6")
        ch = self.programStr[self.index]
        
        if self.is_whitespace(ch):
            word, self.accum = self.accum, ""
            self.state = State.looking
            return self.handleString(word)

        elif ch == "{":
            self.state = State.comment
            word, self.accum = self.accum, ""
            return self.handleString(word)

        elif ch in PUNCT:
            self.state = State.punct
            word, self.accum = self.accum, ""
            return self.handleString(word)
            
        else:
            msg = 'Invalid character {} at position {}, line {}'.format(ch, self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    def initializeTable(self):
        index = 0
        hmap = OrderedDict()
        TOTAL_KEYS = 51
        file = open('hmap.txt', 'r')
        states = [State.looking, State.number, State.string, \
                  State.comment, State.zero, State.punct]
        
        data = file.read()
        data = data.split()
        
        for i in string.ascii_lowercase:
            hmap[i] = {}

        for i in PUNCT:
            hmap[i] = {}

        hmap["_"] = {}
        for i in "123456789":
            hmap[i] = {}

        hmap["0"] = {}
        hmap["{"] = {}
        hmap["}"] = {}

        for j in states:
            for i in hmap.keys(): 
                hmap[i][j] = self.getEnum(data[index])
                index += 1
                #print("setting", i, j, data[index])
        file.close()
        #for i in hmap.keys():
        #    print(hmap[i])
        #print("\n\n")
        
        return hmap

    def getEnum(self, integer):
        
        if integer == "1":
            return State.looking
        elif integer == "2":
            return State.number
        elif integer == "3":
            return State.string
        elif integer == "4":
            return State.comment
        elif integer == "5":
            return State.comment
        elif integer == "6":
            return State.punct
        else:
            return State.error 
