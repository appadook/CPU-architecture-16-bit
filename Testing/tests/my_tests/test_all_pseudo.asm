#Author: Kurtik Appadoo
#Description: 
#	Tests all implemented pseudo-instructions
#	Pass = $7 = 15

# Initialize values
addi $1 $0 5   # $1 = 5
addi $2 $0 10  # $2 = 10

# Test move
move $3 $1     # $3 = 5

# Test blt (less than)
blt $1 $2 1    # 5 < 10, should branch
addi $4 $0 0   # Skipped if branch taken
addi $4 $0 5   # $4 = 5

# Test bgt (greater than)
addi $5 $0 15  # $5 = 15
bgt $5 $2 1    # 15 > 10, should branch
addi $6 $0 0   # Skipped if branch taken
addi $6 $0 5   # $6 = 5

# Test ble (less than or equal) with equality
addi $1 $0 10  # $1 = 10 (now equal to $2)
ble $1 $2 2    # 10 <= 10, should branch
addi $7 $0 0   # Skipped if branch taken
addi $7 $0 0   # Skipped if branch taken
addi $7 $7 15  # $7 = 15

# Success if all branches worked correctly
# $3 should be 5 (from move)
# $4 should be 5 (from blt)
# $6 should be 5 (from bgt)
# $7 should be 15 (from ble)
