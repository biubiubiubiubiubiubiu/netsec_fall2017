# The classes used by customer end

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT16, STRING, \
                                                 ComplexFieldType, PacketFields, ListFieldType, INT32

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