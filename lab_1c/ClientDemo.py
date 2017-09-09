from customerEnd import *
from serverEnd import *
from playground.network.packet import PacketType
class CustomerClientProtocol:

    def __init__(self, customerName, tableNumber):
        self.transport = None
        self.customerName = customerName
        self.tableNumber = tableNumber
        self.receivedMenu = None
        self.currentID = None
    
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        print("Customer: Connection made to a restaurant!")
    
    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, SendMenu):
                if pkt.name != self.customerName or pkt.tableNumber != self.tableNumber:
                    print("Customer: wrong order sent! Sending error message")

                print("Customer: Received a Menu! Reconstructing the menu...")
                self.reconstructMenu(pkt)
                print("Customer: The menu's content received is: {!r}".format(self.receivedMenu))
                self.currentID = pkt.ID
            
            elif isinstance(pkt, Cooking):
                print("Customer: recerived a Cooking message! Send back Thanks!")
                thanksMes = Thanks()
                thanksMes.ID = self.currentID
                thanksMes.name = self.customerName
                thanksMes.tableNumber = self.tableNumber
                self.transport.write(thanksMes.__serialize__())
            
            elif isinstance(pkt, MissingDish):
                print("Customer: received order failure! Message is: {!r}".format(pkt.message))
                if pkt.message == 'Not Found':
                    print("Missing dish: {!r}".format(list(pkt.missing)))
                elif pkt.message == 'Unavailable':
                    print("Unavailable dish: {!r}".format(list(pkt.unavailable)))
                elif pkt.message == 'Not found and unavailable':
                    print("Missing dish: {!r}".format(list(pkt.missing)))
                    print("Unavailable dish: {!r}".format(list(pkt.unavailable)))
                print("Please reorder the dish!")

            elif isinstance(pkt, Nothing):
                print("Customer: received Nothing message, do nothing!")    
    
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
    
    def sendOrder(self, ordered):
        print("Customer: Sending order...")
        order = Order()
        order.ordered_content = []
        order.quantity = []
        order.ID = self.currentID
        order.name = self.customerName
        order.tableNumber = self.tableNumber
        for dish in ordered.keys():
            order.ordered_content.append(dish)
            order.quantity.append(ordered[dish])
        
        self.transport.write(order.__serialize__())
        