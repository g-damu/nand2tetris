// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@SCREEN
D=A

@curraddr
M=D

@256
D=A
@rowcount
M=D

@32
D=A
@colcount
M=D

(ROWLOOP)

@32
D=A
@colcount
M=D

@rowcount
D=M
@END
D;JEQ

(COLUMNLOOP)
@colcount
D=M
@COLUMNLOOPEND
D;JEQ
@curraddr
D=M
M=M+1
A=D
M=-1

@colcount
M=M-1
@COLUMNLOOP
0;JMP

(COLUMNLOOPEND)
@rowcount
M=M-1
@ROWLOOP
0;JMP


(END)
@END
0;JMP


