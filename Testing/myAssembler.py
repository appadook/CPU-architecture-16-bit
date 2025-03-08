# Skeleton Assembler written by John Rieffel.
# Edits by Chris Fernandes.
# Author: Kurtik Appadoo

# R-type instruction: <R/I> <opcode> <rs> <rt> <rd> <funct>
# Bits:                 1        3    3    3    3    3

# I-type instruction: <R/I> <opcode> <rs> <rt> <immediate>
# Bits:                 1        3    3     3        6 

BITS_PER_REGISTER = 3
BITS_PER_IMMEDIATE = 6
import sys

from helperfunctions import *

# Hint: use a dictionary to map instructions to opcodes.
# It makes your life way easier.
R_TYPE = '0'
I_TYPE = '1'
functionDict = {'sub':'011','add':'000', 'and':'001', 'or':'010', 'slt':'100'}
opcodeDict = {'addi':'000', 'andi':'001', 'ori':'010', 'lw':'011', 'sw':'100', 'beq':'111', 'bne':'101'}
j = '110'

# Dictionary defining pseudo-instructions and their expansions
pseudoInstructions = {
    'move': {'real_op': 'add', 'format': 'R', 'template': '{rd} {rs} $0'},     # move rd, rs -> add rd, rs, $0
    'blt': {'real_op': 'slt', 'branch_op': 'bne', 'format': 'branch_cond', 'invert': False},  # blt rs, rt, label -> slt $1, rs, rt; bne $1, $0, label
    'bge': {'real_op': 'slt', 'branch_op': 'beq', 'format': 'branch_cond', 'invert': False},  # bge rs, rt, label -> slt $1, rs, rt; beq $1, $0, label
    'bgt': {'real_op': 'slt', 'branch_op': 'bne', 'format': 'branch_cond', 'invert': True},   # bgt rs, rt, label -> slt $1, rt, rs; bne $1, $0, label
    'ble': {'real_op': 'slt', 'branch_op': 'beq', 'format': 'branch_cond', 'invert': True},   # ble rs, rt, label -> slt $1, rt, rs; beq $1, $0, label
    'jar': {'format': 'jar'},  # jar label -> special hardcoded instruction + j label
}

def _handleJarInstruction(operands):
    """
    Private function to handle jar (jump and register) pseudo-instruction.
    Returns a list of strings, each representing a machine code instruction.
    
    jar label is broken down into:
    1. A special hardcoded instruction (1100000000000110 in binary = C006 in hex)
       This instruction saves the return address to $7 ($ra)
    2. A regular jump (j label) to the target address
    """
    expanded_instructions = []
    
    # First instruction is the hardcoded save-return-address instruction (1100000000000110)
    # This corresponds to a special opcode that the hardware recognizes for saving PC+1 to $7
    save_ra_instruction = '1100000000000110'
    expanded_instructions.append(save_ra_instruction)
    
    # Second instruction is a regular jump to the target address
    if len(operands) == 1:
        address = operands[0]
        jump_instruction = I_TYPE + j + int2bs(address, 12)
        expanded_instructions.append(jump_instruction)
    else:
        raise ValueError(f"jar instruction expects exactly one operand, got {len(operands)}")
    
    return expanded_instructions

def expandPseudoInstruction(operation, operands):
    """
    Expand a pseudo-instruction into one or more real instructions.
    Returns a list of strings, each representing a real instruction.
    """
    if operation not in pseudoInstructions:
        return None  # Not a pseudo-instruction
    
    pseudo_info = pseudoInstructions[operation]
    expanded_instructions = []
    
    if operation == 'jar':
        # Special handling for jar pseudo-instruction
        return _handleJarInstruction(operands)
    elif pseudo_info['format'] == 'R':
        # Handle simple register format pseudo-ops like 'move'
        template = pseudo_info['real_op'] + " " + pseudo_info['template']
        # For move: rd, rs -> add rd, rs, $0
        rd = operands[0]
        rs = operands[1]
        real_instruction = template.format(rd=rd, rs=rs)
        expanded_instructions.append(real_instruction)
    
    elif pseudo_info['format'] == 'branch_cond':
        # Handle branch operations that need comparison first
        rs = operands[0]
        rt = operands[1]
        label = operands[2]
        
        # If invert is True, swap registers for operations like bgt/ble
        if pseudo_info['invert']:
            rs, rt = rt, rs
            
        # First instruction: slt $1, rs, rt
        slt_instruction = f"{pseudo_info['real_op']} $1 {rs} {rt}"
        # Second instruction: beq/bne $1, $0, label
        branch_instruction = f"{pseudo_info['branch_op']} $1 $0 {label}"
        
        expanded_instructions.append(slt_instruction)
        expanded_instructions.append(branch_instruction)
    
    return expanded_instructions

