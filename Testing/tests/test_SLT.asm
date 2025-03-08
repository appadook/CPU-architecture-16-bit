
#presuming all registers begin empty
#registers 3,4 should contain 1
#registers 5, and 6 should each contain 0
#Assumes your processor can handle immediates as high as 10
addi $1 $0 10
addi $2 $0 -10 # 1000 0100 0011 0110 = 8436
addi $5 $0 1
addi $6 $0 1
slt $3 $0 $1  #test the true cases # 0000 0110 0000 1100 = 060c
slt $4 $2 $0 # 0000 1000 1000 0100 = 0884
slt $5 $1 $0  #test the null cases
slt $6 $0 $2
