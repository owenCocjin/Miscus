##
## Author:  Owen Cocjin
## Version: 0.4.1
## Date:    2021.12.10
## Description:  Functions for manipulating bits
## Notes:
def bToI(b):
	'''Returns an int'''
	toret=0
	for i in b:
		toret=(toret<<8)+i
	return toret
def iToB(i,length=1):
	'''Returns a bytes object'''
	h=hex(i)[2:]
	if len(h)%2==1:
		h=f"0{h}"  #Add 0 for stupid bytes object
	#Add padding zeros if length!=None
	toret=bytes.fromhex(h)
	cur_length=len(toret)
	if cur_length<length:
		toret=b'\x00'*(length-cur_length)
	return toret
def setBit(target:int,new:int,pos:int,*,bits=1)->int:
	'''Sets a specific bit(s) in target.
	new is the new value.
	pos is the offset of bits from right to left.
	bits is the number of bits to be modified (make sure it lines up with the bits required for new).
	Returns the new value.
	Explanation:
		Set the desired bits to 0 in the target, then XOR the new bits into target'''
	return target&~(((2**(bits))-1)<<pos)^(new<<pos)
