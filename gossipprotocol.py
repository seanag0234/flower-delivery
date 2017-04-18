import threading
import requests
import random
import time
import json


class GossipInfo:

    def __init__(self, url):
        self.url = url
        self.last_flower_shop = 0
        self.last_driver = 0


class Gossip(threading.Thread):

    def __init__(self, url, gossip_endpoint):
        super(Gossip, self).__init__()
        # member variables
        self.url = url
        self.gossip_endpoint = gossip_endpoint
        self.my_flower_shops = []
        if url != "http://localhost:4000":
            self.my_flower_shops.append(GossipInfo("http://localhost:4000"))
        self.my_drivers = []
        # thread setup
        self.daemon = True
        # self.flower_shops_lock = threading.Lock()
        print('start')
        self.start()  # begin request thread

    def run(self):
        while True:
            time.sleep(.1)
            flower_shop = self.get_request_data()
            if not flower_shop:
                continue
            try:
                data = {'url': self.url, 'shop': flower_shop.last_flower_shop, 'driver': flower_shop.last_driver}
                r = requests.get(flower_shop.url + self.gossip_endpoint, data=json.dumps(data))
                response = r.json()
                self.add_response(flower_shop, response)
            except Exception as e:
                print(e)

    def get_request_data(self):
        flower_shop = None
        # self.flower_shops_lock.acquire()
        if len(self.my_flower_shops) != 0:
            flower_shop = random.choice(self.my_flower_shops)
        # self.flower_shops_lock.release()
        return flower_shop

    def add_response(self, flower_shop, response):
        print('add', response)
        if 'shop' in response:
            # self.flower_shops_lock.acquire()
            flower_shop.last_flower_shop += 1
            new_shop = response['shop']
            self.add_flower_shop(new_shop)
            # self.flower_shops_lock.release()
        if 'driver' in response:
            flower_shop.last_driver += 1
            new_driver = response['driver']
            self.add_driver(new_driver)

    def add_flower_shop(self, url):
        # self.flower_shops_lock.acquire()
        if url != self.url and not any(shop.url == url for shop in self.my_flower_shops):
            print("I, {}, got {}".format(self.url, url))
            self.my_flower_shops.append(GossipInfo(url))
        # self.flower_shops_lock.release()

    def add_driver(self, url):
        if url not in self.my_drivers:
            print ("adding driver " + url)
            self.my_drivers.append(url)

    def respond(self, request):
        try:
            data = json.loads(request.data.decode('utf-8'))
        except Exception as e:
            print(e)
            return '{}'
        else:
            response = {}
            if 'url' in data:
                self.add_flower_shop(data['url'])
            if 'shop' in data:
                shop_index = data['shop']
                if shop_index < len(self.my_flower_shops):
                    response['shop'] = self.my_flower_shops[shop_index].url
            if 'driver' in data:
                driver_index = data['driver']
                if driver_index < len(self.my_drivers):
                    response['driver'] = self.my_drivers[driver_index]
            return json.dumps(response)
