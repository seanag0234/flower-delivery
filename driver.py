# for command line args
import sys
# json.loads() will turn json string to python object
# json.dumps() will turn python object to json string
import json

# here are many imports from flask you may want to use
from flask import Flask, redirect, request, make_response, send_from_directory, render_template


app = Flask(__name__)


@app.route('/example')
def example():
	response = make_response()
	response.headers['Content-Type'] = 'application/json'
	response.data = '{"JSON": True}'
	return response


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Pass a port number to run on')
	else:
		port = int(sys.argv[1])
		app.run(host='0.0.0.0', port=port)
