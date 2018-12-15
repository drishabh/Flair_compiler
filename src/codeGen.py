"""
    author:      rishabh dalal
    description: final codegen
"""
import os

##  0 .. 0
##  1 .. operand 1
##  2 .. operand 2
##  3 .. rarely used
##  4 .. Return val
##  5 .. Staus ptr
##  6 .. top ptr
##  7 .. PC


## -- AR-- 
##status pointer pointing to 0 of this ar

## -n->-3    .. n arguments
## -2        .. empty (left for some other possible args)
## -1        .. return val
## 0         .. addr to branch back to
## 1         .. r1
## 2         .. r2
## 3         .. r3
## 4         .. r5
## 5         .. r6


class CodeGenerator:
    def __init__(self, ast, symbol_table, caller_called,):
        self.ast = ast
        self.IR = ast.createIR()
        #print("ST", symbol_table)
        print('3AC code generated.')
        self.mainFunction = ast.identifier().value()
        
        self.symbol_table = symbol_table
        self.function_call = caller_called
        self.new_symbol_table = {}
        self.functionSeen = set()
        self.jumps = []
        self.result = []
        self.out = ''
        self.count = 0
        self.offset = [6]
        self.function = self.mainFunction
        self.start = 0
        self.label = {}
        self.jump_to = {}
        self.currentRank = 0
        self.curr = 0
        self.lastStart = -1
        self.recurse = False
        self.needToHandleParam = False
        
        
    def generate(self):
        self.initialize()
        file = 'tm_code.tm'
        file = open(file, 'w')
        file.write(self.out)
        file.close()
        print('tm code generated in file in /src: tm_code.tm')
        #print(self.out)
        
    def initialize(self):
        #status pointer
        
        self.outOff("LDC", 5,-1, 0)
        #top ptr
        self.outOff("LDC", 6,2, 0)
        self.prolog(self.mainFunction)
        self.prolog('print')
        self.outClean('HALT', 0,0,0)
        self.jumps[1].append(self.print_ar())
        self.handleIR(self.IR)
        #print("================================================")
        self.handleLabels()
        self.jumps[0].append(self.mainFunction)
        
        self.handle_jumps()

    def handleLabels(self):
        #print(self.label)
        
        for i in self.result:
            #print("I|", i)
            if not str(i[3]).isdigit():
                if not '-' in str(i[3]):
                    #print("IAC", i)
                    #print("self.label", self.label)
                    #print(i[3], self.label[i[3]])
                    #print("replacing", i[3], 'with', self.label[i[3]])
                    i[3] = self.label[i[3]]-int(i[0])-1
                    #print('new i', i)
        self.result = self.turnToString(self.result)

    def turnToString(self, lyst):
        self.out = ''
        for i in lyst:
            if i[-1] == 1:
                val = str(i[0])+ ": " + i[1] + " " + str(i[2]) + ","\
                      + str(i[3]) +"(" +str(i[4]) + ")\n"
                self.out += val
            elif i[-1] == 2:
                val = str(i[0])+ ": " + i[1] + " " + str(i[2]) + ","\
                      + str(i[3]) + "\n"
                self.out += val
            else:
                val = str(i[0])+ ": " + i[1] + " " + str(i[2]) + ","\
                      + str(i[3]) +"," +str(i[4]) + "\n"
                self.out += val
        
    def handle_jumps(self):
        #print('jumps', self.jumps)
        #print('jumps2', self.jump_to)
        #print("SOLVING JUMPS", self.jump_to)
        for i in self.jumps:
            val = str(i[0])+ ": LDA 7," + str(self.jump_to[i[1]][0]) +"(0)\n"
            self.out += val

    def prolog(self, fnName):
        offset = len(self.symbol_table[fnName]) - 1
        #print("off", offset, 'for', fnName)

        if fnName == 'print':
            self.outOff('ST', 1, 1,6)
                
            
        self.outOff('LDA', 1,6, 7) ##store return add
        self.outOff('ST',  1, offset+1, 6)
        self.outOff('ST',  5, offset+5, 6)
        self.outOff('LDA', 5, offset+1, 6)
        self.outOff('ST',  6, offset+6, 6)
        self.outOff('LDA',  6, offset+6, 6)
        ##jump
        self.jumps.append([self.count])
        self.count += 1


        self.outOff('LD', 6, 5, 5)
        self.outOff('LD', 5, 4, 5)
        
        if fnName != 'print':
            self.outOff('LD', 1, len(self.symbol_table[fnName]) - 1, 6)

    def print_ar(self):
        self.jump_to['print'] = [self.count]
        
        for i in range(1,4):
            self.outOff('ST', i, i, 5)

        ##only 1 formal parameter
        self.outOff('LD', 1, -1, 5)     
        self.outClean('OUT', 1, 0, 0)

        for i in range(1,4):
            self.outOff('LD', i, i, 5)
        self.outOff('LD', 7,0,5)
        return 'print'

    def handleIR(self, lst):
        
        while self.curr < len(lst):
            #print("-------------------------------Handling", lst[self.curr])
            op = lst[self.curr][0]
            if op == 'ENTRY':
                
                #print("1")
                if lst[self.curr][1] == self.mainFunction:
                    #print('----------=======INSIDE=======--------------')
                    self.startFunction(self.curr, lst)
                else:
                    #print('--------wrong place----------')
                    self.entry(lst[self.curr])
                
            elif op == 'EXIT':
                #print("2")
                self.endFunction(lst[self.curr])
            elif op == 'RETURN':
                #print("3")
                self.returnVal(lst[self.curr])
