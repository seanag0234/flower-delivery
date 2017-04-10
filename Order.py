class Order:

    flower_shop_url = ''
    location = ''
    correlation_id = ''
    bid = -1

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
        return order
