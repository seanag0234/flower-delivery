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

app = Flask(__name__)
port = 0
flower_url = ''
gossip = None
gossip_endpoint = '/gossip'
drivers = dict()
orders = dict()
order_id = 0


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
    drivername = request.args.get("drivername")
    uri = request.args.get("uri")
    drivers[drivername] = uri
    log = "drivername and uri needed"
    if drivername and uri:
        log = {'result': 'success', 'drivers': drivers}
    return response(log)


def generate_order():
    global order_id
    order_id += 1
    return order_id, generate_location(), len(drivers), dict()


@app.route('/order')
def order():
    order = generate_order()
    log = dict()
    log['order'] = order  # id
    orders[order[0]] = list()
    log['returnURL'] = flower_url + ":" + str(port)
    log['drivers'] = list()

    for driver in drivers.values():
        # scatter order to driver
        driver_url = driver + "/order"
        get_params = dict()
        get_params['uri'] = flower_url
        get_params['location'] = order[1]
        get_params['id'] = order[0]
        requests.get(driver_url, params=get_params)
        log['drivers'].append(driver)
    # set timer to call process_bids(orderid)

    return response(log)


def process_bids(orderid):
    bestbid = 0
    winning_driver = ''
    bids = orders[orderid][3]

    for driver, bid in bids.items():
        if bid > bestbid:
            bestbid = bid
            winning_driver = driver

    driver_url = drivers[winning_driver] + "/deliverorder"
    get_params = dict()
    get_params['id'] = orderid
    requests.get(driver_url, get_params)


@app.route('/bid')
def bid():
    drivername = request.args.get("drivername")
    bid = request.args.get("bid")
    orderid = request.args.get("orderid")
    order = orders[orderid]
    drivers_expected = order[2]
    order[3][drivername] = bid
    orders[orderid] = order

    if drivers_expected == len(order[3]):
        process_bids(orderid)
    return response('bid recorded for ' + drivername + " and bid " + str(bid))


@app.route("/orderdelivered")
def order_delivered():
    orderid = request.args.get("id")
    drivername = request.args.get("drivername")
    return response("Order: " + orderid + " delivered by " + drivername)


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