def convertAssemblyToMachineCode(inline):
	'''given a string corresponding to a line of assembly,
	strip out all the comments, parse it, and convert it into
	a string of binary values'''

	outstring = ''

	if inline.find('#') != -1:
		inline = inline[0:inline.find('#')] #get rid of anything after a comment
		print(f"After removing comments: '{inline}'")
		
	if inline != '':
		words = inline.split() #assuming syntax words are separated by space, not comma
		print(f"Words after splitting: {words}")
		operation = words[0]
		print(f"Operation: {operation}")
		
		# Check if it's an I-type instruction
		is_itype = operation.endswith('i') or operation == 'lw' or operation == 'sw' or operation == 'beq' or operation == 'bne'
		is_jump = operation == 'j' or operation == 'jal' or operation == 'jr'
		print(f"Is I-type: {is_itype}")
		
		# Add the R/I type bit
		if is_itype:
			outstring += I_TYPE
			outstring += opcodeDict[operation]  # Add opcode for I-type
		elif is_jump:
			outstring += I_TYPE + j
		else:
			outstring += R_TYPE
			outstring += "000"  # For R-type, opcode is always 000
		
		# Special handling for lw and sw instructions with format: lw $rt, offset($rs)
		if operation == 'lw' or operation == 'sw':
			# Reconstruct the operand part by joining the remaining parts
			operand_part = " ".join(words[1:])
			print(f"Operand part for {operation}: '{operand_part}'")
			
			# Split by comma to get the register and memory parts - THIS IS THE ISSUE!
			# It's splitting by space, not comma in the assembly
			parts = operand_part.split(' ')
			print(f"Parts after splitting: {parts}")
			
			if len(parts) < 2:
				print(f"ERROR: Not enough parts in {operation} instruction: {operand_part}")
				return ""
				
			rt = parts[0].strip()  # First part is the register (rt)
			print(f"rt register: {rt}")
			
			# Extract the immediate and rs from the memory part
			memory_part = parts[1].strip()
			print(f"Memory part: '{memory_part}'")
			
			# Find where the parenthesis starts
			paren_start = memory_part.find('(')
			if paren_start == -1:
				print(f"ERROR: No opening parenthesis in memory part: {memory_part}")
				return ""
				
			immediate = memory_part[:paren_start].strip()  # Get immediate value
			print(f"Immediate value: {immediate}")
			
			paren_end = memory_part.find(')')
			if paren_end == -1:
				print(f"ERROR: No closing parenthesis in memory part: {memory_part}")
				return ""
				
			
			rs = memory_part[paren_start+1:paren_end].strip()  # Get base register
			print(f"rs register: {rs}")

			# Add rt (destination/source register)
			print(f"Adding rt register binary: {int2bs(rt[1:], BITS_PER_REGISTER)}")
			outstring += int2bs(rt[1:], BITS_PER_REGISTER)
			
			# Add rs (base register) first
			print(f"Adding rs (base) register binary: {int2bs(rs[1:], BITS_PER_REGISTER)}")
			outstring += int2bs(rs[1:], BITS_PER_REGISTER)
			
			
			
			# Add immediate (offset)
			print(f"Adding immediate binary: {int2bs(immediate, BITS_PER_IMMEDIATE)}, value: {immediate}")
			outstring += int2bs(immediate, BITS_PER_IMMEDIATE)
			print(f"Binary instruction so far: {outstring}")
			
		elif is_jump:
			# For jump instructions: <address>
			print(f"Processing jump instruction operands: {words[1:]}")
			address = words[1]
			outstring += int2bs(address, 12)
		elif is_itype:
			# For other I-type: <rs> <rt> <immediate>
			print(f"Processing I-type instruction operands: {words[1:]}")
			operands = words[1:]
			for i, oprand in enumerate(operands):
				if i < 2 and oprand[0] == '$':  # First two operands are registers
					outstring += int2bs(oprand[1:], BITS_PER_REGISTER)
				elif i == 2:  # Third operand is immediate
					outstring += int2bs(oprand, BITS_PER_IMMEDIATE)
		else:
			# For R-type: <rs> <rt> <rd> <funct>
			print(f"Processing R-type instruction operands: {words[1:]}")
			operands = words[1:]
			for i, oprand in enumerate(operands):
				if oprand[0] == '$':
					outstring += int2bs(oprand[1:], BITS_PER_REGISTER)
			
			# Add function code at the end for R-type instructions
			outstring += functionDict[operation]
	
	print(f"Final binary instruction: {outstring}")
	return outstring

