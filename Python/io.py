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
		self.buffers=['', '']
		self.proc=0  #0=Clear; 1=Reading; 2=Writing;
		self.mode=mode  #0=Kill thread; 1=Read; 2=Write; 3=turretThread
		self.thread=None
		#Starts thread & set's read/write function
		if self.mode==3:  #Turret Mode!
			self.thread=threading.Thread(name=f"{self.name}",\
			target=self.turretThread,\
			daemon=self.daemon)
			self.thread.start()
			self.read=self.bufferRead

		elif not self.block:  #Using thread
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
buffers: {self.buffers}'''

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
			self.buffers[0]+=f.read()
		self.proc=0
		return self.buffers[0]
	def writePipe(self):
		'''Writes to pipe'''
		self.proc=2
		with open(self.pipe, 'w') as f:
			while self.buffers[1]=='':
				time.sleep(0.1)  #Time buffer
			f.write(self.buffers[1])
		toRet, self.buffers[1]=self.buffers[1], ''
		self.proc=0
		return self.buffers[1]

	def readBlocking(self):
		'''Reads through pipe'''
		toRet=readPipe()
		self.buffers[1]=''
		return toRet
	def writeBlocking(self, toWrite=None):
		'''Writes through pipe'''
		return writePipe(toWrite)
	def readNoBlocking(self):
		'''Returns self.buffers[0] if not ""'''
		if self.buffers[0]!='':
			toRet, self.buffers[0]=self.buffers[0], ''
			return toRet
		else:
			return None
	def writeNoBlocking(self, toWrite=None):
		'''Starts writing thread, if not started.
		Returns True is write was put through.
		Returns False if thread was already writing
		Returns None if currently reading'''
		if toWrite!=None:
			self.buffers[1]=toWrite
		return True
	def turretThread(self):
		'''Reads indefinitely, constantly writing to read_buffer'''
		with open(self.pipe, 'r') as f:
			while True:
				self.buffers[0]+=f.readline()
	def bufferRead(self):
		'''Reads from buffer, then clears it.
		Mainly used with turretThread'''
		toRet, self.buffers[0]=self.buffers[0], ''
		if toRet=='':
			return None
		else:
			return toRet

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
		return self.buffers
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
	x=FIFO("test", pipe="test.bridge", mode=3, daemon=True)
	while True:
		input("Press enter to read...")
		print(f"{x.read()} | {x.buffers[0]}", end='')
