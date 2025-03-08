#Author: Chris Fernandes
#Description: 
#	Pass = $3 = 3
#	Fail = $3 = 6

addi $1 $0 1
addi $2 $0 2
blt $1 $2 1
addi $3 $3 3
addi $3 $3 3