def assemblyToHex(infilename,outfilename):
	'''given an ascii assembly file , read it in line by line and convert each line of assembly to machine code
	and hex. Then save that hex to an outputfile'''
	
	outlines = []
	f = open(infilename)
	lines = []
	for line in f:
		lines.append(line.strip())

	# First pass: expand pseudo-instructions
	expanded_lines = []
	for i, curline in enumerate(lines):
		print(f"\n--- Processing line {i+1}: '{curline}' ---")
		
		# Skip empty lines and comments
		if curline.strip() == '' or curline.strip().startswith('#'):
			expanded_lines.append(curline)
			continue
			
		# Remove comments
		if curline.find('#') != -1:
			curline = curline[0:curline.find('#')].strip()
		
		# Split the line into operation and operands
		parts = curline.split()
		if not parts:
			expanded_lines.append(curline)
			continue
			
		operation = parts[0]
		operands = parts[1:]
		
		# Check if it's a pseudo-instruction
		if operation in pseudoInstructions:
			print(f"Found pseudo-instruction: {operation}")
			expanded = expandPseudoInstruction(operation, operands)
			if expanded:
				print(f"Expanded to: {expanded}")
				# Add all expanded instructions to expanded_lines, not directly to outlines
				if operation == 'jar':
					# For jar, we need to convert the binary strings to assembly instructions
					# First instruction: Special "save return address" instruction
					expanded_lines.append("__special_savereturn__")  # Use a placeholder that won't conflict
					# Second instruction: Jump instruction
					expanded_lines.append(f"j {operands[0]}")
				else:
					expanded_lines.extend(expanded)
				continue
				
		# If not a pseudo-instruction or expansion failed, keep the original
		expanded_lines.append(curline)

	# Second pass: convert to machine code
	for i, curline in enumerate(expanded_lines):
		print(f"\n--- Converting line {i+1}: '{curline}' ---")
		try:
			if curline == "__special_savereturn__":
				# This is our special jar first instruction
				outstring = '1100000000000110'  # Hardcoded binary for C006
				outlines.append(outstring)
				print(f"Added special jar instruction: {bs2hex(outstring)}")
			else:
				outstring = convertAssemblyToMachineCode(curline)	
				if outstring != '':
					outlines.append(outstring)
					print(f"Hex output: {bs2hex(outstring)}")
				else:
					print("No output generated for this line")
		except Exception as e:
			print(f"ERROR processing line: {e}")
			import traceback
			traceback.print_exc()
	f.close()

	print(f"\nGenerated {len(outlines)} instructions")
	
	out = open(outfilename,'w')
	out.write("v2.0 raw\n")     # Logisim .hex files need this as 1st line
	for outline in outlines:
##		out.write(outline)  # uncomment to see the binary instruction word
		out.write("  " + bs2hex(outline))
		out.write("\n")
	out.close()
	print(f"Output written to {outfilename}")
			

if __name__ == "__main__":
	inputfile = "tests/my_tests/test_pseudo_jar.asm"  # Use the correct path without my_tests
	outputfile = inputfile.split(".")[0] + ".hex"
	assemblyToHex(inputfile,outputfile)
