import time
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares, solve_history 
from easy_trilateration.graph import *  
from math import log10
import database_methods as daytum
import firebase_admin
from firebase_admin import credentials, firestore
'''
However it is not recommended to do what is being done here and ideally the following should be used:
1. A dynamic loss model (Adjusts the FSPL based on real-time measurements or smt)
2. A log-distance path loss model with a tunnel-specific path loss exponent n. 
    For example, tunnels might have an n value between 1.6 and 2.1, instead of the typical 2 used 
    in free-space models. Link to example n values: https://medium.com/@isallam/back-to-basics-1-1aa688aa53c0
'''

# This is a function that calculates distance based on a certain signal strength, 
# can be used in testing towards the later stages
def calculate_distance(signal_strength, frequency):
    """Convert signal strength to distance."""
    # This is a simplified version, where stronger signal -> smaller distance
    # Formula: d = 10^((P_tx - P_rx) / (10 * n))
    # We'll assume a path loss exponent (n) of 2 (free space)
    path_loss_exponent = 2
    reference_signal = -30  # Assume -30 dBm at 1 meter
    distance = 10 ** ((reference_signal - signal_strength) / (10 * path_loss_exponent))
    return distance


# Free-Space Path Loss


def signal_to_distance(mhz, dbm):
    # Free-Space Path Loss adapted avarage constant for home WiFI routers and following units
    # A source like does abs(dbm) to get I
    FSPL = 27.55 # For now it is an approximation that mainly works with routers and access points
    n = 3  # Path loss exponent for indoor environments (FOR TESTING PURPOSES, this constant will differ for the tunnel)
    m = 10 ** (( FSPL - (20 * log10(mhz)) + abs(dbm)) / (10 * n) )
   
    return m

arr = [
    Circle(100, 100, 50),  
    Circle(100, 50, 50),  
    Circle(50, 50, 50),  
    Circle(50, 100, 50)
]  

# This is just a testing function that trilaterates and prints things from an array
# def trilaterate_test(arr):
#     result, meta = easy_least_squares(arr)  
#     create_circle(result, target=True)
#     print(result)
#     draw(arr)

"""
# This is code that is made for that one room in the library with 3 reference APs that trilaterate

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

# TODO: incorporate this function into the main server

# This is made for the actual data that comes from the android device
# ref_APs = {
#     'bssid1': (4, 0),
#     'bssid2': (10, 9),    
#     'bssid3': (1, 10)
# }

# import numpy as np

# class EKF:
#     def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise, access_points):
#         self.state = np.array(initial_state)  # Initial state [x, y]
#         self.covariance = np.array(initial_covariance)  # Initial covariance matrix
#         self.Q = np.array(process_noise)  # Process noise covariance matrix
#         self.R = np.array(measurement_noise)  # Measurement noise covariance matrix
#         self.access_points = np.array(access_points)  # Known APs [[x1, y1], [x2, y2], ...]

#     def predict(self, u, dt):
#         """
#         Predict step: Updates the state based on the motion model (e.g., assuming simple motion)
#         u: Control input (e.g., velocity vector [vx, vy])
#         dt: Time delta
#         """
#         # Simple motion model: x' = x + vx * dt, y' = y + vy * dt
#         F = np.array([[1, 0], [0, 1]])  # State transition matrix (identity for simplicity)
#         self.state = np.dot(F, self.state) + u * dt
#         self.covariance = np.dot(np.dot(F, self.covariance), F.T) + self.Q

#     def update(self, rssi_readings):
#         """
#         Update step: Updates the state based on the RSSI measurements
#         rssi_readings: List of RSSI measurements corresponding to known APs
#         """
#         H = []  # Jacobian matrix of partial derivatives of h(x) w.r.t state
#         z = []  # Measurement vector

#         for i, rssi in enumerate(rssi_readings):
#             # Calculate expected distance based on current state and AP location
#             dx = self.state[0] - self.access_points[i][0]
#             dy = self.state[1] - self.access_points[i][1]
#             expected_distance = np.sqrt(dx**2 + dy**2)
            
