# The classes used by customer end

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT16, STRING, \
    ComplexFieldType, PacketFields, ListFieldType, INT32
import asyncio, sys

# Customer end: "Request Menu" message
class RequestMenu(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.Ruofan.RequestMenu"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("tableNumber", UINT16),
        ("name", STRING)
    ]


# Customer end: Order message
class Order(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.Ruofan.Order"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("ID", UINT16),
        ("name", STRING),
        ("tableNumber", UINT16),
        ("ordered_content", ListFieldType(STRING)),
        ("quantity", ListFieldType(INT32))
    ]


# Customer end: Error message
class CustomerErrorMessage(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.Ruofan.CustomerErrorMessage"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("ID", STRING),
        ("Error_Message", STRING)
    ]


# Customer end:
class Thanks(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.Ruofan.Thanks"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("ID", UINT16),
        ("name", STRING),
        ("tableNumber", UINT16),
    ]
# The classes used by server end

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT16, STRING, \
                                                 ComplexFieldType, PacketFields, ListFieldType

# Server end: "Menu" message
class SendMenu(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.Ruofan.SendMenu"
    DEFINITION_VERSION = "1.0"

    class MenuContent(PacketFields):
        FIELDS = [
            ("Appetizers", ListFieldType(STRING)),
            ("Sandwiches", ListFieldType(STRING)),
            ("Salads_and_Soups", ListFieldType(STRING)),
            ("Desert", ListFieldType(STRING))
        ]

    FIELDS = [
        ("ID", UINT16),
        ("name", STRING),
        ("tableNumber", UINT16),
        ("menuContent", ComplexFieldType(MenuContent))
    ]


# Server end: Cooking message
class Cooking(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.Ruofan.Cooking"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("ID", UINT16),
        ("name", STRING),
        ("tableNumber", UINT16),
    ]

# Server end: MissingDish Message
class MissingDish(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.Ruofan.MissingDish"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("ID", UINT16),
        ("name", STRING),
        ("message", STRING),
        ("tableNumber", UINT16),
        ("missing", ListFieldType(STRING)),
        ("unavailable", ListFieldType(STRING))
    ]

# Server end: Nothing Message
class Nothing(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.Ruofan.Nothing"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("ID", UINT16),
        ("name", STRING),
        ("tableNumber", UINT16),
    ]



class CustomerClientProtocol(asyncio.Protocol):
    # Some statuses for customer end
    WAITING = 0
    WAITING_ORDER = 1
    SEND_ORDER = 2
    WAITING_COMFIRMATION = 3

    def __init__(self, customerName, tableNumber):
        self.transport = None
        self.customerName = customerName
        self.tableNumber = tableNumber
        self.receivedMenu = None
        self.currentID = None
        self.status = None

    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        self.status = self.WAITING
        print("Customer: Connection made to a restaurant!")

    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, SendMenu) and self.status == self.WAITING_ORDER:
                self.currentID = pkt.ID
                if pkt.name != self.customerName or pkt.tableNumber != self.tableNumber:
                    print("Customer: wrong order sent! Sending error message")
                    customerErrorMessage = CustomerErrorMessage()
                    customerErrorMessage.ID = self.currentID
                    customerErrorMessage.Error_Message = "Wrong Order"
                    self.transport.write(customerErrorMessage.__serialize__())

                print("Customer: Received a Menu! Reconstructing the menu...")
                self.reconstructMenu(pkt)
                print("Customer: The menu's content received is: {!r}".format(self.receivedMenu))
                self.status = self.SEND_ORDER

            elif isinstance(pkt, Cooking) and self.status == self.WAITING_COMFIRMATION:
                print("Customer: recerived a Cooking message! Send back Thanks!")
                thanksMes = Thanks()
                thanksMes.ID = self.currentID
                thanksMes.name = self.customerName
                thanksMes.tableNumber = self.tableNumber
                self.status = self.WAITING
                self.transport.write(thanksMes.__serialize__())

            elif isinstance(pkt, MissingDish) and self.status == self.WAITING_COMFIRMATION:
                print("Customer: received order failure! Message is: {!r}".format(pkt.message))
                if pkt.message == 'Not Found':
                    print("Missing dish: {!r}".format(list(pkt.missing)))
                elif pkt.message == 'Unavailable':
                    print("Unavailable dish: {!r}".format(list(pkt.unavailable)))
                elif pkt.message == 'Not found and unavailable':
                    print("Missing dish: {!r}".format(list(pkt.missing)))
                    print("Unavailable dish: {!r}".format(list(pkt.unavailable)))
                print("Please reorder the dish!")
                self.status = self.SEND_ORDER

            elif isinstance(pkt, Nothing) and self.status == self.WAITING_COMFIRMATION:
                print("Customer: received Nothing message, do nothing!")
                self.status = self.WAITING

            else:
                print("Customer: Wrong packet received, current status: {!r}, aborting...".format(self.status))

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
        if (self.transport is not None) and self.status == self.WAITING:
            request = RequestMenu();
            request.tableNumber = self.tableNumber
            request.name = self.customerName
            print("Sending menu request... Name: {!r}, tableNumber: {!r}".format(request.name, \
                                                                                 request.tableNumber))
            self.status = self.WAITING_ORDER
            self.transport.write(request.__serialize__())
        else:
            print("Wrong status for requestMenu, current status: {!r}".format(self.status))

    def sendOrder(self, ordered):
        if (self.transport is not None) and self.status == self.SEND_ORDER:
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
            self.status = self.WAITING_COMFIRMATION
            self.transport.write(order.__serialize__())
        else:
            print("Wrong status for requestMenu, current status: {!r}".format(self.status))



