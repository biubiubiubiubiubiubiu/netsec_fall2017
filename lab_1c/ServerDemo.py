class RestaurantServerProtocol:
    
    def __init__(self, stockList, menu):
        # the stock list is a dictionary for numbers of all the dishes in stock
        self.transport = None
        self.stockList = stockList
        self.menu = menu
    
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        peername = transport.get_extra_info('peername')
        print('get Connection from a customer! {}'.format(peername))
    
    def data_received(self, data):
        print("data received!")