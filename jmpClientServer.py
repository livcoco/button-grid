#!/usr/bin/env python2
import multiprocessing
from multiprocessing.managers import SyncManager

class Server:
    '''Server makes and registers two server queues and a lock [?? is lock
    needed? Doesn't appear to be used in Server. ??]. One queue is for
    receiving jobs (procedure calls) and one for returning results.

    Server also defines `respondToClientRequest(...)` which gets
    requests from queue, invokes a procedure, and returns results.

    Procedures can be invoked that are defined within this class or an
    inheriting class.

    '''
    portNum = 65001
    authKey = b'testMyServer'

    def __init__(self, sho0):
        self.typeString = type('jmpServer')
        self.serverManager = self.makeServerManager()
        self.sho0 = sho0

    def serverRun(self, sho1, sho2):
        while True:
            if sho1: print('Server is waiting for method call...')
            queueData = self.jobQ.get()
            if sho2: print('Server got: {}'.format(queueData))
            self.respondToClientRequest(queueData, self.resultQ)

    def makeServerManager(self):
        self.jobQ = multiprocessing.JoinableQueue(-1)
        self.resultQ = multiprocessing.JoinableQueue(-1)
        self.lock = multiprocessing.Lock()

        class JobQueueManager(SyncManager):
            pass

        JobQueueManager.register('get_job_q', callable=lambda: self.jobQ)
        JobQueueManager.register('get_result_q', callable=lambda: self.resultQ)
        JobQueueManager.register('get_lock', callable=lambda: self.lock)
        manager = JobQueueManager(address=('', self.portNum), authkey = self.authKey)
        manager.start()
        return manager

    def respondToClientRequest(self, methodNameAndArgs, resultsQ):
        if self.sho0:
            print ('To do:  respondToClientRequest({})'.format(methodNameAndArgs))
        try:
            methodName = methodNameAndArgs[0]
            #resultsQ.put(self.__dict__[methodName](self, *methodNameAndArgs[1:]) )
            resultsQ.put(self.__dict__[methodName](*methodNameAndArgs[1:]) )
        except Exception as ex:
            print('Got exception in Server when executing:', methodNameAndArgs, '  Exception=', ex)
            resultsQ.put(ex)

    # Define a Server method that prints RPC arguments
    def anRPC(self,*args):  print(args);  return 1

#=================================================================

class ServerQueueManager(SyncManager):
    pass

class Client:
    '''Client sets up 3 ServerQueueManager items, for sending jobs to a
    Server and getting results back.  Different servers need different
    port numbers.
    '''
    def __init__(self, ipAddress, portNum, authKey, sho7, sho8, sho9):
        '''ipAddress, portNum, authKey values must match those of the Server
        being connected to.  sho7-8-9 are booleans that control whether
        to show an init message (sho7); method call args (sho8) before call;
        and method call result (sho9) after call.
        '''
        self.ipAddress = ipAddress
        self.portNum   = portNum
        self.authKey   = authKey
        self.sho8      = sho8   # whether to show method call args
        self.sho9      = sho9   # whether to show method call results
        if sho7:
            print('Starting clientManager at IP {}:{} with authkey {}'.format(ipAddress, portNum, authKey))
        ServerQueueManager.register('get_job_q')
        ServerQueueManager.register('get_result_q')
        ServerQueueManager.register('get_lock')
        manager = ServerQueueManager(address=(ipAddress, portNum), authkey = authKey)
        manager.connect()
        self.jobQ = manager.get_job_q()
        self.resultQ = manager.get_result_q()
        self.lock = manager.get_lock()
        
    def serverMethodCall(self, args):
        '''Send job to a Server and get results back.  `args` is a list, with
        its first element being a server method name (a string), and other
        elements the parameters to that method.  Returns: job results
        '''
        try:
            self.lock.acquire()
            while not self.resultQ.empty(): # Make the result queue empty
                garbage = self.resultQueue.get()
            if self.sho8:
                print('SMC args:', args),
                if not self.sho9:  print()
            self.jobQ.put(args)             # Add job with args to job-queue
            result = self.resultQ.get()     # Get result of job
            if self.sho9:  print('SMC result:', result)
            return result
        finally:
            self.lock.release()

    def doRPC(self, *args):     # Handle variably-many arguments
        '''Call `serverMethodCall(self, args)` to send job to a Server and get
        results back.  `*args` is a variable number of arguments, the
        first being a server method name (a string), and the other
        arguments the parameters to that method.  Returns: job results
        '''
        return self.serverMethodCall(args)
            
if __name__ == '__main__':
    '''Brief tests for Client and Server, using port 65001.  The server in
    this test creates and registers an `add(x,y)` method.  The client
    in this test does 13 RPCs, computing Fibonacci numbers, then
    exits. '''
    import time
    import sys
    import signal
    def sigHandler(sig, frame):
        exit(0)
    signal.signal(signal.SIGINT, sigHandler) # Make a clean exit on ctrl-c

    if len(sys.argv) > 1:       # Run Server if there's a command line argument
        #--------------------------
        class testServer(Server):
            '''Subclass Server and define the methods we'll provide for service
            '''
            def __init__(self, sho0):
                print 'do super init'
                Server.__init__(self, sho0)
                print 'did super init'
                self.add = lambda x,y: x+y
                #self.add = testServer.add       # Alternative to lambda
            #def add(self, a, b):  return a + b  # Alternative to lambda
        #--------------------------
    
        print ('Creating Server')
        server = testServer(0)
        print ('Running Server')
        server.serverRun(0,0)
    else:                       # Run Client when there's no argument
        ipAddress = '127.0.0.1'
        portNum   = 65001           # must match Server's value
        authKey   = b'testMyServer' # must match Server's value
        print ('Try to start client')
        try:
            client = Client(ipAddress, portNum, authKey, 1,0,0)        
            print ('Started client, running "Fibonacci numbers test"')
            a, b = 1,1
            for t in range(13):
                r = client.doRPC('add', a, b)
                print('{} + {} = {}'.format(a,b,r))
                try:    r = int(r)
                except: r = 88
                a, b = b, r         # Gen. Fibonacci numbers
                time.sleep(.2)
            sys.exit(0)             # sys.exit will cause an exception
        except SystemExit:
            print ('Finished "Fibonacci numbers test"')
        except:
            print ('Client exception', sys.exc_info())
