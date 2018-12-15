##if -then -else --> keywords??
##true-false --> boolean token??                        
##eof vs period                                         <-> sorted
##take care of line position                            <-> sorted
##problem with begin, 0, end --> printing None          <-> sorted

from flr_token import Token, TokenType
from error import LexicalError
RESERVED_WORDS = ["program", "function", "begin", "end", "print", "or", \
                  "and", "if", "then", "else", "not", "return", "integer", "boolean",\
                  "true", "false"]
ARITHMETIC_OPR = ["<", "=", "*", "/", "-", "+"]
COMMENT = ["{", "}"]

IDENTIFIER_LIMIT = 256
#LOW_RANGE = - (2**32)
HIGH_RANGE = (2**32) - 1


class Scanner:

    def __init__(self, programStr):
        self.programStr = programStr
        self.index      = 0
        self.linenumber = 1
        self.length     = len(self.programStr)
        self.char_sums = 0

    ##---------PUBLIC---------------------------------------
        
    def next_token(self):
        return self.get_next_token()

    def get_next_token(self):
        
        self.skip_whitespace()
        
        if self.index >= self.length:
            return Token(TokenType.EOF)
        
        ch = self.programStr[self.index]
        if ch == ".":
            self.index += 1
            return Token(TokenType.PERIOD)
        
        if ch.isalpha():
            word = self.get_keyword()
            if word in RESERVED_WORDS:
                return Token(TokenType.KEYWORD, word)
            if len(word) > IDENTIFIER_LIMIT:
                msg = "Maximum identifier length surpassed in line {}".format(word, self.linenumber)
                raise LexicalError(msg)
            return Token(TokenType.IDENTIFIER, word)

        elif ch.isdigit():
            number = self.get_number()
            if (number[0] == "0"):
                if (len(number) == 1):
                    return self.handle_number(int(number))
                else:
                    msg = "Integer {} cannot start with 0 in line {}".format(number, self.linenumber)
                    raise LexicalError(msg)
            else:
                return self.handle_number(int(number))
                    
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

        elif self.is_arith_op():
            self.index += 1
            return Token(TokenType.ARITH_OPR, self.programStr[self.index-1])

        elif ch == "{":
            self.comment_char()
            return self.get_next_token()

        ##no token match
        else:
            msg = 'invalid characters at position {}, line {}'.format(self.index%self.char_sums, self.linenumber)
            raise LexicalError(msg)

    ##---------PRIVATE------------------------------------
        
    def skip_whitespace(self):
        while self.index < self.length and \
              self.is_whitespace(self.programStr[self.index]):
            self.index += 1
        return

    def is_whitespace(self, ch):
        if '\n' in ch:
            self.linenumber += 1
            self.char_sums = self.index
        return ch in "\n\t\r "

    def get_keyword(self):
        startIndex = self.index
        while self.index < self.length and \
              (self.programStr[self.index].isalpha() or \
               self.programStr[self.index].isdigit() or \
               self.programStr[self.index] == "_"):
               ##Already cheacked above for first alpha char
            
            self.index += 1
        return self.programStr[startIndex: self.index]

    def get_number(self):
        startIndex = self.index
        while self.index < self.length and self.programStr[self.index].isdigit():
            self.index += 1
        return self.programStr[startIndex : self.index]

    def handle_number(self, number):
        if (number > HIGH_RANGE):
            msg = "Integer {} out of bounds in line {}".format(number, self.linenumber)
            raise LexicalError(msg)
        return Token(TokenType.NUMBER, number)
    
    def is_arith_op(self):
        return self.programStr[self.index] in ARITHMETIC_OPR

    def comment_char(self):
        if self.programStr[self.index] == "{":
            while self.programStr[self.index] != "}":
                self.index += 1
            self.index += 1
        
