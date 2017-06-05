from __future__ import print_function
import os

try:
    import queue
except ImportError:
    import Queue as queue
import Pyro4
from Pyro4.util import SerializerBase
# from workitem import Workitem
import operator


# For 'workitem.Workitem' we register a deserialization hook to be able to get these back from Pyro
# SerializerBase.register_dict_to_class("workitem.Workitem", Workitem.from_dict)


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class DispatcherQueue(object):
    def __init__(self):
        self.serverlist = {}
        self.resultqueue = {}
        print(self.serverlist)
        

    def putWork(self, item, totalsize):
        self.serverlist[item]=totalsize
        # print(self.serverlist[item])
        put=Pyro4.Proxy(""+item)
        put.putUri(""+item)
        print(self.serverlist)

    def removeWork(self, item):
        del self.serverlist[item]
        print(self.serverlist)

    def listdir(self, currdir):
        a=[]
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                for i in storage.listdir(currdir):
                    if i == "server.py" or i == "list tidak ada":
                        continue
                    a.append(i)
                    # print(i)
        return a

    def changedirectory(self, currdir, server = None):
        a = False
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkdir(currdir):
                    a = True
        return a

    def move(self, src, dst):
        isifile = ''
        # print ('src-->'+ src)
        # print ('dst-->'+ dst)
        serversize = {}
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:                
                if storage.checkfile(src) == True:
                    isifile = storage.sendfile(src)
                    # print ('masuk if di middleware')
                    serversize[server] = storage.size()
                else:
                    continue
        sorted_x = sorted(serversize.items(), key=operator.itemgetter(1))
                 
        for server in self.serverlist:
            # print (src)
            # print ("=================")
            # print (src.split('/').pop())
            # print ("=================")
            # print (dst.split('/')[-1])
            # print ("=================")
            # print (dst)
            # print (dst.split('/'))

            cekcek = (dst.split('/'))
            cekcek.reverse()

            variab1=False
            ea = cekcek[len(cekcek)-2]
            print(ea)

            for varbagus in self.serverlist:
                with Pyro4.Proxy(varbagus) as variab2:
                    if variab2.checkdir(ea):
                        variab1=True
                        servervariab1=varbagus
            
            with Pyro4.Proxy(server) as storage:
                variab = False
                if storage.checkdir(dst.split('/')[-1]) == False:
                    variab = False
                elif storage.checkdir(dst.split('/')[-1]) == True:
                    variab = True
                
                if variab == False and dst.split('/')[-1] != src.split('/').pop(): #kalo ganti nama
                    if dst.split('/')[-1] == ".":
                        filename = src.split('/').pop()
                        if dst[len(dst)-1] != '/': #misal dst nya ga ada slash
                            kirim = dst + '/' + filename
                        else: #misal dst nya ada slash
                            kirim = dst + filename
                        print (filename)
                        print (dst)
                        print('check '+kirim+'\n isifile: '+isifile)
                    else:
                        filename = dst.split('/')[-1]
                        kirim = dst
                        print (filename)
                        print (dst)
                        print('check '+kirim+'\n isifile: '+isifile)


                else:
                    filename = src.split('/').pop()
                    if dst[len(dst)-1] != '/': #misal dst nya ga ada slash
                        kirim = dst + '/' + filename
                    else: #misal dst nya ada slash
                        kirim = dst + filename
                    print (filename)
                    print (dst)
                    print('check '+kirim+'\n isifile: '+isifile)

                if variab1 is True:
                    with Pyro4.Proxy(servervariab1) as storage:
                    # serversize[server] = storage.size() 
                    # sorted_x = sorted(serversize.items(), key=operator.itemgetter(1))

                        print (storage.checkfile(kirim))
                        print (storage.checkdir(dst))
                        if storage.checkfile(kirim) == False and storage.checkdir(dst) == True:
                            print ('ini mau dikirim-->'+isifile)
                            storage.recvfile(isifile, kirim)
                            self.removefile(src)
                            # self.removefile(src)
                            # print(src)
                            # self.removefile(src)
                        elif storage.checkfile(kirim) == False and storage.checkdir(dst) == False:
                            print ('ini mau dikirim2-->'+isifile)
                            storage.recvfile(isifile, kirim)
                            self.removefile(src)
                            # self.removefile(src)
                        else:
                            continue
                else:

                    with Pyro4.Proxy(sorted_x[0][0]) as storage:
                        # serversize[server] = storage.size() 
                        # sorted_x = sorted(serversize.items(), key=operator.itemgetter(1))
                        print (storage.checkfile(kirim))
                        print (storage.checkdir(dst))
                        if storage.checkfile(kirim) == False and storage.checkdir(dst) == True:
                            print ('ini mau dikirim-->'+isifile)
                            storage.recvfile(isifile, kirim)
                            self.removefile(src)
                            # self.removefile(src)
                            # print(src)
                            # self.removefile(src)
                        elif storage.checkfile(kirim) == False and storage.checkdir(dst) == False:
                            print ('ini mau dikirim2-->'+isifile)
                            storage.recvfile(isifile, kirim)
                            self.removefile(src)
                            # self.removefile(src)
                        else:
                            continue

    def copy(self, src, dst):
        isifile = ''
        print ('src-->'+ src)
        print ('dst-->'+ dst)
        serversize = {}
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:                
                if storage.checkfile(src) == True:
                    isifile = storage.sendfile(src)
                    print ('masuk if di middleware')
                    serversize[server] = storage.size()
                else:
                    continue
        sorted_x = sorted(serversize.items(), key=operator.itemgetter(1))
                 
        for server in self.serverlist:
            # print (src)
            # print ("=================")
            # print (src.split('/').pop())
            # print ("=================")
            # print (dst.split('/')[-1])
            # print ("=================")
            # print (dst)
            # print (dst.split('/'))

            cekcek = (dst.split('/'))
            cekcek.reverse()
            folderFlag = False
            folderName = cekcek[len(cekcek)-2]
            print(folderName)

            for server in self.serverlist:
            
                with Pyro4.Proxy(server) as storage:
                
                    if storage.checkdir(folderName):
                    
                        folderFlag = True
                        serverDst=server
                        

            with Pyro4.Proxy(server) as storage:
                folderFlag2 = False
                variab = False
                if storage.checkdir(dst.split('/')[-1]) == False:
                    folderFlag2 = False
                elif storage.checkdir(dst.split('/')[-1]) == True:
                    folderFlag2 = True

                if folderFlag2 == False and dst.split('/')[-1] != src.split('/').pop(): #kalo ganti nama
                    if dst.split('/')[-1] == ".":
                        filename = src.split('/').pop()
                        if dst[len(dst)-1] != '/': #misal dst nya ga ada slash
                            kirim = dst + '/' + filename
                        else: #misal dst nya ada slash
                            kirim = dst + filename
                        print (filename)
                        print (dst)
                        print('check '+kirim+'\n isifile: '+isifile)
                    else:
                        filename = dst.split('/')[-1]
                        
                        kirim = dst
                        print (filename)
                        print (dst)
                        print('check '+kirim+'\n isifile: '+isifile)


                else:
                    filename = src.split('/').pop()
                    if dst[len(dst)-1] != '/': #misal dst nya ga ada slash
                        kirim = dst + '/' + filename
                    else: #misal dst nya ada slash
                        kirim = dst + filename
                    print (filename)
                    print (dst)
                    print('check '+kirim+'\n isifile: '+isifile)

                if folderFlag is True:
                    print(serverDst)
                    with Pyro4.Proxy(serverDst) as storage:
                        print (storage.checkfile(kirim))
                        print (storage.checkdir(dst))
                        if storage.checkfile(kirim) == False and storage.checkdir(dst) == True:
                            print ('ini mau dikirim-->'+isifile)
                            storage.recvfile(isifile, kirim)
                        elif storage.checkfile(kirim) == False and storage.checkdir(dst) == False:
                            print ('ini mau dikirim2-->'+isifile)
                            storage.recvfile(isifile, kirim)
                        else:
                            continue
                else:
                    with Pyro4.Proxy(sorted_x[0][0]) as storage:
                        # serversize[server] = storage.size() 
                        # sorted_x = sorted(serversize.items(), key=operator.itemgetter(1))
                        print (storage.checkfile(kirim))
                        print (storage.checkdir(dst))
                        if storage.checkfile(kirim) == False and storage.checkdir(dst) == True:
                            print ('ini mau dikirim-->'+isifile)
                            storage.recvfile(isifile, kirim)
                            # self.removefile(src)
                            # self.removefile(src)
                            # print(src)
                            # self.removefile(src)
                        elif storage.checkfile(kirim) == False and storage.checkdir(dst) == False:
                            print ('ini mau dikirim2-->'+isifile)
                            storage.recvfile(isifile, kirim)
                            # self.removefile(src)
                            # self.removefile(src)
                        else:
                            continue



    

    def makefile(self, currdir, dst): 
        serversize = {}
        dira = list(dst)
        # print (dira)
        if dira[0] == '/':
            # print(dira)
            dira.reverse()
            # print("======")
            # print(dira.pop())
            dira.reverse()
            oo = True
        else:
            oo = False
        print (currdir)
        cekcek = (currdir.split('/'))
        cekcek.reverse()
        print ("asdasd", cekcek)
        folderFlag = False
        folderName = cekcek[len(cekcek)-2]
        print(ea)
        print(folderName)
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkdir(folderName):
                    folderFlag = True
                    serverDst = server


        if folderFlag==False or oo==True:   
            for server in self.serverlist: 
                with Pyro4.Proxy(server) as storage:
                    serversize[server] = storage.size() 
            sorted_x = sorted(serversize.items(), key=operator.itemgetter(1)) 
            # print (sorted_x[0][0]) 
            with Pyro4.Proxy(sorted_x[0][0]) as storage: 
                storage.makefile(''.join(dira)) 
        else:
            with Pyro4.Proxy(serverDst) as storage: 
                storage.makefile(currdir) 

    def check(self, currdir, storage = None):
        return storage.check(currdir)


    def removefile(self, currdir):
        a = False
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkfile(currdir):
                    storage.removefile(currdir)
                    a = True

        return a

    def removedir(self, currdir):
        a = False
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkdir(currdir):
                    storage.removedir(currdir)
                    a = True

        return a

    def checkfile(self, dir):
        return os.path.isfile(dir)

    def checkdir(self, dir):
        return os.path.isdir(dir)           

        

    

# main program

Pyro4.Daemon.serveSimple({
    DispatcherQueue: "filesystem.middleware"
},)

