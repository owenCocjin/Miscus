## Author:  Owen Cocjin
## Version: 1.1
## Date:    2021.01.13
## Description:  Input/output management, including pipes!
## Notes:
##    - FIFO doesn't manage itself very well. The user will have to manage reading/writing a lot.
##    - When switching between modes, the current mode must be fulfilled before the switch happens.
##        * eg. If you are reading and switch to write mode, FIFO will continue to read until data is written to the pipe
## Update:
##    - Fixed FIFO reading not storing read lines
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
	Only pass pipe name, NOT file descriptors.
	"daemon" arg is for threading.
	"block" arg determines if pipes block or not.
	Because a pipe should only be read OR written by the class at a time, only one thread is required'''
	def __init__(self, name, *, pipe=None, daemon=False, block=False, mode=1):
		self.name=name
		self.pipe=pipe
		self.daemon=daemon
		self.block=block
		self.read_buffer=''
		self.write_buffer=''
		self.proc=0  #0=Clear; 1=Reading; 2=Writing
		self.mode=mode  #1=Read; 2=Write; 0=Kill thread
		self.thread=None
		#Starts thread & set's read/write function
		if not self.block:  #Using thread
			self.thread=threading.Thread(name=f"{self.name}",\
			target=self.threadRunner,\
			daemon=self.daemon)

			self.thread.start()

			self.read=self.readNoBlocking
			self.write=self.writeNoBlocking
		else:
			self.read=self.readBlocking
			self.write=self.writeBlocking

	def __str__(self):
		return f'''FIFO {self.name}:
pipe:   {self.pipe}
thread: {self.thread}
buffers: [{self.read_buffers}, {self.write_buffer}]'''

	def threadRunner(self):
		'''Manages if the process is either reading or writing at the moment'''
		#Check mode to see if should be read/writing
		while self.mode!=0:
			if self.mode==1:
				self.readPipe()
			elif self.mode==2:
				self.writePipe()
			else:  #Sleep as to not hog resources
				time.sleep(0.5)
	def readPipe(self):
		'''Reads from a pipe'''
		self.proc=1
		with open(self.pipe, 'r') as f:
			self.read_buffer+=f.read()
			#print(f"[|X:io:FIFO:readPipe]: {self.read_buffer}")
		self.proc=0
		return self.read_buffer
	def writePipe(self):
		'''Writes to pipe'''
		self.proc=2
		with open(self.pipe, 'w') as f:
			while self.write_buffer=='':
				time.sleep(0.1)  #Time buffer
			f.write(self.write_buffer)
		toRet, self.write_buffer=self.write_buffer, ''
		self.proc=0
		return self.write_buffer

	def readBlocking(self):
		'''Reads through pipe'''
		toRet=readPipe()
		self.write_buffer=''
		return toRet
	def writeBlocking(self, toWrite=None):
		'''Writes through pipe'''
		return writePipe(toWrite)
	def readNoBlocking(self):
		'''Returns self.read_buffer if not ""'''
		if self.read_buffer!='':
			toRet, self.read_buffer=self.read_buffer, ''
			return toRet
		else:
			return None
	def writeNoBlocking(self, toWrite=None):
		'''Starts writing thread, if not started.
		Returns True is write was put through.
		Returns False if thread was already writing
		Returns None if currently reading'''
		if toWrite!=None:
			self.write_buffer=toWrite
		return True

	def switchTo(self, proc):
		'''Switch to reading/writing:
		1=Reading
		2=Writing'''
		self.mode=proc

	def kill(self):
		'''Sets mode to 0, marking thread to die'''
		self.mode=0

	def getName(self):
		return self.name
	def getPipe(self):
		return self.pipe
	def getMode(self):
		return self.mode
	def getBuffers(self):
		return self.read_buffer, self.write_buffer
	def setName(self, new):
		self.name=new
	def setPipe(self, new):
		self.pipe=new
	def setMode(self, new):
		self.mode=new
	def isAlive(self):
		'''Returns alive thread:
		1=Reading
		2=Writing'''
		return self.proc



if __name__=="__main__":
	x=FIFO("test", pipe_in="in.bridge", pipe_out="out.bridge")
	print(x)
	while True:
		x.write(input(": "))
		print(x.read())
