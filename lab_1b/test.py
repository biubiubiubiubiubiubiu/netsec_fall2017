from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import NamedPacketType, ComplexFieldType, PacketFields, Uint, \
                                                    STRING, ListFieldType
from playground.network.packet.fieldtypes.attributes import MaxValue, Bits                      

# Customer end: "Request Menu" message

def basicUnitTest():
    p = PacketType()
    class TestPacket1(PacketType):
        DEFINITION_IDENTIFIER = "packettype.basicunittest.TestPacket1"
        DEFINITION_VERSION    = "1.0"
        
        class SubFields(PacketFields):
            FIELDS = [("subfield1",Uint({Bits:16})), ("subfield2",Uint({Bits:16}))]
        
        FIELDS = [  ("header", ComplexFieldType(SubFields)), 
                    ("field1", Uint({MaxValue:1000})), 
                    ("field2", STRING),
                    ("trailer",ComplexFieldType(SubFields)),
                    ("ls", ListFieldType(STRING))
                ]
    
    packet = TestPacket1()
    packet.header = TestPacket1.SubFields()
    packet.trailer = TestPacket1.SubFields()
    
    packet.header.subfield1 = 1
    packet.header.subfield2 = 100
    packet.field1 = 50
    packet.field2 = "test packet field 2"
    packet.trailer.subfield1 = 5
    packet.trailer.subfield2 = 500
    print(packet.ls)
    
    packet.ls = list()
    packet.ls.append("asdfas")

    serializedData = packet.__serialize__()
    # restoredPacket = PacketType.Deserialize(serializedData)
    
    # assert packet.header.subfield1 == restoredPacket.header.subfield1 
    # assert packet.field2 == restoredPacket.field2
    # print("Success!")
if __name__=="__main__":
    basicUnitTest()