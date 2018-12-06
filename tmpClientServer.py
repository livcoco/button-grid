#!/usr/bin/python2
import multiprocessing
from multiprocessing.managers import SyncManager

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
    def cat4(self, n, d, x, y):
        print ('cat3', n, d, x, y); return 3

    def makeServerManager(self):
        show = 0
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
        try:
            manager.start()
        except:
            print 'makeServerManager .start exception', sys.exc_info()
            raise
        print('started server manager')
        return manager

    def respondToClientRequest(self, methodNameAndArgs, sharedResultQ):
        show = 0
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
            
class TestServer(_TestServer):
    portNum = 65001
    #portNum = 8084
    authKey = b'testMyServer'
    def __init__(self):
        try:
            _TestServer.__init__(self)
            self.run()
        except:
            print 'TestServer init exception', sys.exc_info()
            raise
        
    def run(self):
        show = 0
        try:
            self.serverManager = self.makeServerManager()
        except:
            print 'TestServer run exception', sys.exc_info()
            raise
        
        while True:
            if show: print('waiting for method call...')
            queueData = self.jobQ.get()
            self.respondToClientRequest(queueData, self.resultQ)

#=================================================================
class TestClientGeneric:
    def serverMethodCall(self, args):
        show = 0
        try:
            self.lock.acquire()
            while not self.resultQ.empty(): # Make the result queue empty
                garbage = self.resultQueue.get()
            if show: print('in serverMethodCall with args', args)
            self.jobQ.put(args)             # Add job with args to job-queue
            data = self.resultQ.get()       # Get result of job
            return data
        finally:
            self.lock.release()

    def makeClientManager(self, ipAddress, portNum, authKey):
        class ServerQueueManager(SyncManager):
            pass

        show = 0
        ServerQueueManager.register('get_job_q')
        ServerQueueManager.register('get_result_q')
        ServerQueueManager.register('get_lock')
        if show: print('starting clientManager at address', (ipAddress, portNum), 'with authkey', authKey)
        manager = ServerQueueManager(address=(ipAddress, portNum), authkey = authKey)
        manager.connect()
        if show: print('client connected to %s:%s'%(ipAddress, portNum))
        return manager

    def startClient(self, ipAddress, portNum, authKey):
        self.manager = self.makeClientManager(ipAddress, portNum, authKey)
        self.jobQ = self.manager.get_job_q()
        self.resultQ = self.manager.get_result_q()
        self.lock = self.manager.get_lock()

class TestClient(TestClientGeneric):
    def __init__(self):
        self.ipAddress = '127.0.0.1'
        self.portNum = TestServer.portNum
        self.authKey = TestServer.authKey
        print('authKey', self.authKey)
        self.startClient(self.ipAddress, self.portNum, self.authKey)
        
    def doOp2(self, op, a, b):
        return self.serverMethodCall((op, a, b))
    
    def doOp4(self, op, n, d, x, y):
        return self.serverMethodCall((op, n, d, x, y))
            
if __name__ == '__main__':
    # Brief tests for client and server.  If attempt to start a server
    # fails, start client.  The client in this test does 13 RPCs,
    # computing Fibonacci numbers, then exits.
    import time
    import sys
    import signal
    def sigHandler(sig, frame):
        exit(0)
    signal.signal(signal.SIGINT, sigHandler) # Make a cleaner exit on ctrl-c

    serverRunning = False
    try:
        print 'Try to start Server'
        server = TestServer()
        print 'Started Server'
        serverRunning = True    # Got it started
    except:
        print 'Server exception', sys.exc_info()
    if not serverRunning:
        client = TestClient()
        print 'Started client'
        a, b = 1,1
        for t in range(13):
            r = client.doOp2('add', a, b)
            print('{} + {} = {}'.format(a,b,r))
            a, b = b, r         # Gen. Fibonacci numbers
            time.sleep(1)
        sys.exit(0)