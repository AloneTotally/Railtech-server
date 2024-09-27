
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares, solve_history 
from easy_trilateration.graph import *  

example_json = {
    "accessPoints": [
        {
            "bssid": "11FYUKGF21324",
            "distance": 10
        },
        {
            "bssid": "22CFYUGFYRHTR6",
            "distance": 30
        },
        {
            "bssid": "3389765GHJKMHG",
            "distance": 50
        }
    ],
    "user": "alonzo"
},


from math import log10

'''
However it is not recommended to do what is being done here and ideally the following should be used:
1. A dynamic loss model (Adjusts the FSPL based on real-time measurements or smt)
2. A log-distance path loss model with a tunnel-specific path loss exponent n. 
    For example, tunnels might have an n value between 1.6 and 2.1, instead of the typical 2 used 
    in free-space models. Link to example n values: https://medium.com/@isallam/back-to-basics-1-1aa688aa53c0
'''


# Free-Space Path Loss
FSPL = 27.55 # For now it is an approximation that mainly works with routers and access points
n = 3  # Path loss exponent for indoor environments (FOR TESTING PURPOSES, this constant will differ for the tunnel)

def signal_to_distance(mhz, dbm):
    # import time
    # start = time.time()
    # Free-Space Path Loss adapted avarage constant for home WiFI routers and following units

    # A source like does abs(dbm) to get I
    m = 10 ** (( FSPL - (20 * log10(mhz)) + abs(dbm)) / (10 * n) )
    # m=round(m,2)
    # end = time.time()
    return m #, end- start

# arr = [
#     Circle(Point(100, 100), 50),  
#     Circle(Point(100, 50), 50),  
#     Circle(Point(50, 50), 50),  
#     Circle(Point(50, 100), 50)
# ]

arr = [
    Circle(100, 100, 50),  
    Circle(100, 50, 50),  
    Circle(50, 50, 50),  
    Circle(50, 100, 50)
]  
def trilaterate(arr):
    result, meta = easy_least_squares(arr)  
    create_circle(result, target=True)
    print(result)
    draw(arr)

quality = 6
ghz = 5

dBm = (quality / 2) - 100
mhz = ghz*1000
# print(signal_to_distance(mhz, dBm))
trilaterate(arr)