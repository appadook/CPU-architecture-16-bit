#Author: Kurtik Appadoo
#Description: 
#	Tests the jr (jump register) pseudo-instruction
#	Pass = Program jumps to address stored in $7 ($ra)
#	      and $3 = 5 (skipping instructions after jr)

# Initialize registers
addi $1 $0 1   # $1 = 1
addi $2 $0 2   # $2 = 2

# Store jump destination address (10) in $7 (ra register)
addi $7 $0 10

# Jump to the address stored in $ra ($7), which is address 10
jr

# These instructions should be skipped (addresses 4-9)
addi $3 $0 30   # $3 = 30 (should be skipped)
addi $4 $0 30   # $4 = 30 (should be skipped)
addi $5 $0 30   # $5 = 30 (should be skipped)
addi $1 $0 30   # $1 = 30 (should be skipped)
addi $2 $0 30   # $2 = 30 (should be skipped)
addi $7 $0 30   # $7 = 30 (should be skipped)

# Program continues here (address 10)
addi $3 $0 5    # $3 = 5

# Expected values after execution:
# $1 = 1, $2 = 2 (unchanged from beginning)
# $3 = 5 (set after jump)
# $4 = 0, $5 = 0, $6 = 0 (registers not modified)
# $7 = 10 (the jump address, unchanged by jr)
