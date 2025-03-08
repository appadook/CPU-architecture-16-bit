#Author: Kurtik Appadoo
#Description: 
#	Tests the jar (jump and register) pseudo-instruction
#	Pass = Value in $7 is PC+1 after jar instruction
#	      and program jumps to instruction at address 12

# NOTE: Instructions are zero-indexed in memory
# Instruction 0: addi $1 $0 1
# Instruction 1: addi $2 $0 2
# Instruction 2: addi $3 $0 3
# Instruction 3: the C006 special instruction (part of jar expansion)
# Instruction 4: the j 12 instruction (part of jar expansion)
# Instruction 5-11: skipped instructions
# Instruction 12: program continues here

# Initialize registers
addi $1 $0 1   # $1 = 1
addi $2 $0 2   # $2 = 2
addi $3 $0 3   # $3 = 3

# This jar instruction should:
# 1. Save PC+1 (which is 5) to $7
# 2. Jump to instruction at address 12
jar 12

# These instructions should be skipped (addresses 5-11)
addi $4 $0 99   # $4 = 99 (should be skipped)
addi $5 $0 99   # $5 = 99 (should be skipped)
addi $6 $0 99   # $6 = 99 (should be skipped)
addi $1 $0 99   # $1 = 99 (should be skipped)
addi $2 $0 99   # $2 = 99 (should be skipped)
addi $3 $0 99   # $3 = 99 (should be skipped)
addi $7 $0 99   # $7 = 99 (should be skipped)

# Program continues here (address 12)
addi $4 $0 4    # $4 = 4

# Test if return address was saved correctly
# Expected values:
# $1 = 1, $2 = 2, $3 = 3 (unchanged from beginning)
# $4 = 4 (set after jump)
# $5 = 0, $6 = 0 (unchanged)
# $7 = 0
