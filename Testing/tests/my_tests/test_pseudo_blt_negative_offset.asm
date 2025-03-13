#Author: Kurtik Appadoo
#Description: 
#	Tests BLT instruction with negative offset (branch backwards)
#	Pass = $3 = 5 (loop completes 5 iterations)
#	Fail = $3 < 5 or $3 > 5 (loop doesn't iterate correctly)

# Initialize registers
addi $1 $0 0    # $1 = 0 (loop counter)
addi $2 $0 5    # $2 = 5 (loop limit)
addi $3 $0 0    # $3 = 0 (accumulator)

# Loop start (position 3)
addi $3 $3 1    # Add 1 to $3 each iteration
addi $1 $1 1    # Increment counter
blt $1 $2 -3    # Branch back to "Loop start" if counter < limit

# After loop completes:
# - $1 should be 5
# - $3 should be 5 (added 1 five times)