#             # Measurement model h(x): distance = sqrt((x - AP_x)^2 + (y - AP_y)^2)
#             H_i = np.array([dx / (expected_distance + 1e-6), dy / (expected_distance + 1e-6)])  # Avoid division by zero
#             H.append(H_i)

#             # Convert RSSI to distance (assuming a path-loss model for simplicity)
#             z_i = self.rssi_to_distance(rssi)
#             z.append(z_i)

#         H = np.array(H)
#         z = np.array(z)

#         # Predicted measurement
#         h_x = np.array([np.sqrt((self.state[0] - ap[0])**2 + (self.state[1] - ap[1])**2) for ap in self.access_points])

#         # Calculate Kalman gain
#         S = np.dot(np.dot(H, self.covariance), H.T) + self.R
#         K = np.dot(np.dot(self.covariance, H.T), np.linalg.inv(S))

#         # Update state and covariance
#         y = z - h_x  # Innovation (measurement residual)
#         self.state = self.state + np.dot(K, y)
#         I = np.eye(len(self.state))
#         self.covariance = np.dot(I - np.dot(K, H), self.covariance)

# # Example usage
# initial_state = [0, 0]  # Initial position
# initial_covariance = [[1, 0], [0, 1]]  # Initial covariance matrix
# measurement_noise = [[10]]  # Example variance for RSSI, assuming a single AP (adjust based on measurements)
# process_noise = [[0.05, 0], [0, 0.05]]  # Variance for state transition (position components in x and y directions)

# ekf = EKF(initial_state, initial_covariance, process_noise, measurement_noise, access_points)
# ekf.predict(u=np.array([1, 1]), dt=1)  # Predict step with some control input
# ekf.update([-70, -65, -80])  # Update step with RSSI readings
# print("Estimated state:", ekf.state)


def trilaterate_actual(data, ref_APs):
    arr = []
    for accessPoint in data["accessPoints"]:
        print(accessPoint['bssid'])
        if accessPoint['bssid'] in list(ref_APs.keys()):
            print(f"hi {accessPoint}")
            # Finding the index of the BSSID
            # index = ref_BSSIDs.index(accessPoint['bssid'])
            # currentAP = ref_APs[index]
            bssid = accessPoint['bssid']
            coords = ref_APs[bssid]
            

            distance = signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"])
            arr.append(Circle(coords["x"], coords["y"], distance))
    print(arr)
    # trilaterate_test(arr)
    try:
        return easy_least_squares(arr)  
        create_circle(result, target=True)
        print(result)
        # draw(arr)
    except Exception as e:
        print(f"Trilateration failed for AP {accessPoint['bssid']} due to: {e}")
        return []

# TODO: refer to line 201 in index.py for db schema

# memo stores where the APs are using trilateration follows the following schema:
# {
# "mac": (Circle(3, 3, 5), {some long ass info abt the thing})
# }

# TODO: memo and insufficient circles to be replaced by database
# this stores the circles of the user (with each circles
# radius being the length to each AP)

# This is a function that will be called multiple times, and it will update the memo as required
# user_loc is a tuple (x, y)
ignoremac = ["60:b9:c0:97:c6:ac",
             "88:d7:f6:a8:b1:7c",
             "60:b9:c0:97:c6:cc",
             "60:b9:c0:7e:ac:8b",
             "60:b9:c0:7e:9c:eb",
             "60:b9:c0:7e:b9:ab",
             "60:b9:c0:7e:2e:4c",
             "60:b9:c0:7e:b2:6c",
             "60:b9:c0:7e:36:ac"
             ,"60:b9:c0:7e:29:4c","60:b9:c0:7e:33:8c","60:b9:c0:7e:2b:0c","60:b9:c0:7e:6c:8c"]