class RestaurantServerProtocol(asyncio.Protocol):
    # Some statuses for server end
    WAITING = 0
    WAITING_ORDER = 1
    COOKING = 2
    PROCESSING_ORDER = 3

    def __init__(self, stockList, menu):
        # the stock list is a dictionary for numbers of all the dishes in stock
        self.transport = None
        self.stockList = stockList
        self.originalMenu = menu
        self.menu = self.formatMenu(menu)
        self.counter = 1;
        self.status = None

    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        print('Restaurant: Got Connection from a customer!')
        self.status = self.WAITING

    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            if pkt is None:
                pass
            elif isinstance(pkt, RequestMenu) and self.status == self.WAITING:
                # Now the restaurant has received a menu request, it should respond the menu it has
                print('Restaurant: Get menu request from customer: {!r}, table number: {!r}'.format(pkt.name, \
                                                                                                    pkt.tableNumber))
                # Generate id
                self.menu.ID = self.counter
                self.counter += 1
                self.menu.tableNumber = pkt.tableNumber
                self.menu.name = pkt.name
                print("Restaurant: Sending back the menu to customer: {!r}, table number: {!r}".format(self.menu.name, \
                                                                                                       self.menu.tableNumber))
                # Things will go wrong if you uncomment the following code
                # serialized = sendMenu.__serialize__()
                # print(type(PacketType.Deserialize(serialized)))
                self.status = self.WAITING_ORDER
                self.transport.write(self.menu.__serialize__())

            elif isinstance(pkt, CustomerErrorMessage):
                print("Restaurant: received customer's complain! Please resend the menu")

            elif isinstance(pkt, Order) and self.status == self.WAITING_ORDER:
                print("Restaurant: received customer's order from name: {!r}, tableNumber: {!r}".format(pkt.name,
                                                                                                        pkt.tableNumber))
                # Validate the order
                self.status = self.PROCESSING_ORDER
                validateRes = self.validateOrder(pkt)
                missingDish = MissingDish()
                missingDish.ID = pkt.ID
                missingDish.name = pkt.name

                missingDish.tableNumber = pkt.tableNumber
                missingDish.missing = []
                missingDish.unavailable = []
                if validateRes["validate"]:
                    print("Restaurant: Successfully ordered the dish, content is: {!r}, number is: {!r}".format(
                        list(pkt.ordered_content), list(pkt.quantity)))
                    print("Restaurant: Sending Cooking message...")
                    cookingMes = Cooking()
                    cookingMes.ID = pkt.ID
                    cookingMes.name = pkt.name
                    cookingMes.tableNumber = pkt.tableNumber
                    self.status = self.COOKING
                    self.transport.write(cookingMes.__serialize__())

                elif validateRes["message"] == "Nothing orderred":
                    print("Restaurant: Nothing orderred from customer. Sending Nothing message")
                    nothing = Nothing()
                    nothing.ID, nothing.name, nothing.tableNumber = pkt.ID, pkt.name, pkt.tableNumber
                    self.status = self.WAITING
                    self.transport.write(nothing.__serialize__())

                elif validateRes["message"] == "Not Found":
                    print("Restaurant: Order failure! Reason: {!r}, not found dish: {!r}".format(validateRes['message'],
                                                                                                 validateRes[
                                                                                                     'notFoundDish']))
                    print("Restaurant Sending Warning Message...")

                    missingDish.message = validateRes['message']
                    missingDish.missing = validateRes['notFoundDish']
                    self.status = self.WAITING_ORDER
                    self.transport.write(missingDish.__serialize__())


                elif validateRes["message"] == "Unavailable":
                    print(
                        "Restaurant: Order failure! Reason: {!r}, unavailable dish: {!r}".format(validateRes['message'],
                                                                                                 validateRes[
                                                                                                     'unAvailableDish']))
                    print("Restaurant Sending Warning Message...")

                    missingDish.message = validateRes['message']
                    missingDish.unavailable = validateRes['unAvailableDish']
                    self.status = self.WAITING_ORDER
                    self.transport.write(missingDish.__serialize__())


                elif validateRes["message"] == "Not found and unavailable":
                    print("Restaurant: Order failure! Reason: {!r}, unavailable dish: {!r}, not found dish: {!r}" \
                          .format(validateRes['message'], \
                                  validateRes['unAvailableDish'], \
                                  validateRes['notFoundDish']))
                    print("Restaurant Sending Warning Message...")

                    missingDish.message = validateRes['message']
                    missingDish.missing = validateRes['notFoundDish']
                    missingDish.unavailable = validateRes['unAvailableDish']
                    self.status = self.WAITING_ORDER
                    self.transport.write(missingDish.__serialize__())


            elif isinstance(pkt, Thanks) and self.status == self.COOKING:
                print("Restaurant: Thanks message received from customer: {!r}, table number: {!r}". \
                      format(pkt.name, pkt.tableNumber))
                self.status = self.WAITING

            else:
                print("Restaurant: Wrong packet received, current status: {!r}, type: {!r}, aborting...".format(
                    self.status, type(pkt)))

    def formatMenu(self, menu):
        sendMenu = SendMenu()
        sendMenu.menuContent = SendMenu.MenuContent()
        sendMenu.menuContent.Appetizers = list(menu["Appetizers"])
        sendMenu.menuContent.Sandwiches = list(menu["Sandwiches"])
        sendMenu.menuContent.Salads_and_Soups = list(menu["Salads_and_Soups"])
        sendMenu.menuContent.Desert = list(menu["Desert"])
        return sendMenu

    def validateOrder(self, order):
        if self.status == self.PROCESSING_ORDER:
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
        else:
            print("Wrong method 'validateOrder' called at this status: {!r}".format(self.status))


