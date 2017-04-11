# for command line args
import sys
# json.loads() will turn json string to python object
# json.dumps() will turn python object to json string
import json
import requests
import random
import directions_api
from order import Order
# here are many imports from flask you may want to use
from flask import Flask, redirect, request, make_response, send_from_directory, render_template


app = Flask(__name__)

# The correlation_id of the order will be the key and the Order object the value
orders_received = dict()
delivered_orders = dict()
driver_name = random.randint(0,999999)
port = 5000

def generate_location():
    latitude = random.uniform(35,40)
    longitude = random.uniform(-110,-80)
    location = str(latitude) + "," + str(longitude)
    return location

location = generate_location()
print location

# Endpoint to receive an order from a flower shop
@app.route('/order')
def send_bid():
    #    def __init__(self, flower_shop_url, location, correlation_id):
	flower_shop_url = request.args.get("uri")
	location = request.args.get("location")
	id = request.args.get("id")
	order = Order(flower_shop_url, location, id)
	orders_received[id] = order
	bid = calculate_bid(order)
	get_params = dict()
	get_params["drivername"] = driver_name
	get_params["bid"] = bid
	get_params["orderid"] = order.correlation_id
	response = requests.get(flower_shop_url, params=get_params)
	return create_response(response)


@app.route('/deliverorder')
def deliver_order():
	return "Unimplemented"

# Register with a flower shop
@app.route("/register")
def register():
	flower_shop_url = request.args.get("uri")
	get_params = dict()
	get_params["drivername"] = driver_name
	get_params["uri"] = "http://localhost:" + str(port)
	response = requests.get(flower_shop_url, params=get_params)
	return create_response(response)

def calculate_bid(order):
    bid =  directions_api.secondsA2B(location, order.location)
    temp = get_weather(order.location)

    if temp < 40:
        bid += 10 * 40 - temp
    elif temp > 80:
        bid += 12 * 80 - temp

    return bid

# Call Weather Underground API
def get_weather(location):
	return 81

def create_response(response):
	return (response.text, response.status_code, response.headers.items())


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Running on port 5000"
		port = 5000
	else:
		port = int(sys.argv[1])

	app.run(host='0.0.0.0', port=port)
