#Author: Kurtik Appadoo
#Description: 
#	Pass = $3 = 3 (when $1 == $2, branch is taken)
#	Fail = $3 = 6 (when branch is not taken)

# Test case: $1 == $2
addi $1 $0 2
addi $2 $0 2
bge $1 $2 1
addi $3 $3 3
addi $3 $3 3

# Expected: branch taken, $3 = 3