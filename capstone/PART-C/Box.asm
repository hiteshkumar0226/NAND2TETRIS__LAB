// Capstone Box.asm - K=33, starts at row 33, 20 rows, 32 pixels wide.
// A pressed key draws black (-1); no key clears the box (0).
(LOOP)
    @KBD
    D=M
    @BLACK
    D;JNE
    @WHITE
    0;JMP

(BLACK)
    @R3
    M=-1
    @DRAW
    0;JMP

(WHITE)
    @R3
    M=0

(DRAW)
    // R0 = SCREEN + 32*33 = 17440
    @17440
    D=A
    @R0
    M=D
    // R2 = number of rows
    @20
    D=A
    @R2
    M=D

(ROW)
    // Draw two adjacent 16-bit words (32 pixels).
    @R3
    D=M
    @R0
    A=M
    M=D
    @R0
    M=M+1
    @R3
    D=M
    @R0
    A=M
    M=D
    // Advance from the second word to the same position next row (+31).
    @R0
    D=M
    @31
    D=D+A
    @R0
    M=D
    // Decrement row counter.
    @R2
    M=M-1
    D=M
    @ROW
    D;JGT
    @LOOP
    0;JMP
