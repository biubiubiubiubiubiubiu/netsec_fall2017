from customerEnd import *
from serverEnd import *
from playground.network.packet import PacketType
import asyncio
class RestaurantServerProtocol:
    
    def __init__(self, stockList, menu):
        # the stock list is a dictionary for numbers of all the dishes in stock
        self.transport = None
        self.stockList = stockList
        self.menu = self.formatMenu(menu)
        self.counter = 1;
    
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        print('Restaurant: Got Connection from a customer!')
    
    def dataReceived(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if (isinstance(pkt, RequestMenu)):
                # Now the restaurant has received a menu request, it should respond the menu it has
                print('Restaurant: Get menu request from customer: {!r}, table number: {!r}'.format(pkt.name, \
                                                                                              pkt.tableNumber))
                # Generate id
                self.menu.ID = self.counter
                self.counter += 1
                self.menu.tableNumber = pkt.tableNumber
                self.menu.name = pkt.name
                print("Restaurant: Sending back the menu to customer: {!r}, table number: {!r}".format(self.menu.name,\
                                                                                                         self.menu.tableNumber))
                # Things will go wrong if you uncomment the following code
                # serialized = sendMenu.__serialize__()
                # print(type(PacketType.Deserialize(serialized)))
                self.transport.write(self.menu.__serialize__())
    


    def formatMenu(self, menu):
        sendMenu = SendMenu()
        sendMenu.menuContent = SendMenu.MenuContent()
        sendMenu.menuContent.Appetizers = list(menu["Appetizers"])
        sendMenu.menuContent.Sandwiches = list(menu["Sandwiches"])
        sendMenu.menuContent.Salads_and_Soups = list(menu["Salads_and_Soups"])
        sendMenu.menuContent.Desert = list(menu["Desert"])
        return sendMenu
            