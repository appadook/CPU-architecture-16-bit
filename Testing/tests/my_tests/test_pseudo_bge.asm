#Author: Kurtik Appadoo
#Description: 
#	Pass = $3 = 3 (when $2 >= $1, branch is taken)
#	Fail = $3 = 6 (when branch is not taken)

# Test case 1: $2 > $1
addi $1 $0 1
addi $2 $0 2
bge $2 $1 1
addi $3 $3 3
addi $3 $3 3

# Expected: branch taken, $3 = 3