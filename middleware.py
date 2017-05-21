from __future__ import print_function
import operator
try:
    import queue
except ImportError:
    import Queue as queue
import Pyro4
from Pyro4.util import SerializerBase
# from workitem import Workitem


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
                    if i == "server.py":
                        continue
                    a.append(i)
                    print(i)
        return a

    def makefile(self, currdir):
        serversize = {}
        for server in self.serverlist:
            with Pyro4.Proxy(server) as storage:
                serversize[server] = storage.size()
        sorted_x = sorted(serversize.items(), key=operator.itemgetter(1))
        # print (sorted_x[0][0])
        with Pyro4.Proxy(sorted_x[0][0]) as storage:
            storage.makefile(currdir)

        return a

        # print (serversize)
    # def changedirectory(self, currdir, server = None):
    #     for server in self.serverlist:
    #         with Pyro4.Proxy(server) as storage:
    #             for i in storage.listdir(currdir):
    #                 if i == "server.py":
    #                     continue
    #                 a.append(i)
    #     return 


# main program

Pyro4.Daemon.serveSimple({
    DispatcherQueue: "filesystem.middleware"
})
