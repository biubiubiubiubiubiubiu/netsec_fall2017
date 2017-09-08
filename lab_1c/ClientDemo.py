from customerEnd import *
from serverEnd import *
from playground.network.packet import PacketType
class CustomerClientProtocol:

    def __init__(self, customerName, tableNumber):
        self.transport = None
        self.customerName = customerName
        self.tableNumber = tableNumber
    
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        print("Customer: Connection made to a restaurant!")
    
    def dataReceived(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print("Customer: Received another packet!")
            print("Packet type: {!r}".format(type(pkt)))

    def requestMenu(self):
        request = RequestMenu();
        request.tableNumber = self.tableNumber
        request.name = self.customerName 
        print("Sending menu request... Name: {!r}, tableNumber: {!r}".format(request.name, \
                                                                             request.tableNumber))
        self.transport.write(request.__serialize__())

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')