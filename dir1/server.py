import os
import socket
import signal
import sys

import Pyro4
from shutil import copyfile


# currdir = os.path.abspath('./')

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Jebret(object):
	tot = None

	def __init__(self):
		self.daemon = None
		print("kontol")

	def listdir(self, currdir):
		a=[]
		print(self.daemon)
		try:
			for i, file in enumerate(os.listdir(currdir)):
				a.append(file)
		except Exception:
			return a.append("titdak ada")
		finally:
			return a
	#touch
	def makefile(self, path):
	    with open(path, 'a'):
		    return os.utime(path, None)

	#rm
	def removefile(self, path):
		return os.remove(path)

	#cd
	def changedirectory(self, path):
		print path
		# os.chdir(currdir+''+path)
		for i, file in enumerate(os.listdir(currdir+'/'+path)):
			print file

		# currdir = os.path.abspath('.')
		# return currdir
		

	#cp
	def copy(self, src, dst):
		# print src, dst
		copyfile(src, dst)

	#mv
	def move(self, src, dst):
		os.rename(src, dst)

	def putUri(self, uri):
		self.daemon = uri
		print(self.daemon)
	
	def size(self):
		total_size = 0
		for dirpath, dirnames, filenames in os.walk("."):
		    for f in filenames:
		        fp = os.path.join(dirpath, f)
		        total_size += os.path.getsize(fp)	
		return total_size


def main():
	with Pyro4.Daemon(host="0.0.0.0") as daemon:
	    worker_name = "Worker_%d@%s" % (os.getpid(), socket.gethostname())
	    print("Starting up worker", worker_name)
	    uri = daemon.register(Jebret)
	    ns = Pyro4.locateNS()
	    ns.register(worker_name, uri, metadata={"server"})
	    middleware = Pyro4.Proxy("PYRONAME:filesystem.middleware")
	    total_size = 0
	    for dirpath, dirnames, filenames in os.walk("."):
	        for f in filenames:
	            fp = os.path.join(dirpath, f)
	            total_size += os.path.getsize(fp)
	    tae=Pyro4.async(middleware)
	    tae.putWork(uri.asString(), total_size)

	    try:
	    	
	    	daemon.requestLoop()
	    except KeyboardInterrupt:
	    	raise KeyboardInterrupt('a')
	    finally:
	    	ns.remove(worker_name)
	    	middleware.removeWork(uri.asString())
			
	
			
    
    
	

if __name__=="__main__":
    main()


