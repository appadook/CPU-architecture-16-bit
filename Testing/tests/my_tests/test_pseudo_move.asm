#Author: Kurtik Appadoo
#Description: 
#	Pass = $3 = 5
#	Fail = Value of $3 is not 5

# Initialize $1 with value 5
addi $1 $0 5

# Use move pseudo-instruction to copy value from $1 to $3
move $3 $1

# If move worked, $3 should now be 5