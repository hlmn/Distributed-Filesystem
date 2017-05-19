import Pyro4
import sys
import os


# uri = input("Enter the uri of the jebret: ").strip()
uri ="PYRONAME:filesystem.middleware"
jebret = Pyro4.Proxy(uri)
# input=raw_input()
currdir="./"

while True:
	commands = []
	print currdir+'# ',
	command = raw_input()
	commands.extend(command.split(' '))
	# print commands

	if commands[0] == 'ls':
		if len(commands)==1:
			for i in jebret.listdir(currdir):
				print(i)
		else:
			for i in jebret.listdir(currdir+''+commands[1]):
				print(i)

		
		
	elif commands[0] == 'touch':
		jebret.makefile(commands[1])
	elif commands[0] == 'rm':
		jebret.removefile(currdir+'/'+commands[1])
	elif commands[0] == 'cd':
		print jebret.changedirectory(commands[1])
	elif commands[0] == 'cp':
		if '/' in commands[2]:
			var1 = commands[2].split('/')[0]
			var2 = commands[2].split('/')[1]
			jebret.copy(currdir+'/'+commands[1], currdir+'/'+var1+'/'+var2)
		elif os.path.isdir(commands[2]):
			jebret.copy(currdir+'/'+commands[1], currdir+'/'+commands[2]+'/'+commands[1])
		else:
			jebret.copy(currdir+'/'+commands[1], currdir+'/'+commands[2])

	elif commands[0] == 'mv':
		if '/' in commands[2]:
			var1 = commands[2].split('/')[0]
			var2 = commands[2].split('/')[1]
			jebret.move(currdir+'/'+commands[1], currdir+'/'+var1+'/'+var2)	
		elif os.path.isdir(commands[2]):
			jebret.move(currdir+'/'+commands[1], currdir+'/'+commands[2]+'/'+commands[1])
		else:
			jebret.move(currdir+'/'+commands[1], currdir+'/'+commands[2])

			
		# removefile(currdir+'/'+commands[1])

	else:
		break