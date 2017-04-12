# for command line args
import sys
# json.loads() will turn json string to python object
# json.dumps() will turn python object to json string
import json

# here are many imports from flask you may want to use
from flask import Flask, redirect, request, make_response, send_from_directory, render_template


app = Flask(__name__)
port = 0
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
    return ('location', 'payment')

@app.route('/order')
def order():
    order = generate_order()
    log = dict()
    log['order'] = order #id
    orders[order] = list()
    log['returnURL'] = url +":"+ str(port)
    log['drivers'] = list()
    for driver in drivers.keys():
        # scatter order to driver
        log['drivers'].append(driver)
    #set timer to call process_bids(orderid)
    return response(log)

def process_bids(orderid):
    bestbid = 0;
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

@app.route("/orderdelivered")
def order_delivered():
    return response("Unimplemented")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Pass in a port number')
    else:
        port = int(sys.argv[1])
        app.run(host='0.0.0.0', port=port)
