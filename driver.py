# for command line args
import sys
# json.loads() will turn json string to python object
# json.dumps() will turn python object to json string
import json

# here are many imports from flask you may want to use
from flask import Flask, redirect, request, make_response, send_from_directory, render_template


app = Flask(__name__)

# The correlation_id of the order will be the key and the Order object the value
orders = dict()
driver_name = ''

# Endpoint to receive an order from a flower shop
@app.route('/order')
def send_bid(order="fsda"):
	return "Unimplemented"

@app.route('/deliverorder')
def deliver_order(order):
	return "Unimplemented"

def send_bid(bid):
	return "Unimplemented"

def calculate_bid(order):
	return "Unimplemented"

# Call Google Maps API
def get_distance(location):
	return "Unimplemented"

# Call Weather Underground API
def get_weather(location):
	return "Unimplemented"

# Send the
def deliver_order(order):
	return "Unimplemented"

# Register with a flower shop
def register(url):
	return "Unimplemented"

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Running on port 5000"
		port = 5000
	else:
		port = int(sys.argv[1])

	app.run(host='0.0.0.0', port=port)