##            elif lst[i][0] == 'BEGIN_CALL':
##                self.calling(lst[i])
            elif op == 'PARAM':
                self.handleParam(lst[self.curr])
            elif op == 'RECEIVE':
                self.receive(lst[self.curr])
            elif op == 'BEGIN_CALL':             ##Redundant
                #self.handleBegin(lst[self.curr])
                pass
            elif op in ['CALL', 'PRINT']:
                self.call(lst[self.curr])
            elif op == '':
                #print("4")
                self.handleAssn(lst[self.curr])
            elif op in '+-/*':
                #print("5")
                self.handleArithOp(lst[self.curr])
            elif op in '=<':
                #print('7')
                self.handleEqualLess(lst[self.curr])
            elif op == 'if':
                self.handleIf(lst[self.curr])
            elif op in ['not', 'and', 'or']:
                #print("6")
                self.handleBoolOp(lst[self.curr])
            elif op in ['GOTO', 'LABEL']:
                self.handleJumps(lst[self.curr])
            else:
                #print("7")
                print('Can\'t handle now', lst[self.curr])
            self.curr += 1
            #print(self.curr)

    def entry(self, i):
        self.offset.append(6)
        self.function = i[1]
        self.functionSeen.add(i[1])
        #print("------------CALLING--------------", self.function)
        if not i[1] in self.jump_to:
            self.jump_to[i[1]] = [self.count]
        else:
            self.jump_to[i[1]].append(self.count)
                       
        for i in range(1,4):
            self.outOff('ST', i, i, 5)

