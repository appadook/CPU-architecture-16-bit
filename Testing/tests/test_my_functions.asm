#   Tests jal and jr.  Assumes no stack, but j must be implemented.
#   Assume 1, 2, 3, 4 are stored in memory, starting at addr 0.
#   Swap contents of array given *indices* to be swapped
#   Register use:
#	$1: base addr of array arr (assume arr starts at mem addr 0)
#	$2: 1st index to swap
#	$3: 2nd index to swap
#	$4: true addr of index $2
#	$5: true addr of index $3
#	$6:	contents of arr[$2]
#	$0: temporary storage (replaces $7's role)
#	Passes if array contains 2, 1, 4, 3 in that order

    j 8				# jump to main at addr (line) 8
    add $4 $1 $2	# $4 = &arr[$2]  (start of swap function)
    add $5 $1 $3	# $5 = &arr[$3]
    lw $6 0($4)		# $6 = arr[$2]
    lw $0 0($5)		# $0 = arr[$3]  (using $0 instead of $7)
    sw $6 0($5)
    sw $0 0($4) 
    jr $ra
    addi $1 $0 0	# base addr of array (start of main)
    addi $2 $0 0	# swap arr[0]
    addi $3 $0 1	# with arr[1]
    jal 1			# swap arr[$2] with arr[$3]
    addi $2 $0 2
    addi $3 $0 3
    jal 1