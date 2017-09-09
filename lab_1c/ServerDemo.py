from customerEnd import *
from serverEnd import *
from playground.network.packet import PacketType
import asyncio
class RestaurantServerProtocol:
    
    def __init__(self, stockList, menu):
        # the stock list is a dictionary for numbers of all the dishes in stock
        self.transport = None
        self.stockList = stockList
        self.originalMenu = menu
        self.menu = self.formatMenu(menu)
        self.counter = 1;
    
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        print('Restaurant: Got Connection from a customer!')
    
    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, RequestMenu):
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
            elif isinstance(pkt, Order):
                print("Restaurant: received customer's order from name: {!r}, tableNumber: {!r}".format(pkt.name, pkt.tableNumber))
                # Validate the order
                validateRes = self.validateOrder(pkt)
                print(validateRes["message"])
                missingDish = MissingDish()
                missingDish.ID = pkt.ID
                missingDish.name = pkt.name

                missingDish.tableNumber = pkt.tableNumber
                missingDish.missing = []
                missingDish.unavailable = []
                if validateRes["validate"]:
                    print("Restaurant: Successfully ordered the dish, content is: {!r}, number is: {!r}".format(list(pkt.ordered_content), list(pkt.quantity)))
                    print("Restaurant: Sending Cooking message...")
                    cookingMes = Cooking()
                    cookingMes.ID = pkt.ID
                    cookingMes.name = pkt.name
                    cookingMes.tableNumber = pkt.tableNumber
                    self.transport.write(cookingMes.__serialize__())
                
                elif validateRes["message"] == "Nothing orderred":
                    print("Restaurant: Nothing orderred from customer. Sending Nothing message")
                    nothing = Nothing()
                    nothing.ID, nothing.name, nothing.tableNumber = pkt.ID, pkt.name, pkt.tableNumber
                    self.transport.write(nothing.__serialize__())

                elif validateRes["message"] == "Not Found":
                    print("Restaurant: Order failure! Reason: {!r}, not found dish: {!r}".format(validateRes['message'], validateRes['notFoundDish']))
                    print("Restaurant Sending Warning Message...")
                    
                    missingDish.message = validateRes['message']
                    missingDish.missing = validateRes['notFoundDish']

                    self.transport.write(missingDish.__serialize__())

                elif validateRes["message"] == "Unavailable":
                    print("Restaurant: Order failure! Reason: {!r}, unavailable dish: {!r}".format(validateRes['message'], validateRes['unAvailableDish']))    
                    print("Restaurant Sending Warning Message...")

                    missingDish.message = validateRes['message']
                    missingDish.unavailable = validateRes['unAvailableDish']
                    
                    self.transport.write(missingDish.__serialize__())

                elif validateRes["message"] == "Not found and unavailable":
                    print("Restaurant: Order failure! Reason: {!r}, unavailable dish: {!r}, not found dish: {!r}"\
                        .format(validateRes['message'], \
                                validateRes['unAvailableDish'],\
                                validateRes['notFoundDish'])) 
                    print("Restaurant Sending Warning Message...")

                    missingDish.message = validateRes['message']
                    missingDish.missing = validateRes['notFoundDish']
                    missingDish.unavailable = validateRes['unAvailableDish']
                
                    self.transport.write(missingDish.__serialize__())

            elif isinstance(pkt, Thanks):
                print("Restaurant: Thanks message received from customer: {!r}, table number: {!r}".\
                        format(pkt.name, pkt.tableNumber))   


    def formatMenu(self, menu):
        sendMenu = SendMenu()
        sendMenu.menuContent = SendMenu.MenuContent()
        sendMenu.menuContent.Appetizers = list(menu["Appetizers"])
        sendMenu.menuContent.Sandwiches = list(menu["Sandwiches"])
        sendMenu.menuContent.Salads_and_Soups = list(menu["Salads_and_Soups"])
        sendMenu.menuContent.Desert = list(menu["Desert"])
        return sendMenu

    def validateOrder(self, order):
        dishes = order.ordered_content
        quantity = order.quantity
        
        unAvailableDish = []
        notFoundDish = []
        for i in range(0, len(dishes)):
            found = False
            for category in self.originalMenu.keys():
                if dishes[i] in self.originalMenu[category]:
                    found = True
                    if self.stockList[category][dishes[i]] > quantity[i]:
                        break
                    else:
                        unAvailableDish.append(dishes[i])
            if not found:
                notFoundDish.append(dishes[i])
        # Check the result
        ret = dict()
        if len(dishes) == 0:
            ret["validate"] = False
            ret["message"] = "Nothing orderred"
        elif len(unAvailableDish) > 0 and len(notFoundDish) > 0:
            ret["validate"] = False
            ret["message"] = "Not found and unavailable"
            ret["notFoundDish"] = notFoundDish
            ret["unAvailableDish"] = unAvailableDish
        elif len(unAvailableDish) > 0:
            ret["validate"] = False
            ret["message"] = "Unavailable"
            ret["unAvailableDish"] = unAvailableDish
        elif len(notFoundDish) > 0:
            ret["validate"] = False
            ret["message"] = "Not Found"
            ret["notFoundDish"] = notFoundDish
        else:
            ret["validate"] = True
            ret["message"] = "Success"      
        return ret
            