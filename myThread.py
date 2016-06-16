import threading
from time import ctime,sleep

class MyThread(threading.Thread):
	"""docstring for MyThread"""
	def __init__(self,func,args,name=''):
		super(MyThread, self).__init__()
		self.name = name
		self.func = func
		self.args = args

	def getResult(self):
		return self.res
	
	def run(self):
		print 'starting',self.name, 'at:', ctime()
		self.res = self.func(*self.args)
		print self.name, 'finished at:', ctime()		

def loop():
	print 'start loop'
	sleep(2)
	print 'end loop'
t = MyThread(loop,[],name='test thread')
t.start()
t.join()