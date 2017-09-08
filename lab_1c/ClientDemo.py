from customerEnd import *
from serverEnd import *
from playground.network.packet import PacketType
class CustomerClientProtocol:

    def __init__(self, customerName, tableNumber):
        self.transport = None
        self.customerName = customerName
        self.tableNumber = tableNumber
        self.receivedMenu = None
    
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        print("Customer: Connection made to a restaurant!")
    
    def dataReceived(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if (isinstance(pkt, SendMenu)):
                print("Customer: Received a Menu! Reconstructing the menu...")
                self.reconstructMenu(pkt)
                print("The menu's content is: {!r}".format(self.receivedMenu))
                
    
    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.transport = None
        self.receivedMenu = None

    def reconstructMenu(self, menuPacket):
        self.receivedMenu = {}
        for category in menuPacket.menuContent.__dict__['_fields'].keys():
            self.receivedMenu[category] = list(element for element in getattr(menuPacket.menuContent, category))
        

    def requestMenu(self):
        request = RequestMenu();
        request.tableNumber = self.tableNumber
        request.name = self.customerName 
        print("Sending menu request... Name: {!r}, tableNumber: {!r}".format(request.name, \
                                                                             request.tableNumber))
        self.transport.write(request.__serialize__())