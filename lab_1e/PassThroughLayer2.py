from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
import playground

class PassThroughLayer2(StackingProtocol):
    
    def connection_made(self, transport):
        self.transport = transport
        print("PassThroughLayer2: connection_made called, sending higher transport to ClientDemo")
        higherTransport = StackingTransport(self.transport)
        self.higherProtocol().connection_made(higherTransport)
    
    def data_received(self, data):
        print("PassThroughLayer2: data received from the other side.")
        self.higherProtocol().data_received(data)

    def connection_lost(self):
        print("PassThroughLayer2: connection lost")
        self.higherProtocol().connection_lost()