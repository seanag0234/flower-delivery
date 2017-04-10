class Order:

    flower_shop_url = ''
    location = ''
    correlation_id = ''

    def __init__(self, flower_shop_url, location, correlation_id):
        self.flower_shop_url = flower_shop_url
        self.location = location
        self.id = correlation_id