##    def handleBegin(self, i):
##        temp = self.curr
##        
##        while True:
##            if self.IR[temp][0] == 'CALL':
##                if self.IR[temp][1] in self.functionSeen:
##                    self.recursiveCall = True
##                else:
##                    self.recursiveCall = False
##                break
##            else:
##                temp += 1

        ####NEW######
    def handleBegin(self, i):
        pass
            
    def handleParam(self, i):
        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        temp = self.curr

        if not self.needToHandleParam:
            flag = False
            self.recurse = False
            recVal = None
            
            while True:
                #print("Handling", self.IR[temp])
                if self.IR[temp][0] == 'CALL':
                    if self.IR[temp][1] != self.function:
                        #print("IS not called function so break")
                        flag = False
                        break
                if self.IR[temp][0] == 'RECEIVE':
                    if recVal == None:
                        #print('recVal', self.IR[temp][1])
                        recVal = self.IR[temp][1]
                elif self.IR[temp][0] == 'RETURN':
                    #print("ret val", self.IR[temp][1], 'recVal', recVal)
                    if self.IR[temp][1] == recVal:
                        #print('flag  True')
                        flag = True
                    else:
                        flag = False
                    break
                temp += 1
            self.recurse = flag
            self.needToHandleParam = True

        if not self.recurse:
            self.outOff('ST', 1, self.currentRank+1, 6)
            
        else:
            #print("$$$$$$$$$$$$$$$$$$$HANDLING PARAM", i[1])
            self.outOff('ST', 1, -1*(len(self.symbol_table[self.function])-1 \
                        +2) + self.currentRank, 5)
            #print(-1*(len(self.symbol_table[self.function])-1 \
            #            +2) + self.currentRank)
        self.currentRank += 1
                        
    def receive(self, i):
        if not i[1] in self.new_symbol_table:
            self.new_symbol_table[i[1]] = self.offset[-1]
            val = self.offset[-1]
            self.outOff('ST', 4, val, 5)
            self.outOff('LDA', 6, self.offset[-1], 5)
            self.offset[-1] += 1
            #self.incrementTop()
        else:
            val = self.new_symbol_table[i[1]]
        ##REceive the return value
            self.outOff('ST', 4, val, 5)
        
        
    def call(self, i):
        self.currentRank = 0
##        if i[0] == 'PRINT':
##            #print('insde')
##            self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
##            self.outClean('OUT', 1, 0, 0)
        if i[0] == 'PRINT':
            #print(self.new_symbol_table)
            self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
            self.outOff('ST', 1, 3, 6)
            self.outOff('LDC', 0, 2, 0)
            self.outClean('ADD', 6, 6, 0)
            self.outClean('SUB', 0, 0, 0)
            offset = 1
            self.outOff('LDA', 1,6, 7) ##store return add
            self.outOff('ST',  1, offset+1, 6)
            self.outOff('ST',  5, offset+5, 6)
            self.outOff('LDA', 5, offset+1, 6)
            self.outOff('ST',  6, offset+6, 6)
            self.outOff('LDA',  6, offset+6, 6)
            ##jump
            self.jumps.append([self.count, 'print'])
            self.count += 1


            self.outOff('LD', 6, 5, 5)
            self.outOff('LD', 5, 4, 5)
            self.outOff('LDC', 0, 2, 0)
            self.outClean('SUB', 6, 6, 0)
            self.outClean('SUB', 0,0,0)

        elif self.recurse:
            #print("INSIDE")
            self.outOff('LDA', 6, 5, 5)
            ##set pc
            self.outOff('LDC', 7, self.jump_to[self.function][0], 0)
            
        else:
            
            self.currentRank = 0
            self.outOff('LDC', 0, 2, 0)
            self.outClean('ADD', 6, 6, 0)
            self.outClean('SUB', 0, 0, 0)
            offset = len(self.symbol_table[i[1]])-1
            self.outOff('LDA', 1,6, 7) ##store return add
            self.outOff('ST',  1, offset+1, 6)
            self.outOff('ST',  5, offset+5, 6)
            self.outOff('LDA', 5, offset+1, 6)
            self.outOff('ST',  6, offset+6, 6)
            self.outOff('LDA',  6, offset+6, 6)
            ##jump
            self.jumps.append([self.count, i[1]])
            self.count += 1


            self.outOff('LD', 6, 5, 5)
            self.outOff('LD', 5, 4, 5)
            self.outOff('LDC', 0, 2, 0)
            self.outClean('SUB', 6, 6, 0)
            self.outClean('SUB', 0,0,0)
        self.recurse = False
        self.needToHandleParam = False
            
        #self.outOff('LD', 1, len(self.symbol_table[i[1]]) - 1, 6)
        
