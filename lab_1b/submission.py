# Network Security Assignment 1[b]
# Author: Ruofan Shen

from customerEnd import *
from serverEnd import *

def basicUnitTest():
    
    # RequestMenu class
    print("---------------- Testing RequestMenu class from customerEnd -------------------")
    requestMenu = RequestMenu()
    requestMenu.tableNumber = 12
    requestMenu.name = "David"
    serializedData = requestMenu.__serialize__()
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert requestMenu.tableNumber == restoredPacket.tableNumber
    assert requestMenu.name == restoredPacket.name

    print("RequestMenu passed the test!")

    # SendMenu class
    print("---------------- Testing SendMenu class from serverEnd -------------------")
    sendMenu = SendMenu()
    sendMenu.ID = 124
    sendMenu.tableNumber = 14
    sendMenu.name = "David"
    sendMenu.menuContent = SendMenu.MenuContent()
    sendMenu.menuContent.Appetizers = ["Buffalo Fried Cauliflower"]
    sendMenu.menuContent.Sandwiches = ["Bacon Avocado Chicken", "Buffalo Chicken Ranch", "Grilled Chicken"]
    sendMenu.menuContent.Salads_and_Soups = ["Santa Fe Crisper Salad", "Margherita Flatbread Salad"]
    sendMenu.menuContent.Desert = list()
    serializedData = sendMenu.__serialize__();
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert sendMenu.ID == restoredPacket.ID
    assert sendMenu.tableNumber == restoredPacket.tableNumber
    assert sendMenu.name == restoredPacket.name
    assert len(sendMenu.menuContent.Appetizers) == len(restoredPacket.menuContent.Appetizers)
    assert len(sendMenu.menuContent.Sandwiches) == len(restoredPacket.menuContent.Sandwiches)
    assert len(sendMenu.menuContent.Salads_and_Soups) == len(restoredPacket.menuContent.Salads_and_Soups)
    for i in range (0, len(sendMenu.menuContent.Appetizers)):
        assert sendMenu.menuContent.Appetizers[i] == restoredPacket.menuContent.Appetizers[i]

    for i in range (0, len(sendMenu.menuContent.Sandwiches)):
        assert sendMenu.menuContent.Sandwiches[i] == restoredPacket.menuContent.Sandwiches[i]

    for i in range (0, len(sendMenu.menuContent.Salads_and_Soups)):
        assert sendMenu.menuContent.Salads_and_Soups[i] == restoredPacket.menuContent.Salads_and_Soups[i]

    print("SendMenu passed the test!")

    # Order Class
    print("---------------- Testing Order class from customerEnd -------------------")
    order = Order()
    order.ID = 20
    order.tableNumber = 12
    order.name = "George"
    order.ordered_content = list()
    order.quantity = list()
    # for simplicity, we make a promise here that every field with number -1 is the classification label
    ordered = {
        "Sandwiches": -1,
        "Bacon Avocado Chicken": 1, 
        "Buffalo Chicken Ranch": 2,
        "Appetizers": -1,
        "Buffalo Fried Cauliflower": 1
    }
    for key in ordered.keys():
        order.ordered_content.append(key)
        order.quantity.append(ordered[key])
    serializedData = order.__serialize__();
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert order.ID == restoredPacket.ID
    assert order.tableNumber == restoredPacket.tableNumber
    assert order.name == restoredPacket.name
    assert len(restoredPacket.ordered_content) == len(order.ordered_content)
    assert len(restoredPacket.quantity) == len(order.quantity)

    for i in range(0, len(restoredPacket.ordered_content)):
        assert order.ordered_content[i] == restoredPacket.ordered_content[i]
        assert order.quantity[i] == restoredPacket.quantity[i]
    
    print("Order passed the test!")

    # CustomerErrorMessage class
    print("---------------- Testing CustomerErrorMessage class from customerEnd -------------------")
    customerErrorMessage = CustomerErrorMessage()
    customerErrorMessage.ID = 10
    customerErrorMessage.Error_Message = "Wrong table number or name!"
    serializedData = customerErrorMessage.__serialize__();
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert customerErrorMessage.ID == restoredPacket.ID
    assert customerErrorMessage.Error_Message == restoredPacket.Error_Message

    print("CustomerErrorMessage passed the test!")

    # Cooking class
    print("---------------- Testing Cooking class from serverEnd -------------------")
    cooking = Cooking()
    cooking.ID = 10
    cooking.tableNumber = 14
    cooking.name = "Tom"
    serializedData = cooking.__serialize__();
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert cooking.ID == restoredPacket.ID
    assert cooking.tableNumber == restoredPacket.tableNumber
    assert cooking.name == restoredPacket.name

    print("Cooking passed the test!")

    # MissingDish class
    print("---------------- Testing MissingDish class from serverEnd -------------------")
    missingDish = MissingDish()
    missingDish.ID = 12
    missingDish.tableNumber = 25
    missingDish.name = "Louis"
    missingDish.missing = ["Buffalo Chicken Ranch", "Buffalo Fried Cauliflower"]
    serializedData = missingDish.__serialize__();
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert missingDish.ID == restoredPacket.ID
    assert missingDish.tableNumber == restoredPacket.tableNumber
    assert missingDish.name == restoredPacket.name
    assert len(restoredPacket.missing) == len(missingDish.missing)
    for i in range(0, len(restoredPacket.missing)):
        assert restoredPacket.missing[i] == missingDish.missing[i]

    print("MissingDish passed the test!")

    # Nothing class
    print("---------------- Testing Nothing class from serverEnd -------------------")
    nothing = Nothing()
    nothing.ID = 10
    nothing.tableNumber = 14
    nothing.name = "Tom"
    serializedData = nothing.__serialize__();
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert nothing.ID == restoredPacket.ID
    assert nothing.tableNumber == restoredPacket.tableNumber
    assert nothing.name == restoredPacket.name

    print("Nothing passed the test!")

    print("---------------- Testing Thanks class from serverEnd -------------------")
    thanks = Thanks()
    thanks.ID = 10
    thanks.tableNumber = 14
    thanks.name = "Tom"
    serializedData = thanks.__serialize__();
    restoredPacket = PacketType.Deserialize(serializedData)
    
    assert thanks.ID == restoredPacket.ID
    assert thanks.tableNumber == restoredPacket.tableNumber
    assert thanks.name == restoredPacket.name

    print("Thanks passed the test!")

    print("Success!")

if __name__=="__main__":
    basicUnitTest()
