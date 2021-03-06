import os
import time
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-d", default=5, help="the number of drivers wanted")
parser.add_argument("-f", default=2, help="the number of flower shops wanted")
parser.add_argument("-t", default=3, help="delay before starting the freeport command")
args = parser.parse_args()

num_drivers = int(args.d)
driver_port = 5000
num_flowershops = int(args.f)
flower_port = 4000

delay = int(args.t)

for i in range(0, num_drivers):
    filename = "d:" + str(driver_port + i) + ".txt"
    open(filename, 'a')
    os.system("python driver.py " + str(driver_port + i) + " > " + filename + " 2>&1 &")
    # os.system("python driver.py " + str(driver_port + i) + "&")

for i in range(0, num_flowershops):
    filename = "f:" + str(flower_port + i) + ".txt"
    open(filename, 'a')
    os.system("python flowershop.py " + str(flower_port + i) + " > " + filename + " 2>&1 &")
    # os.system("python flowershop.py " + str(flower_port + i) + "&")

time.sleep(delay)

# This automatically registers the drivers with the shops don't use when testing gossip
for f in range(0, num_flowershops):
    port = flower_port
    for i in range(0, num_drivers):
        requests.get("http://localhost:" + str(driver_port + i) + "/register?uri=http://localhost:" + str(port) + "/register")

# You will need to pip install freeport in your environment for this section to work
# This section will kill the processes running on the ports that the script uses
# You will have to type yes for each process in the terminal

for i in range(0, num_drivers):
   os.system("freeport " + str(driver_port + i))

for i in range(0, num_flowershops):
   os.system("freeport " + str(flower_port + i))