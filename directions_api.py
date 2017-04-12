# api key: AIzaSyBKCGfjVLeKmVKKROH_omQEozOQn5vowqI
# example request:
# https://maps.googleapis.com/maps/api/directions/json?origin=941+E+25+S+Lindon+Utah&destination=Universal+Studios+Hollywood4&key=AIzaSyBKCGfjVLeKmVKKROH_omQEozOQn5vowqI
import json
import requests
import re

# input coordinates in the form '40.3371336,-111.6921782' or use english
def secondsA2B(A, B):
    url = makeurl(A, B)
    jsonstr = requests.get(url).content
    data = json.loads(jsonstr)
    if (data['status'] != 'OK'):
        return 0
    return data['routes'][0]['legs'][0]['duration']['value']

def makeurl(A, B):
    url = 'https://maps.googleapis.com/maps/api/directions/json?key=AIzaSyBKCGfjVLeKmVKKROH_omQEozOQn5vowqI&origin='
    url += urlify(A) +'&destination='+ urlify(B)
    return url

def urlify(s):
    # Remove all non-word characters (everything except numbers, letters, and these '-.,')
    s = re.sub(r"[^\w\s\-.,]", '', s)
    # Replace all runs of whitespace with a +
    s = re.sub(r"\s+", '+', s)
    return s