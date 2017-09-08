from ClientDemo import CustomerClientProtocol
from ServerDemo import RestaurantServerProtocol
from playground.network.packet import PacketType
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol

import asyncio

def basicUnitTest():
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
            "Grilled Chicken": 57 
        },
        "Salads_and_Soups" : { 
            "Santa Fe Crisper Salad": 54,
            "Margherita Flatbread Salad": 42,
            "Margherita Flatbread Salad with Chicken": 32,
            "House Salad": 35 
        },
        "Deserts" : {
            "Triple Berry Crumble Cake" : 39
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
    print("Submission: Testing sending menu")
    client.requestMenu()
    print("======================================================================")
    print("Checking the serialization on ComplexFieldType:")
    temp = server.formatMenu(menu)
    temp.ID = 1
    temp.name = "adf"
    temp.tableNumber = 20
    serialized = temp.__serialize__()
    retrieved = PacketType.Deserialize(serialized)
    print("retrieveID: {!r}".format(retrieved.ID))
    print("retrieveName: {!r}".format(retrieved.name))
    print("retrieveNum: {!r}".format(retrieved.tableNumber))

if __name__ == "__main__":
    basicUnitTest()
