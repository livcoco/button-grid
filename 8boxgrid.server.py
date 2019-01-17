#!/usr/bin/env python2

# 'Server' code for 8boxgrid - Creates server methods for 8boxgrid to
# invoke - jiw - Jan 2019 - Offered without warranty under GPL v3
# terms as at http://www.gnu.org/licenses/gpl.html

import sys
import jmpClientServer
import signal
def sigHandler(sig, frame):  sys.exit(0)
signal.signal(signal.SIGINT, sigHandler)  # Set up for clean exit on ctrl-c

# Set up and start my server, to respond to RPC requests from mpClient
class boxServer(jmpClientServer.Server):
    '''Subclass Server and define methods cat0...cat4 for service to client
    '''
    def __init__(self, shoI):
        jmpClientServer.Server.__init__(self, shoI)
        self.cat0 = lambda n,d,x,y: boxServer.jpText(self, 0,n,d,x,y) 
        self.cat1 = lambda n,d,x,y: boxServer.jpText(self, 1,n,d,x,y)
        self.cat2 = lambda n,d,x,y: boxServer.jpText(self, 2,n,d,x,y)
        self.cat3 = lambda n,d,x,y: boxServer.jpText(self, 3,n,d,x,y)
        self.cat4 = lambda n,d,x,y: boxServer.jpText(self, 4,n,d,x,y)
    
    def jpText(self,l,n,d,x,y):
        print('cat'+str(l),n,d,x,y)
        return l

print ('Creating Server')
server = boxServer(0)
print ('Running Server')
server.serverRun(0,0)