##        offset = self.currentRank
##        self.currentRank = 0
##        self.outOff('LDA', 1,6, 7) ##store return add
##        self.outOff('ST',  1, offset+1, 6)
##        self.outOff('ST',  5, offset+6, 6)
##        self.outOff('LDA', 5, offset+1, 6)
##        self.outOff('ST',  6, offset+7, 6)
##        self.outOff('LDA',  6, offset+9, 6)
##        ##jump
##        self.jumps.append([self.count, i[1]])
##        self.count += 1
##
##
##        self.outOff('LD', 6, 5, 5)
##        self.outOff('LD', 5, 4, 5)
##        
##        self.outOff('LD', 1, len(self.symbol_table[i[1]]) - 1, 6)
##    
        
    def startFunction(self, index, lst):
        #print("INSIDE")
        self.jump_to[lst[index][1]] = [self.count]
        self.start = self.count
        for i in range(1,4):
            #self.outOff('ST', i, i+1, 5)
            self.outOff('ST', i, i, 5)
        index += 1
                    
    def endFunction(self, i):
        for j in range(1,4):
            self.outOff('LD', j, j, 5)
                    
        self.outOff('LD', 7, 0, 5)
        self.offset.pop()
        

    def returnVal(self, i):
        #print("I", i)
        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        self.outOff('ST', 1, -1, 5)
        self.outOff('LD', 4, self.new_symbol_table[i[1]], 5)
        

    def incrementTop(self):
        self.outOff('LDC', 0,1,0)
        self.outClean('ADD', 6,6,0)
        self.outClean('SUB', 0,0,0)
        
    def handleAssn(self, i):
        #print("==============ASSN handling=================", i)        
        reg = 1
        
        if i[1].isdigit():
            #print(1)
            self.outOff('LDC', reg, i[1], 0)
            
        else:
            if i[1] == 'true':
                #print(2)
                self.outOff('LDC', reg, 1, 0)
                    
            elif i[1] == 'false':
                #print(3)
                self.outOff('LDC', reg, 0, 0)
                
            else:
                #print(5)
                #print("ST for", self.function, self.symbol_table[self.function])
                #print('function', self.function)
                total = len(self.symbol_table[self.function])-1
                for j in range(total):
                    #print('j', j, 'curr', self.symbol_table[self.function][j][0],\
                    #      'tocompater2', i[1])
                    if self.symbol_table[self.function][j][0] == i[1]:
                        #print(6)
                        #print(self.symbol_table[self.function][j][0], 'is at',\
                        #      -1*(total-j)-2)
                        self.outOff('LD', reg, -1*(total-j+2), 5)
                        #print("IR", reg, -1*(total-j+2), 5)
                        break
        #print("ST", self.new_symbol_table)
        if i[-1] in self.new_symbol_table:
            #print(i[-1], 'in st')
            self.outOff('ST', reg, self.new_symbol_table[i[-1]], 5)
        else:
            #print(i[-1], 'not in st')
            self.outOff('ST', reg, self.offset[-1], 5)
            self.new_symbol_table[i[-1]] = self.offset[-1]
            self.outOff('LDA', 6, self.offset[-1], 5)
            self.offset[-1] += 1
            #self.incrementTop()

        #print("==============end ASSN handling=================")
            

    def handleBoolOp(self, i):
        #implementing short circuit
        
        regToOutput = 3
        
        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        
        if i[0] == 'not':
            self.outOff('JNE', 1, 2, 7)
            self.outOff('LDC', 1, 1, 0)
            self.outOff('LDA', 7, 1, 7)
            self.outOff('LDC', 1, 0, 0)
            
        else:
            self.outOff('LD', 2, self.new_symbol_table[i[2]], 5)
            if i[0] == 'or':    
                self.outOff('JNE', 1, 3, 7)
                self.outOff('JNE', 2, 2, 7)
                self.outOff('LDC', 1, 0, 0)
                self.outOff('LDA', 7, 1, 7)
                self.outOff('LDC', 1, 1, 0)
            
            else:
                self.outClean('MUL', 1, 1, 2)

        if i[-1] in self.new_symbol_table:
            #print(i[-1], 'in st')
            self.outOff('ST', 1, self.new_symbol_table[i[-1]], 5)
        else:
            self.new_symbol_table[i[-1]] = self.offset[-1]
            self.outOff('ST', 1, self.offset[-1], 5)
            self.outOff('LDA', 6, self.offset[-1], 5)
            self.offset[-1] += 1
            #self.incrementTop()

    def handleEqualLess(self, i):
        #print("INSIDE handle equal")
        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        self.outOff('LD', 2, self.new_symbol_table[i[2]], 5)
        flag = False
        if i[-1] in self.new_symbol_table:
            off = self.new_symbol_table[i[-1]]
        else:
            self.new_symbol_table[i[-1]] = self.offset[-1]
            flag = True
            off = self.offset[-1]
            self.offset[-1] += 1
                   

        if i[0] == '=':
            #print('i', i)
            
            #print("ST", self.new_symbol_table)
            
            self.outClean('SUB',1,1,2)
            self.outOff('JNE',1,3,7)
            self.outOff('LDC', 1, 1, 0)                
            self.outOff('ST',1,off,5)
            self.outOff('LDA',7,2,7)
            self.outOff('LDC',1,0,0)
            self.outOff('ST',1,off,5)
            
        else:
            self.outClean('SUB',1,1,2)
            self.outOff('JGE',1,3,7)
            self.outOff('LDC', 1, 1, 0)
            self.outOff('ST',1,off,5)
            self.outOff('LDA',7,2,7)
            self.outOff('LDC',1,0,0)
            self.outOff('ST',1,off,5)

        if flag:
            #self.incrementTop()
            self.outOff('LDA', 6, self.offset[-1]-1, 5)
        
    def handleIf(self, i):
        self.outOff('LD',1,self.new_symbol_table[i[1]],5)
        jumpTo = (i[-1].split())[-1]
        self.outOff('JNE',1,jumpTo,7)
        
    def handleJumps(self, i):
        #print(i)
        if i[0] == 'GOTO':
            self.outOff('LDA', 7, i[1], 7)
        elif i[0] == 'LABEL':
            self.label[i[1]] = self.count

    def handleArithOp(self, i):
        regToOutput = 3

        self.outOff('LD', 1, self.new_symbol_table[i[1]], 5)
        if i[2] != '':
            self.outOff('LD', 2, self.new_symbol_table[i[2]], 5)
        
        if i[0] == '-':
            if i[2] != '':
                self.outClean('SUB', 1, 1, 2)
            else:
                self.outClean('SUB', 1, 0, 1)                                  
        elif i[0] == '*':
            self.outClean('MUL', 1, 1, 2)
        elif i[0] == '/':
            self.outClean('DIV', 1, 1, 2)            
        else:
            self.outClean('ADD', 1, 1, 2)

        if i[-1] in self.new_symbol_table:
            #print(i[-1], 'in st')
            self.outOff('ST', 1, self.new_symbol_table[i[-1]], 5)
        else:
            #print(i[-1], 'not in st putting it in', self.offset[-1])
            self.new_symbol_table[i[-1]] = self.offset[-1]
            self.outOff('ST', 1, self.offset[-1], 5)
            self.outOff('LDA', 6, self.offset[-1], 5)
            self.offset[-1] += 1
            #self.incrementTop()
        
            
    def outOff(self, op, reg1, off, reg2):
##        val = str(self.count)+ ": " + op + " " + str(reg1) + ","\
##              + str(off) +"(" +str(reg2) + ")\n"
##        self.result += val
        val = [self.count, op, reg1, off, reg2, 1]
        #print('val', val)
        self.result.append(val)
        self.count += 1

    def outTwo(self, op, reg1, reg2):
##        val = str(self.count)+ ": " + op + " " + str(reg1) + ","\
##              + str(reg2) + "\n"
##        self.result += val
        val = [self.count, op, reg1, reg2, 2]
        #print('val', val)
        self.result.append(val)
    
        self.count += 1

    def outClean(self, op, reg1, reg2, reg3):
##        val = str(self.count)+ ": " + op + " " + str(reg1) + ","\
##              + str(reg2) +"," +str(reg3) + "\n"
##        self.result += val
        val = [self.count, op, reg1, reg2, reg3, 3]
        self.result.append(val)
        #print('val', val)
        self.count += 1

    def comment(self, msg=None):
        if msg:
            self.result += msg + '\n'
        else:
            self.result += '\n'
