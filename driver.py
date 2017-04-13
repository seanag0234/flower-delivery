from __future__ import print_function
# for command line args
import sys

# json.loads() will turn json string to python object
# json.dumps() will turn python object to json string
import json
import requests
import random
import weather_api
import directions_api
from order import Order
# here are many imports from flask you may want to use
from flask import Flask, redirect, request, make_response, send_from_directory, render_template

app = Flask(__name__)

# The correlation_id of the order will be the key and the Order object the value
orders_received = dict()
orders_delivered = dict()
port = 5000
driver_url = "http://localhost:" + str(port)


def generate_location():
    latitude = random.uniform(35,40)
    longitude = random.uniform(-110,-80)
    location = str(latitude) + "," + str(longitude)
    return location

driver_location = generate_location()
print("Driver Location: " + str(driver_location))


# Endpoint to receive an order from a flower shop
@app.route('/order')
def send_bid():
    global orders_received
    flower_shop_url = request.args.get("uri")
    order_location = request.args.get("location")
    id = request.args.get("id")
    order = Order(flower_shop_url, order_location, id)
    bid = calculate_bid(order, driver_location)
    order.bid = bid
    orders_received[id] = order
    get_params = dict()
    get_params["uri"] = driver_url
    get_params["bid"] = bid
    get_params["orderid"] = order.correlation_id
    response = requests.get(flower_shop_url + "/bid", params=get_params)
    return create_response(response)


@app.route('/deliverorder')
def deliver_order():
    global orders_delivered
    id = request.args.get("id")
    if not id in orders_received:
        response = make_response()
        response.data = "That order id doesn't exist for driver " + str(driver_url)
        return response
    order = orders_received[id]
    order.delivered = True
    orders_delivered[id] = order
    get_params = dict()
    get_params["id"] = id
    get_params['uri'] = driver_url
    driver_location = order.location
    response = requests.get(order.flower_shop_url + "/orderdelivered", params=get_params)
    return create_response(response)


def response(obj):
    response = make_response()
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(obj)
    return response


@app.route("/ordersreceived")
def get_orders_received():
    all_orders = list()
    for order in orders_received.values():
        dictionary = order.get_dict()
        all_orders.append(dictionary)

    return response(all_orders)


@app.route("/ordersdelivered")
def get_orders_delivered():
    all_orders = list()
    for order in orders_delivered.values():
        dictionary = order.get_dict()
        all_orders.append(dictionary)

    return response(all_orders)

# Register with a flower shop
@app.route("/register")
def register():
    flower_shop_url = request.args.get("uri")
    get_params = dict()
    get_params["uri"] = driver_url
    response = requests.get(flower_shop_url, params=get_params)
    return create_response(response)


def calculate_bid(order, location):
    bid = directions_api.secondsA2B(location, order.location)
    print("secondsA2B is " + str(bid) + " for order " + str(order.correlation_id))
    order_temp = get_temp(order.location)
    current_temp = get_temp(location)
    temp = (order_temp + current_temp) / 2.0
    print ("temp is " + str(temp))
    if temp < 40:
        bid += 10 * (40 - temp)
    elif temp > 80:
        bid += 12 * (80 - temp)

    return bid


# Call Weather Underground API
def get_temp(location):
    loc = location.split(",")
    lat = loc[0]
    long = loc[1]
    return weather_api.get_temp(lat, long)


def create_response(response):
    return response.text, response.status_code, response.headers.items()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Running on port 5000")
        port = 5000
    else:
        port = int(sys.argv[1])
        driver_url = "http://localhost:" + str(port)
    app.run(host='0.0.0.0', port=port)
