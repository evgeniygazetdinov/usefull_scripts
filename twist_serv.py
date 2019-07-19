from autobahn.twisted.websocket import WebSocketServerProtocol


class MyServerProtocol(WebSocketServerProtocol):
    def onMessage(self,payload,isBinary):
        self.send_message(payload,isBinary)





if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor
   log.startLogging(sys.stdout)

   from autobahn.twisted.websocket import WebSocketServerFactory
   factory = WebSocketServerFactory()
   factory.protocol = MyServerProtocol

   reactor.listenTCP(9000, factory)
   reactor.run()
