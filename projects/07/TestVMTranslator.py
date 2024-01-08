
class Parser:

    def __init__(self, infile):
        
        self.file=open(infile)
        
      
    def hasMoreCommands(self):
        
        currline = self.file.readline()
        
        while currline[:2] == "//" or currline=='\n':
            
            currline=self.file.readline()
#            print(currline)
        
        self.currline=currline
#        print(self.currline)
        
        return len(self.currline)>0
    
    def advance(self):
    
        self.command=self.currline
    
    def commandType(self):
    
        self.command_parts=self.command[:-1].split(' ')
        
        oplist=["add","sub","lt","gt","eq","not","and","or","neg"]
        
        if self.command_parts[0] == "pop":
            return "C_POP"
    
        elif self.command_parts[0] == "push":
            return "C_PUSH"
    
        elif self.command_parts[0] in oplist:
            return "C_ARITHMETIC"
    
    def arg1(self):
        if self.commandType() == "C_ARITHMETIC":
            return self.command_parts[0]
        return self.command_parts[1]
    
    def arg2(self):
        return self.command_parts[2]

class CodeWriter:
    
    
    def __init__(self,outfile):
        self.lines=[]
        self.cmpOpCount={"lt":0,"gt":0,"eq":0}
        self.file=open(outfile,"w")   
    
    def writeArithmetic(self,command):
        
        binaryOps={"add" : "+","sub":"-","or":"|","and":"&","lt":"lt","gt":"gt","eq":"eq"}
        unaryOps={"not":"!","neg":"-"}
        cmpOps=["lt","gt","eq"]

        
        self.lines.append(command)
        
        
        self.writeSPDec()    #pop var1
        
        if command in unaryOps:
            self.lines.append("D="+unaryOps[command]+"D")
        
        elif command in binaryOps:
        
        
            self.lines.append("@var1")
            self.lines.append("M=D")
        
            self.writeSPDec()    #pop var2
            self.lines.append("@var1")
            if command not in cmpOps:
                self.lines.append("D=D"+binaryOps[command]+"M")
            
            else:
                self.lines.append("D=D-M")
                self.lines.apppend("@"+command+str(self.cmpOpCount[command]))
                self.lines.append("D;J"+command.upper())
                self.lines.append("D=0")
                self.lines.append("@NXT"+command+str(self.cmpOpCount[command]))
                self.lines.append("0;JMP")
                self.lines.append("("+command+str(self.cmpOpCount[command])+")")            
                self.lines.append("D=-1")
                self.lines.append("(NXT"+command+str(self.cmpOpCount[command])+")")
                self.cmpOpCount[command] = self.cmpOpCount[command]+1
        
        self.writeSPInc() # push result present in D
        
#    def writeNoJmp():
        
    
    def writeSPDec(self):
        self.lines.append("@SP")
        self.lines.append("M=M-1")
        self.lines.append("A=M")
        self.lines.append("D=M")
        
    def writeSPInc(self):
        self.lines.append("@SP");
        self.lines.append("A=M");
        self.lines.append("M=D");
        self.lines.append("@SP");
        self.lines.append("M=M+1");
        
    
    def writePushPop(self,command,segment,index):
        
        self.lines.append(command+" "+segment+" "+str(index))
        
        segtext=segment.upper()
        if segment=="local":
            segtext="LCL"
        
        elif segment=="argument":
            segtext="ARG"
        
        elif segment=="temp":            
            segtext=str(5)
        
        elif segment=="static":            
            segtext=str(16)
        
        if command=="C_PUSH":
            
            self.lines.append("@"+str(index))
            self.lines.append("D=A")
            
            if segment!="constant":
                self.lines.append("@"+segtext)
                
                if segment=="local" or segment=="argument" or segment=="this" or segment=="that":
                    self.lines.append("A=M+D")
                elif segment=="static" or segment=="temp":
                    self.lines.append("A=A+D")
                self.lines.append("D=M")


            self.writeSPInc()
                        
        elif command=="C_POP":
            self.lines.append("@"+segtext)
            if segment=="local" or segment=="argument" or segment=="this" or segment=="that":
                self.lines.append("D=M")
            elif segment=="static" or segment=="temp":
                self.lines.append("D=A")
            self.lines.append("@"+str(index))
            self.lines.append("D=D+A")
            self.lines.append("@addr")
            self.lines.append("M=D")
            self.writeSPDec()

            self.lines.append("@addr")
            self.lines.append("A=M")
            self.lines.append("M=D")
        
#        for l in lines:
        
#            print(l)

    def close(self):
        
 #       for l in self.lines:
 #           print(l)
        separator="\n"
        self.file.write(separator.join(self.lines))
        self.file.close()
        

import sys

vmfile=sys.argv[1]

parser=Parser(vmfile)

asmfile=vmfile[:-3]+"1.asm"

writer=CodeWriter(asmfile)

while(parser.hasMoreCommands()):
 
    parser.advance()

    if parser.commandType()=="C_ARITHMETIC":
#        print(parser.commandType(),parser.arg1())
        writer.writeArithmetic(parser.arg1())
        
    
    elif parser.commandType()=='C_PUSH' or parser.commandType()=="C_POP" :
 #       print(parser.commandType(),parser.arg1(),parser.arg2())
        writer.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())

writer.close()
    
        
        



























    
    
    