def find_new_APs(data_variant, user_loc,db):
    # to make data variant only top 5
    # data = array of top 5 in data_variant["accessPoints"]
    data = daytum.top5(data_variant["accessPoints"],ascending=True)
    pulledmemo = daytum.get_collection_data("Access Points")
    memo ={
    i["mac"] : Circle(
        i["coordinates"]["x"],
        i["coordinates"]["y"],
        i["radius"]
    ) for i in pulledmemo if i["coordinates"]["x"] != None and i["mac"] not in ignoremac
    }
    pulledcircles = daytum.select_field("Access Points","trilat","mac")
    
    insufficient_circles = {}
    for a in pulledcircles:
        print(pulledcircles[a])
        if a not in ignoremac:
            templist = [Circle(i["x"],i["y"],i["radius"]) for i in pulledcircles[a]]
            insufficient_circles[a] = templist
    # insufficient_circles = {
    # i : Circle(
    #     pulledcircles[i]["x"],
    #     pulledcircles[i]["y"],
    #     pulledcircles[i]["radius"]
    # ) for i in pulledcircles 
    # }
    print(insufficient_circles,memo)
    existance = daytum.get_collection_names("Access Points")
    for accessPoint in data:
        if accessPoint["bssid"] not in existance:
            daytum.add("Access Points",accessPoint["bssid"],{"coordinates":{"x":None,"y":None},"radius":None,"trilat":[],"mac":accessPoint["bssid"]})
        distance = signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"])
        
        # the circles that we have calculated for the current AP
        circleInfo = insufficient_circles.get(accessPoint["bssid"], [])
        if circleInfo == []:
            # create AP in insufficient_circles
            insufficient_circles[accessPoint["bssid"]] = [Circle(user_loc[0], user_loc[1], distance)]
        else:
            insufficient_circles[accessPoint["bssid"]].append(Circle(user_loc[0], user_loc[1], distance))
            
            # This is done in a way where this will always trilaterate as long as there is 
            # 3 or more, it will not delete the element from the circleInfo array
            if len(insufficient_circles[accessPoint["bssid"]]) >= 3:
                
                try:
                    data,check = easy_least_squares(insufficient_circles[accessPoint["bssid"]])# need change initial guess too if possible for future me
                    if data.radius>=-10 and data.radius<=10:# i need to see if smt like this will work
                        memo[accessPoint["bssid"]] = Circle(user_loc[0], user_loc[1], distance)
                        # if not ignore:
                        daytum.update("Access Points",accessPoint["bssid"],{"coordinates":{"x":data.center.x,"y":data.center.y},"radius":data.radius})
                        # create_circle(memo[accessPoint["bssid"]][0], target=True)
                        # TODO: UNCOMMENT ME FOR TESTING
                        # draw(insufficient_circles[accessPoint["bssid"]])
                    else:
                        insufficient_circles[accessPoint["bssid"]].pop()

                except Exception as e:
                    print(f"Trilateration failed for AP {accessPoint['bssid']} due to: {e}")
                    

    for i in insufficient_circles:
        print(i,insufficient_circles[i])
        for a in range(len(insufficient_circles[i])):
            temp = insufficient_circles[i][a]
            insufficient_circles[i][a] = {"x":temp.center.x,"y":temp.center.y,"radius":temp.radius}
    print(insufficient_circles)

    for i in insufficient_circles:
        # transaction = db.transaction()
        # daytum.transactional_update(transaction,"Access Points",i,{"trilat":insufficient_circles[i]})
        daytum.update_field("Access Points",i,"trilat",insufficient_circles[i])


# from dummydata import data_variant_1, data_variant_2, data_variant_3
# find_new_APs(data_variant_1, (12, 5))
# find_new_APs(data_variant_2, (8, 19))
# find_new_APs(data_variant_3, (3, 14))
# print(memo)



data = {
    "accessPoints": [
        {
            "ssid": "ssid1",
            "bssid": "bssid1",
            "signalStrength": -20,
            "frequency": 5040
        },
        {
            "ssid": "ssid1",
            "bssid": "bssid2",
            "signalStrength": -60,
            "frequency": 5040
        },
        {
            "ssid": "ssid1",
            "bssid": "bssid3",
            "signalStrength": -60,
            "frequency": 5040
        }
    ],
    "user": "alonzo"
}
# trilaterate_actual(data)