from playground.network.packet import PacketType
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import playground
import asyncio

def basicUnitTest():
    print("WARNING: Since most of the data only exist in transmission, this unit test will use printing method to show if the code works")
    print("")
    asyncio.set_event_loop(TestLoopEx())
    clientName = "peter"
    tableNumber = 14
    stockList = {
        "Appetizers" : {
            "Buffalo Fried Cauliflower": 43,
            "Triple Dipper": 37
        },
        "Sandwiches" : {
            "Bacon Avocado Chicken": 96,
            "Buffalo Chicken Ranch": 23,
            "Grilled Chicken": 3
        },
        "Salads_and_Soups" : {
            "Santa Fe Crisper Salad": 54,
            "Margherita Flatbread Salad": 42,
            "Margherita Flatbread Salad with Chicken": 32,
            "House Salad": 35
        },
        "Desert" : {
            "Triple Berry Crumble Cake" : 1
        }
    }
    menu = {
        "Appetizers" : [
            "Buffalo Fried Cauliflower",
            "Triple Dipper"
        ],
        "Sandwiches" : [
            "Bacon Avocado Chicken",
            "Buffalo Chicken Ranch",
            "Grilled Chicken"
        ],
        "Salads_and_Soups": [
            "Santa Fe Crisper Salad",
            "Margherita Flatbread Salad",
            "Margherita Flatbread Salad with Chicken",
            "House Salad"
        ],
        "Desert": [
            "Triple Berry Crumble Cake"
        ]
    }
    client = playground.getConnector().create_playground_server(lambda: CustomerClientProtocol(clientName, tableNumber), 101)
    server = playground.getConnector().create_playground_connection(lambda: RestaurantServerProtocol(stockList, menu), "20174.1.1.1", 101)
    # client = CustomerClientProtocol(clientName, tableNumber)
    # server = RestaurantServerProtocol(stockList, menu)
    transportToServer = MockTransportToProtocol(server)
    transportToClient = MockTransportToProtocol(client)
    client.connection_made(transportToServer)
    server.connection_made(transportToClient)
    print("======================================================================")
    print("Submission: Testing sending menu...")
    client.requestMenu()
    assert menu.keys() == client.receivedMenu.keys()
    for key in menu.keys():
        assert menu[key] == client.receivedMenu[key]
        assert client.receivedMenu[key] == server.originalMenu[key]
    assert client.status == client.SEND_ORDER
    assert server.status == server.WAITING_ORDER
    print("======================================================================")
    print("Submission: Testing sending order from Client...")

    print("1) Testing normal orders...(should success)")
    ordered = {
        "Bacon Avocado Chicken": 1,
        "Buffalo Chicken Ranch": 2,
        "Buffalo Fried Cauliflower": 1
    }
    client.sendOrder(ordered)
    assert client.status == client.WAITING
    assert server.status == server.WAITING
    print(" ")
    print("2) Testing ordering dishes that does not exist in menu...(should fail)")
    client.requestMenu()
    ordered = {
        "Bacon Avocado Chicken": 1,
        "Buffalo Chicken Ranch": 2,
        "Buffalo Fried Cauliflower": 1,
        "Something not exist1": 10,
        "Something not exist3": 12
    }
    client.sendOrder(ordered)
    print(" ")
    print("3) Testing ordering dishes that are out of stock...(should fail)")
    client.requestMenu()
    ordered = {
        "Bacon Avocado Chicken": 1,
        "Buffalo Chicken Ranch": 2,
        "Triple Berry Crumble Cake": 3,
        "Grilled Chicken": 4
    }
    client.sendOrder(ordered)
    print(" ")
    print("4) Testing ordering dishes that are both not exist and out of stock...(should fail)")
    client.requestMenu()
    ordered = {
        "Bacon Avocado Chicken": 1,
        "Buffalo Chicken Ranch": 2,
        "Triple Berry Crumble Cake": 3,
        "Grilled Chicken": 4,
        "Something not exist1": 10,
        "Something not exist3": 12
    }
    client.sendOrder(ordered)
    print(" ")
    print("5) Testing ordering nothing")
    client.requestMenu()
    client.sendOrder({})
    print("======================================================================")

if __name__ == "__main__":
    basicUnitTest()
