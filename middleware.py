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
                    print(i)
        return a

    def changedirectory(self, currdir, server = None):
        a = False
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkdir(currdir):
                    print("kontol")
                    a = True
        return a

    #Define dst path file yang baru (misal 'folde1/' -> 'folder1/fileName', misal 'folder1' -> 'folder1/fileName')
    def fullPath(dst,fileName):
        kirim = {}
        #Case path -> 'folder1'
        if dst[len(dst)-1] != '/':
            kirim = dst + '/' + filename
        #Case path -> 'folder1/'
        else: 
            kirim = dst + filename
        return kirim

    #Send File, DST Server, src(src file yang mau di copy), dst(dst path in server)
    def pyroSendFile(server, src, dst, isifile):
        with Pyro4.Proxy(server) as storage:
            #Folder udah ada, nama file di src di tambah ke dst
            if storage.checkdir(dst) == True:
                fileName = src.split('/').pop()
                kirim = fullPath(dst,fileName)
                #kirim file ke tujuan
                storage.recvfile(isifile,kirim)
            #Folder belum ada
            elif storage.checkdir(dst) == False:
                #File ga ada
                if storage.checkfile(dst) == False:
                    kirim = dst
                    #kirim file ke tujuan
                    storage.recvfile(isifile,kirim)
            

    def copy(self, src, dst):
        isifile = ''
        print ('src-->'+ src)
        print ('dst-->'+ dst)
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkfile(src) == True:
                    isifile = storage.sendfile(src)
                    print ('masuk if di middleware')
                else:
                    continue
        for server in self.serverlist:
            pyroSendFile(server, src, dst, isifile)

    def move(self, src, dst):
        isifile = ''
        print ('src-->'+ src)
        print ('dst-->'+ dst)
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkfile(src) == True:
                    isifile = storage.sendfile(src)
                    # kirim = pickle.dumps(isifile)
                else:
                    continue
        for server in self.serverlist:
             pyroSendFile(server, src, dst, isifile)
        self.removefile(src)

    # def copy(self, src, dst):
    #     isifile = ''
    #     print ('src-->'+ src)
    #     print ('dst-->'+ dst)
    #     for server in self.serverlist:
    #         with Pyro4.Proxy(server) as storage:
    #             if storage.checkfile(src) == True:
    #                 isifile = storage.sendfile(src)
    #                 print ('masuk if di middleware')
    #             else:
    #                 continue
    #     for server in self.serverlist:
    #         if dst.split('/')[-1] != src:
    #             print ('masuk if cuk')
    #             filename = dst.split('/')[-1]
    #             kirim = dst
    #             print (filename)
    #             print (dst)
    #             print('check '+kirim+'\n isifile: '+isifile)
    #         else:
    #             print ('masuk else cuk')
    #             filename = src.split('/').pop()
    #             if dst[len(dst)-1] != '/': #misal dst nya ga ada slash
    #                 kirim = dst + '/' + filename
    #             else: #misal dst nya ada slash
    #                 kirim = dst + filename
    #             print (filename)
    #             print (dst)
    #             print('check '+kirim+'\n isifile: '+isifile)
    #         with Pyro4.Proxy(server) as storage:
    #             print (storage.checkfile(kirim))
    #             print (storage.checkdir(dst))
    #             if storage.checkfile(kirim) == False and storage.checkdir(dst) == True:
    #                 print ('ini mau dikirim-->'+isifile)
    #                 storage.recvfile(isifile, kirim)
    #                 # print(src)
    #                 # self.removefile(src)
    #             elif storage.checkfile(kirim) == False and storage.checkdir(dst) == False:
    #                 print ('ini mau dikirim2-->'+isifile)
    #                 storage.recvfile(isifile, kirim)
    #             else:
    #                 continue

    # def move(self, src, dst):
    #     isifile = ''
    #     print ('src-->'+ src)
    #     print ('dst-->'+ dst)
    #     for server in self.serverlist:
    #         with Pyro4.Proxy(server) as storage:
    #             if storage.checkfile(src) == True:
    #                 isifile = storage.sendfile(src)
    #                 # kirim = pickle.dumps(isifile)
    #             else:
    #                 continue
    #     for server in self.serverlist:
    #         filename = src.split('/').pop()
    #         if dst[len(dst)-1] != '/':
    #             kirim = dst + '/' + filename
    #         else:
    #             kirim = dst + filename
    #         print (filename)
    #         print (dst)
    #         print('check '+kirim+'\n isifile: '+isifile)
    #         with Pyro4.Proxy(server) as storage:
    #             print (storage.checkfile(kirim))
    #             print (storage.checkdir(dst))
    #             if storage.checkfile(kirim) == False and storage.checkdir(dst) == True:
    #                 print ('ini mau dikirim-->'+isifile)
    #                 storage.recvfile(isifile, kirim)
    #                 self.removefile(src)
    #             else:
    #                 continue

    def makefile(self, currdir): 
        serversize = {} 
        for server in self.serverlist: 
            with Pyro4.Proxy(server) as storage:
                serversize[server] = storage.size() 
        sorted_x = sorted(serversize.items(), key=operator.itemgetter(1)) 
        # print (sorted_x[0][0]) 
        with Pyro4.Proxy(sorted_x[0][0]) as storage: 
            storage.makefile(currdir) 

    def check(self, currdir, storage = None):
        return storage.check(currdir)


    def removefile(self, currdir):
        a = False
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkfile(currdir):
                    print("kontol")
                    storage.removefile(currdir)
                    a = True

        return a

    def removedir(self, currdir):
        a = False
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                if storage.checkdir(currdir):
                    print("kontol")
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
})
