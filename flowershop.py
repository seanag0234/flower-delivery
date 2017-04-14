# for command line args
import sys
# json.loads() will turn json string to python object
# json.dumps() will turn python object to json string
import json

# here are many imports from flask you may want to use
from flask import Flask, redirect, request, make_response, send_from_directory, render_template
import gossipprotocol
import requests
import random
from threading import Thread

app = Flask(__name__)
port = 0
flower_url = ''
gossip = None
gossip_endpoint = '/gossip'
orders = dict()
order_id = 0
orders_delivered = dict()


def generate_location():
    latitude = random.uniform(35,40)
    longitude = random.uniform(-110,-80)
    location = str(latitude) + "," + str(longitude)
    return location


def response(obj):
    response = make_response()
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(obj)
    return response


@app.route('/register')
def register():
    global gossip
    uri = request.args.get("uri")
    gossip.add_driver(uri)
    log = "uri needed"
    if uri:
        log = {'result': 'success', 'drivers': gossip.my_drivers}
    return response(log)


def generate_order():
    global order_id
    order_id += 1
    return flower_url + "-" + str(order_id), generate_location(), len(gossip.my_drivers), dict()


def send_get(url, params):
    requests.get(url, params=params)


@app.route("/flowershops")
def get_flower_shops():
    flower_shops = list()
    for gossip_info in gossip.my_flower_shops:
        flower_shops.append(gossip_info.url)

    return response(flower_shops)


@app.route('/ordersdelivered')
def get_orders_delivered():
    return response(orders_delivered)


@app.route('/order')
def order():
    global orders
    order = generate_order()
    log = dict()
    log['order'] = order #id
    orders[order[0]] = order
    log['returnURL'] = flower_url +":"+ str(port)
    log['drivers'] = list()
    drivers = gossip.my_drivers
    for driver in drivers:
        # scatter order to driver
        driver_url = driver + "/order"
        get_params = dict()
        get_params['uri'] = flower_url
        get_params['location'] = order[1]
        get_params['id'] = order[0]
        thread = Thread(target=send_get, args=(driver_url, get_params))
        thread.start()
        log['drivers'].append(driver)
    # set timer to call process_bids(orderid)

    return response(log)


def process_bids(orderid):
    bestbid = sys.maxint
    winning_driver = ''
    bids = orders[orderid][3]

    for driver, bid in bids.items():
        if int(bid) < int(bestbid):
            bestbid = bid
            winning_driver = driver

    driver_url = winning_driver + "/deliverorder"
    get_params = dict()
    get_params['id'] = orderid
    thread = Thread(target=send_get, args=(driver_url, get_params))
    thread.start()


@app.route("/drivers")
def get_drivers():
    return response(gossip.my_drivers)


@app.route('/bid')
def bid():
    global orders
    uri = request.args.get("uri")
    bid = request.args.get("bid")
    orderid = str(request.args.get("orderid"))
    order = orders[orderid]
    drivers_expected = order[2]
    order[3][uri] = bid
    orders[orderid] = order

    if drivers_expected == len(order[3]):
        process_bids(orderid)
    return response('bid recorded for ' + uri + " and bid " + str(bid))


@app.route("/orderdelivered")
def order_delivered():
    global orders_delivered
    orderid = request.args.get("id")
    uri = request.args.get("uri")
    if uri not in orders_delivered.keys():
        orders_delivered[uri] = list()
    orders_delivered[uri].append(orderid)
    return response("Order: " + orderid + " delivered by " + uri)


@app.route(gossip_endpoint)
def gossip():
    return gossip.respond(request)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Pass in a port number')
    else:
        port = int(sys.argv[1])
        flower_url = "http://localhost:" + str(port)
        gossip = gossipprotocol.Gossip(flower_url, gossip_endpoint)
        app.run(host='0.0.0.0', port=port)
