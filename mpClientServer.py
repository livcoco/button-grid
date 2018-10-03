#!/usr/bin/python3
import multiprocessing
from multiprocessing.managers import SyncManager

class BorgTestServer:
    _sharedState = {}
    def __init__(self):
        self.__dict__ = self._sharedState

class _TestServer:
    def __init__(self):
        self.typeString = type('asdf')

    def add(self, a, b):        return a + b
    def sub(self, a, b):        return b - a
    def mul(self, a, b):        return a * b
    def div(self, a, b):        return b // a
    def cat0(self, n, d, x, y):
        print ('cat0', n, d, x, y); return 0
    def cat1(self, n, d, x, y):
        print ('cat1', n, d, x, y); return 1
    def cat2(self, n, d, x, y):
        print ('cat2', n, d, x, y); return 2
    def cat3(self, n, d, x, y):
        print ('cat3', n, d, x, y); return 3

    def makeServerManager(self):
        show = True
        self.jobQ = multiprocessing.JoinableQueue(-1)
        self.resultQ = multiprocessing.JoinableQueue(-1)
        self.lock = multiprocessing.Lock()

        class JobQueueManager(SyncManager):
            pass

        JobQueueManager.register('get_job_q', callable=lambda: self.jobQ)
        JobQueueManager.register('get_result_q', callable=lambda: self.resultQ)
        JobQueueManager.register('get_lock', callable=lambda: self.lock)
        if show: print('starting manager with address =', ('', self.portNum), ', authkey', self.authKey)
        manager = JobQueueManager(address=('', self.portNum), authkey = self.authKey)
        manager.start()
        print('started server manager')
        return manager

    def respondToClientRequest(self, methodNameAndArgs, sharedResultQ):
        show = True
        if show: print('in respondToClientRequest() with', methodNameAndArgs)
        try:
            if type(methodNameAndArgs) == self.typeString:
                self.execResult = None
                exec('self.execResult = ' + methodNameAndArgs)
            else:
                methodName = methodNameAndArgs[0]
                sharedResultQ.put(_TestServer.__dict__[methodName](self, *methodNameAndArgs[1:]) )
        except Exception as ex:
            print('received exception in TestServer when', methodNameAndArgs, 'executed.  returning exception', ex)
            sharedResultQ.put(ex)
            
class TestServer(BorgTestServer, _TestServer):
    portNum = 65001
    #portNum = 8084
    authKey = b'testMyServer'
    def __init__(self):
        BorgTestServer.__init__(self)
        if self._sharedState:
            return
        _TestServer.__init__(self)
        self.run()
        
    def run(self):
        show = True
        self.serverManager = self.makeServerManager()
        while True:
            if show: print('waiting for method call...')
            queueData = self.jobQ.get()
            self.respondToClientRequest(queueData, self.resultQ)

#=================================================================
class TestClientGeneric:
    def startClient(self, ipAddress, portNum, authKey):
        self.manager = self.makeClientManager(ipAddress, portNum, authKey)
        self.jobQ = self.manager.get_job_q()
        self.resultQ = self.manager.get_result_q()
        self.lock = self.manager.get_lock()

    def makeClientManager(self, ipAddress, portNum, authKey):
        show = True
        class ServerQueueManager(SyncManager):
            pass

        ServerQueueManager.register('get_job_q')
        ServerQueueManager.register('get_result_q')
        ServerQueueManager.register('get_lock')

        if show: print('starting clientManager at address', (ipAddress, portNum), 'with authkey', authKey)

        manager = ServerQueueManager(address=(ipAddress, portNum), authkey = authKey)
        manager.connect()
        if show: print('client connected to %s:%s'%(ipAddress, portNum))
        return manager

    def serverMethodCall(self, args):
        show = True
        try:
            self.lock.acquire()
            while not self.resultQ.empty():
                garbage = self.resultQueue.get()
            #if show: print('in serverMethodCall with args', args)
            self.jobQ.put(args)
            data = self.resultQ.get()
            return data
        finally:
            self.lock.release()

class TestClient(TestClientGeneric):
    def __init__(self):
        self.ipAddress = '127.0.0.1'
        self.portNum = TestServer.portNum
        self.authKey = TestServer.authKey
        print('authKey', self.authKey)
        self.startClient(self.ipAddress, self.portNum, self.authKey)
        
    def doOp2(self, op, a, b):  return self.serverMethodCall((op, a, b))
    
    def doOp4(self, c, n, d, x, y):
        return self.serverMethodCall((c, n, d, x, y))
            
if __name__ == '__main__':
    ts = TestServer()
