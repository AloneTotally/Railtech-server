import time
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
    # start = time.perf_counter()
    # print("start",start)
    # Free-Space Path Loss adapted avarage constant for home WiFI routers and following units

    # A source like does abs(dbm) to get I
    m = 10 ** (( FSPL - (20 * log10(mhz)) + abs(dbm)) / (10 * n) )
    # m=round(m,2)
    # end = time.perf_counter()
    # print("end",end)
    # print(f"Elapsed time: {end - start} seconds")    
    return m

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
def trilaterate_test(arr):
    result, meta = easy_least_squares(arr)  
    create_circle(result, target=True)
    print(result)
    draw(arr)

"""

arr = [
    (80, 2.4),
    (90, 2.4),
    (43, 5)
]

quality = 43
ghz = 5
radii = []

# 200 degrees - 2.1m
# 154 degrees - 17m
# 328 - 11m

for i in arr:
    # dBm = (quality / 2) - 100
    # mhz = ghz*1000
    # print(signal_to_distance(mhz, dBm))
    dBm = (i[0] / 2) - 100
    mhz = i[1]*1000
    radii.append(signal_to_distance(mhz, dBm))
    print(signal_to_distance(mhz, dBm))

import math
trilaterate_test([
    Circle(17* math.cos(154-90), -17 * math.cos(180-154), radii[0]), # bc:54:2f:4c:71:3d
    Circle(-2.1 * math.sin(200-180), -2.1 * math.cos(200-180), radii[1]), # 3c:33:32:49:8c:a0 
    Circle(-11 * math.sin(360-328), 11*math.cos(360-328), radii[2]) # 60:b9:c0:98:77:cf
])
"""

# TODO: Discover AP location
# TODO: incorporate this function into the main server

def trilaterate_actual(data):
    ref_APs = [
        {"coords": (4, 0), "bssid": 'bssid1'},
        {"coords": (10, 9), "bssid": 'bssid2'},
        {"coords": (1, 10), "bssid": 'bssid3'}
    ]

    ref_BSSIDs = [
        ref_APs[0]["bssid"], ref_APs[1]["bssid"], ref_APs[2]["bssid"], 
    ]

    arr = []

    for accessPoint in data["accessPoints"]:
        if accessPoint['bssid'] in ref_BSSIDs:
            # Finding the index of the BSSID
            index = ref_BSSIDs.index(accessPoint['bssid'])
            currentAP = ref_APs[index]

            distance = signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"])
            arr.append(Circle(currentAP["coords"][0], currentAP["coords"][1], distance))

    trilaterate_test(arr)

memo = {
    # ((x, y), radius)
    # "bssid1": (Circle(3, 3, 5), {memo})
}
insufficient_circles = {}

# This is a function that will be called multiple times, and it will update the memo as required
# user_loc is a tuple (x, y)
def find_new_APs(data_variant, user_loc):
    for accessPoint in data_variant["accessPoints"]:
        distance = signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"])
        
        # the circles that we have calculated for the current AP
        circleInfo = insufficient_circles.get(accessPoint["bssid"], [])
        if circleInfo == []:
            # create AP in circles_insufficient
            insufficient_circles[accessPoint["bssid"]] = [Circle(user_loc[0], user_loc[1], distance)]
        else:
            insufficient_circles[accessPoint["bssid"]].append(Circle(user_loc[0], user_loc[1], distance))
            
            # This is done in a way where this will always trilaterate as long as there is 
            # 3 or more, it will not delete the element from the circleInfo array
            if len(circleInfo) >= 3:

                try:
                    memo[accessPoint["bssid"]] = easy_least_squares(insufficient_circles[accessPoint["bssid"]])
                    create_circle(memo[accessPoint["bssid"]][0], target=True)
                    draw(insufficient_circles[accessPoint["bssid"]])

                except Exception as e:
                    print(f"Trilateration failed for AP {accessPoint['bssid']} due to: {e}")

from dummydata import data_variant_1, data_variant_2, data_variant_3
find_new_APs(data_variant_1, (12, 5))
find_new_APs(data_variant_2, (8, 19))
find_new_APs(data_variant_3, (3, 14))
print(memo)



data = {
    "accessPoints": [
        {
            "ssid": 'ssid1',
            "bssid": 'bssid1',
            "signalStrength": -20,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid2',
            "signalStrength": -60,
            "frequency": 5040
        },
        {
            "ssid": 'ssid1',
            "bssid": 'bssid3',
            "signalStrength": -60,
            "frequency": 5040
        },
    ],
    "user": "alonzo",
}
# trilaterate_actual(data)