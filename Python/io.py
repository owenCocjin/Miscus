## Author:  Owen Cocjin
## Version: 0.1
## Date:    2020.12.26
## Description:  Input/output management, including pipes!
## Notes:
import os

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

def checkPipe(pipe):
	'''Creates a FIFO pipe if one doesn't exist.
	Return statuses:
	0: Pipe exists
	1: Pipe just created
	2: Error making pipe'''
	try:
		os.mkfifo(pipe)
		return 1
	except FileExistsError:
		return 0
	except:
		return 2
