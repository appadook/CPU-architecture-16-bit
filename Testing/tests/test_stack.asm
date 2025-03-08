#   Test of $sp via recursion
#	Requires support for bne, j, jal, and jr
#   find A + B in a wacky recursive way
#   Register use:
#	$1: A (=4)
#	$2: B (=3)
#	$3: function return value (acts as $v0)
#   $4: test passes if 7 is here at end
	
	addi $1 $0 4
	addi $2 $0 3 
	jal 5
	add $4 $0 $3
	j 18
	addi $sp $sp -1 	# addr 5: start of RecurAdd
	sw $ra 0($sp)
	bne $1 $0 4			# branch offset = 4 starting from next line (else line)
	add $3 $2 $0
	lw $ra 0($sp)
	addi $sp $sp 1
	jr $ra
	addi $1 $1 -1		# start of else
	jal 5
	addi $3 $3 1
	lw $ra 0($sp)
	addi $sp $sp 1
	jr $ra
	# addr 18: end