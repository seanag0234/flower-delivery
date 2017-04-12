# for command line args
import sys

# json.loads() will turn json string to python object
# json.dumps() will turn python object to json string
import json
import gossipprotocol
# here are many imports from flask you may want to use
from flask import Flask, redirect, request, make_response, send_from_directory, render_template
# from apscheduler.scheduler import Scheduler


app = Flask(__name__)
port = 0
gossip = None
url = ''
drivers = dict()
orders = dict()


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
    return 'location', 'payment'


@app.route('/order')
def order():
    order = generate_order()
    log = dict()
    log['order'] = order  # id
    orders[order] = list()
    log['returnURL'] = url + ":" + str(port)
    log['drivers'] = list()
    for driver in drivers.keys():
        # scatter order to driver
        log['drivers'].append(driver)
    # set timer to call process_bids(orderid)
    return response(log)


def process_bids(orderid):
    bestbid = 0
    bids = orders[orderid]
    for i in range(len(bids)):
        if bids[i][1] > bids[bestbid][1]:
            bestbid = i
    # send order_assignment to driver bids[bestbid] 


@app.route('/bid')
def bid():
    drivername = request.args.get("drivername")
    bid = request.args.get("bid")
    orderid = request.args.get("orderid")
    orders[orderid].append((drivername, bid))
    return response('bid recorded')


@app.route('/gossip')
def gossip():
    print('I got hit on gossip', request.host)
    return gossip.respond(request)


@app.route('/debug')
def debug():
    return ' '.join([shop.url for shop in gossip.my_flower_shops])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Pass a port number to run on')
    else:
        gossip = gossipprotocol.Gossip('http://localhost:'+sys.argv[1], '/gossip')
        for url in sys.argv[2:]:
            gossip.add_flower_shop(url)
        port = int(sys.argv[1])
        app.run(host='0.0.0.0', port=port)
