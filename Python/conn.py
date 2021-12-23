## Author:  Owen Cocjin
## Version: 1.1
## Date:    2021.12.23
## Description:  Socket helper functions

def recvExact(s,n):
	'''Receive exactly n bytes from s via while loop.
	Returns None if timeout.
	NOTE: This function depends on the RecvError below!'''
	toret=b''
	target=n
	try:
		while True:
			toret+=s.recv(target)
			if toret==b'':  #Remote closed
				raise RecvError("Remote closed")
			target=n-len(toret)
			if target!=0:
				continue
			else:
				return toret
	except socket.timeout:
		return None


class RecvError(Exception):
	'''NOTE: This is depended by recvExact!'''
	def __init__(self,message):
		super().__init__(f"Error receiving bytes: {message}")
		self.message=message
