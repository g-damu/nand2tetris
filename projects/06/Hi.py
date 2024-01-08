#print("Hi")
#from collections import OrderedDict
SymbolTable={
                "SP":"0",
                "LCL":"1",
                "ARG":"2",
                "THIS":"3",
                "THAT":"4",
                "SCREEN":"16384",
                "KBD":"24576"

            }

linemap={}

class Parser:
    def __init__(self, instruction):
        self.instruction=instruction.split("//")[0].strip()
        self.findType()
#        print(self.instruction)
        if(self.instrnType=="A"):
            self.handleAType()
        else:
            self.handleCType()
        
    def handleAType(self):
        if not self.isSymbol():
            self.issymbol=False
            val=self.instruction[1:]
            if(self.instruction[1]=="R"):
                val= self.instruction[2:]
            self.findBinary(val)
        else:
            self.issymbol=True
            self.symbolname=self.instruction[1:]
            if self.instruction[1:] not in SymbolTable:
                SymbolTable[self.instruction[1:]]=None
            
#        print(self.issymbol)
        
    def isSymbol(self):
        return (not (self.instruction[1].isdigit() or (self.instruction[1]=="R" and self.instruction[2].isdigit())))
    
    def handleCType(self):
        self.split()
    
    def split(self):
        jmpsplit=self.instruction.split(';')
        
        if len(jmpsplit)>1:
            self.dest=""
            self.jmp=jmpsplit[1]
            self.comp=jmpsplit[0]
        else:
            dstsplit=jmpsplit[0].split('=')
            self.dest=dstsplit[0]
            self.comp=dstsplit[1]
            self.jmp=""
         
#        print("DEST:"+self.dest,",COMP:"+self.comp,self.jmp)
#        self.comp=txt[1]
    
    def findBinary(self,val):
        self.binval = '{0:016b}'.format(int(val))
    
    def findType(self):
        if(self.instruction[0]=='@'):
            self.instrnType="A"
        else:
            self.instrnType="C"
#        print(self.instrnType)

class Code:
    def __init__(self,txt,part):
        self.txt=txt
        
        if part == 'c':
            self.getctrlbits()
        elif part == 'd':
            self.getdestbits()
        elif part == 'j':           
            self.getjmpbits()
        
    
    def getdestbits(self):
        destl=['0','0','0']
        
        if 'A' in self.txt:
            destl[0]='1'
        
        if 'M' in self.txt:
            destl[2]='1'
        
        if 'D' in self.txt:
            destl[1]='1'
        self.destbits="".join(destl)
#        print("DEST"+self.dest)
    
    def getjmpbits(self):
        text=self.txt
        jmpbitsmap={
        "":"000",
        "JMP":"111",
        "JEQ":"010",
        "JNE":"101",
        "JLE":"110",
        "JLT":"100",
        "JGT":"001",
        "JGE":"011",      
        }
        self.jmpbits=jmpbitsmap[text]
    
    def getctrlbits(self):
        text=self.txt
        a="0"
        if 'M' in text:
            a="1"
            text=text.replace("M","A")
            
        ctrlbitsmap={
                "0":"101010",
                "1":"111111",
                "-1":"111010",
                "D":"001100",
                "A":"110000",
                "!D":"001101",
                "!A":"110001",
                "-D":"001111",
                "-A":"110011",
                "D+1":"011111",
                "A+1":"110111",
                "D-1":"001110",
                "A-1":"110010",
                "D+A":"000010",
                "D-A":"010011",
                "A-D":"000111",
                "D&A":"000000",
                "D|A":"010101"                                  
                
                }
        
#        ctrl=ctrlbits[text.rstrip()]
        self.ctrlbits=a+ctrlbitsmap[text.rstrip()]
#        print("CTRL"+self.ctrl)
            
#    def 

#p1=Parser("Bye")
#print(p1.filename)
import sys

asmfile=sys.argv[1]

f=open(asmfile)

instrns=[]

lineno=-1

for x in f:
    if ((x not in ['\n']) and x[:2]!="//"):
        if x[0]=='(':
            lbl=x[1:x.find(')')]
            SymbolTable[lbl]=lineno+1
#            print(str(SymbolTable))
        else:
            lineno += 1
            p=Parser(x)
#            print(p.instrnType)
            if p.instrnType=="A":
#                print(p.binval)
                if not p.issymbol:
                    instrn=p.binval   
                
                else:
                    instrn=p.instruction
                    linemap[lineno]=p.symbolname
                    
            else:

#                print(p.dest,p.comp)
                dst=Code(p.dest,'d')
                
#                print(c.dest)
                ctrl=Code(p.comp,'c')
#                print(c.ctrl)
#                print("111"+ctrl.ctrl+dst.dest+"000")
                jmp=Code(p.jmp,'j')
                instrn="111"+ctrl.ctrlbits+dst.destbits+jmp.jmpbits
            instrns.append(instrn+"\n") 

count=16
for s in SymbolTable:
    
    if SymbolTable[s] is None:
        SymbolTable[s]=count
        count+=1

for s in linemap:
    
    p=Parser("@"+str(SymbolTable[linemap[s]]))
    instrns[s]=p.binval+"\n"

'''for i in instrns:
    print(i)
print(linemap)    
print(SymbolTable) '''  
hackfile=open(asmfile[:-4]+".hack","w")          

hackfile.writelines(instrns)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            