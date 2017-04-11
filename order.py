class Order:

    flower_shop_url = ''
    location = ''
    correlation_id = ''
    bid = -1
    delivered = False

    def __init__(self, flower_shop_url, location, correlation_id):
        self.flower_shop_url = flower_shop_url
        self.location = location
        self.correlation_id = correlation_id

    def get_dict(self):
        order = dict()
        order["flower_shop_url"] = self.flower_shop_url
        order["location"] = self.location
        order["correlation_id"] = self.correlation_id
        order["bid"] = self.bid
        order['delivered'] = self.delivered
        return order

    def order_from_dict(self, order_dict):
       self.flower_shop_url = order_dict["flower_shop_url"]
       self.location = order_dict["location"]
       self.correlation_id = order_dict["correlation_id"]
       self.bid = order_dict["bid"]
       self.delivered = order_dict["delivered"]
