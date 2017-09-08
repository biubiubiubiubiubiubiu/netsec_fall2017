class CustomerClientProtocol:

    def __init__(self, loop, customerName, tableNumber):
        self.transport = None
        self.loop = loop
        self.customerName = customerName
        self.tableNumber = tableNumber
    
    def connection_made(self, transport):
        