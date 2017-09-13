from ClientDemo import CustomerClientProtocol
from ServerDemo import RestaurantServerProtocol

from playground.network.packet import PacketType
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import playground
import asyncio, sys

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
    client = CustomerClientProtocol(clientName, tableNumber)
    server = RestaurantServerProtocol(stockList, menu)
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
    
    echoArgs = {}
    
    args= sys.argv[1:]
    i = 0
    for arg in args:
        if arg.startswith("-"):
            k,v = arg.split("=")
            echoArgs[k]=v
        else:
            echoArgs[i] = arg
            i+=1
    
    if not 0 in echoArgs:
        sys.exit(USAGE)

    mode = echoArgs[0]
    print("WARNING: Since most of the data only exist in transmission, this unit test will use printing method to show if the code works")
    print("")
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
    loop = asyncio.get_event_loop()
    if mode.lower() == "server":
        coro = playground.getConnector().create_playground_server(lambda: RestaurantServerProtocol(stockList, menu), 101)
        server = loop.run_until_complete(coro)
        print("Restaurant Server Started at {}".format(server.sockets[0].gethostname()))
        loop.run_forever()
        loop.close()

    else:
        remoteAddress = "20174.1.1.1"
        coro = playground.getConnector().create_playground_connection(lambda: CustomerClientProtocol(clientName, tableNumber), remoteAddress, 101)
        transport, protocol = loop.run_until_complete(coro)
        print("Customer Connected. Starting UI t:{}. p:{}".format(transport, protocol))
        loop.add_reader(sys.stdin, protocol.requestMenu)
        loop.run_forever()
        loop.close()