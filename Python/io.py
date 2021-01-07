## Author:  Owen Cocjin
## Version: 0.3
## Date:    2021.01.06
## Description:  Input/output management, including pipes!
## Notes:
##    - In FIFO.writePipe(), there is a commented sleep line. This can be uncommented if the program uses too many resources
## Update:
##    - Added time buffers in FIFO.writePipe()
import os, threading, time

def handlePipe(pipe, toSend=None):
	'''Reads/Writes to pipe.
	If toSend is None, opens pipe in reading mode, else writing mode
	Needs to close when done to tell pipe it's done sending/receiving.
	Returns the read text if in reading mode.
	Threads are run as daemons (because they are in infinite loops).'''
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

class FIFO():
	'''Managed FIFO pipes.
	At most 2 pipes (one as input, one as output).
	Only pass pipe names, NOT file descriptors'''
	def __init__(self, name, *, pipe_in=None, pipe_out=None, daemon=False):
		self.name=name
		self.daemon=daemon
		self.pipes=[pipe_in, pipe_out]
		self.threads=[None, None]  #Matches self.pipes
		self.buffers=['', '']  #[read, write]
		#Starts threads
		self.startThreads()

	def __str__(self):
		return f'''FIFO {self.name}:
pipes:   {self.pipes}
threads: {self.threads}
buffers: {self.buffers}'''

	def startThreads(self):
		'''Starts threads'''
		#Reading thread
		if self.pipes[0]!=None:
			print("[|X:io:FIFO:startThreads]: Starting reading thread!")
			self.threads[0]=threading.Thread(name=f"{self.name}-reader",\
			target=self.readPipe,\
			daemon=self.daemon)
			self.threads[0].start()
		#Writing thread
		if self.pipes[1]!=None:
			print("[|X:io:FIFO:startThreads]: Starting writing thread!")
			self.threads[1]=threading.Thread(name=f"{self.name}-writer",\
			target=self.writePipe,\
			daemon=self.daemon)
			self.threads[1].start()

	def readPipe(self):
		'''Reads from a pipe'''
		self.buffers[0]=''
		while True:
			time.sleep(0.5)  #Sleep buffer so writing doesn't take too many resources
			with open(self.pipes[0], 'r') as f:
				self.buffers[0]+=f.read()
				#print("[|X:io:FIFO:readPipe]: Read from pipe!")
				#print(self.buffers[0])
	def writePipe(self):
		'''Writes to pipe'''
		while True:
			time.sleep(0.5)  #Sleep buffer so writing doesn't take too many resources
			with open(self.pipes[1], 'w') as f:
				if self.buffers[1]!='':  #Only write when buffer isn't empty
					f.write(self.buffers[1])
			self.buffers[1]=''

	def read(self):
		'''Returns buffer[0], then clears it.
		Returns None if buffer is an empty string'''
		if self.buffers[0]=='':
			return None
		else:
			toRet=self.buffers[0]
			self.buffers[0]=''
			return toRet

	def write(self, writebuff):
		'''Writes to pipes[1] by setting buffers[1]'''
		self.buffers[1]+=writebuff

	def getName(self):
		return self.name
	def getPipes(self):
		return self.pipes
	def getBuffers(self):
		return self.buffers
	def setName(self, new):
		self.name=new
	def setPipes(self, new, pipe=0):
		'''0=Input, 1=Output'''
		self.pipes[pipe]=new
	def setBuffers(self, new, buffer=0):
		'''0=Read, 1=Write'''
		self.buffers[buffer]=new

if __name__=="__main__":
	x=FIFO("test", pipe_in="in.bridge", pipe_out="out.bridge")
	print(x)
	while True:
		x.write(input(": "))
		print(x.read())
