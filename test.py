import Pyro4
import sys
import os


# uri = input("Enter the uri of the jebret: ").strip()
uri ="PYRONAME:filesystem.middleware"
jebret = Pyro4.Proxy(uri)
# input=raw_input()
currdir="./"
currserver=""
# print(./)

while True:
	commands = []
	print (currdir+'# '),
	command = raw_input()
	commands.extend(command.split(' '))
	# print commands

	if commands[0] == 'ls':
		if len(commands)==1:
			for i in jebret.listdir(currdir):
				print(i)
		else:
			kontol=commands[1]
			split = kontol.split()[0]

			if split[0]=="/":
				# jebret.changedirectory(currdir)
				print('.'+commands[1])
				for i in jebret.listdir('.'+commands[1]):
					if i != "list tidak ada":
						print(i)
				# print(currdir)
			else:
				if currdir == "./":
					# print(currdir+""+commands[1])
					a=0
					for i in jebret.listdir(currdir+""+commands[1]):
						if i != "list tidak ada":
							print(i)
						else: 
							a+=1
					if len(jebret.listdir(currdir+""+commands[1])) == a: 
						print "tidak ada"

				else:
					a=0
					for i in jebret.listdir(currdir+'/'+commands[1]):
						if i != "list tidak ada":
							print(i)
						else: 
							a+=1
					# print("nilai a ->",a)
					if len(jebret.listdir(currdir+'/'+commands[1])) == a: 
						print "tidak ada"


					# print (currdir+'/'+commands[1])
					# for i in jebret.listdir(currdir+'/'+commands[1]):
					# 	# print(i)
					# 	if i != "tidak ada":
					# 		print("a")
					# 	else:
					# 		print("file ga ada")

					# currdir=currdir+"/"+commands[1]

		
		
	elif commands[0] == 'touch':
		jebret.makefile(currdir+'/'+commands[1])
		
	elif commands[0] == 'rm':
		if commands[1] == '-rf':
			jebret.removedir(currdir+'/'+commands[2])
			print(currdir+'/'+commands[2])
		else:
			jebret.removefile(currdir+'/'+commands[1])

	elif commands[0] == 'cd':
		if len(commands)==1:
			currdir="./"
			currserver=""
		else:
			kontol=commands[1]
			split = kontol.split()[0]
			# print(split)
			if commands[1] == "..":

				res=currdir.split("/")
				print(res)
				tot=currdir.split("/"+res[len(res)-1])
				print(tot)
				currdir=tot[0]+"/"

			elif split[0]=="/":
				# jebret.changedirectory(currdir)
				if jebret.changedirectory("."+commands[1]):
					currdir="."+commands[1]
				else:
					print("Tidak ada")
				
				# print(currdir)
			else:
				if currdir == "./":
					if jebret.changedirectory(currdir+""+commands[1]):
						currdir=currdir+""+commands[1]
					else:
						print("Tidak ada")
					
				else:
					if jebret.changedirectory(currdir+"/"+commands[1]):
						currdir=currdir+"/"+commands[1]
					else:
						# jebret.changedirectory(currdir+"/"+commands[1])
						print("Tidak ada")



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