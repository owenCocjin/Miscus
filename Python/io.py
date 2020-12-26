## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.26
## Description:  Input/output management, including pipes!
## Notes:
def handlePipe(pipe, toSend=None):
	'''Reads/Writes to pipe.
	If toSend is None, opens pipe in reading mode, else writing mode
	Needs to close when done to tell pipe it's done sending/receiving.
	Returns the read text if in reading mode'''
	if toSend==None:
		with open(pipe, 'r') as p:
			return p.read()
	else:
		with open(pipe, 'w') as p:
			p.write(str(toSend))
