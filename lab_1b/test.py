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
        
        FIELDS = [  
                    ("ls", ListFieldType(SubFields))
                ]
    
    packet = TestPacket1()
    packet.ls = []
    subFields = TestPacket1.SubFields();
    subFields.subfield1 = 21
    subFields.subfield2 = 45
    packet.ls.append(subFields)

    serializedData = packet.__serialize__()
    restoredPacket = PacketType.Deserialize(serializedData)
    
    print("Success!")
if __name__=="__main__":
    basicUnitTest()