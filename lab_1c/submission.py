from ClientDemo import CustomerClientProtocol
from ServerDemo import RestaurantServerProtocol
from playground.network.packet import PacketType
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol

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
    print("======================================================================")
    print("Submission: Testing sending order from Client...")

    print("1) Testing normal orders...(should success)")
    ordered = {
        "Bacon Avocado Chicken": 1, 
        "Buffalo Chicken Ranch": 2,
        "Buffalo Fried Cauliflower": 1
    }
    client.sendOrder(ordered)
    print(" ")
    print("2) Testing ordering dishes that does not exist in menu...(should fail)")
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
    ordered = {
        "Bacon Avocado Chicken": 1, 
        "Buffalo Chicken Ranch": 2,
        "Triple Berry Crumble Cake": 3,
        "Grilled Chicken": 4
    }
    client.sendOrder(ordered)
    print(" ")
    print("4) Testing ordering dishes that are both not exist and out of stock...(should fail)")
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
    client.sendOrder({})
    print("======================================================================")

if __name__ == "__main__":
    basicUnitTest()
