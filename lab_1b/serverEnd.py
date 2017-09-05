from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT16, STRING, \
                                                 ComplexFieldType, PacketFields, ListFieldType

# Server end: "Menu" message
class SendMenu(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.Ruofan.SendMenu"
    DEFINITION_VERSION = "1.0"

    class MenuContent(PacketFields):
        FIELDS = [
            ("sandwich", ListFieldType(STRING)),
            ("salads and soups", ListFieldType(STRING)),
            ("Appetizers", ListFieldType(STRING)),
            ("desert", ListFieldType(STRING))
        ]

    FIELDS = [
        ("ID", UINT16),
        ("name", STRING),
        ("tableNumber", UINT16),
        ("MenuContent", ComplexFieldType(MenuContent))
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
        ("tableNumber", UINT16),
        ("ordered content", ListFieldType(STRING))
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