import database_methods as daytum
from easy_trilateration.model import Circle
from trilateration import find_new_APs
db = daytum.setup()
users = ["Darius"]
user_name = "Darius"
# if user_name in users:
#     # user = users[user_name]
#     # user.previous_coordinates = user.current_coordinates.copy()  # Store previous
#     # user.current_coordinates = new_coords  # Update current coordinates
#         user = daytum.get_document("Users",user_name)
#         daytum.update_field("Users",user_name,"previous_coordinates",user["current_coordinates"])
#         user = daytum.get_document("Users",user_name)
#         print(user)
class circle:
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
def classtodict(x):
    return {"x":x.x,"y":x.y,"radius":x.radius}
def dicttoclass(x):
    return circle(x["x"],x["y"],x["radius"])
#darius, alonzo phone, alonzo computer
mac = ["60:b9:c0:97:c6:ac","88:d7:f6:a8:b1:7c","60:b9:c0:97:c6:cc"]
# 60:b9:c0:97:c6:ac is esc np wireless x ap
# 88:d7:f6:a8:b1:7c is esc own router
data = circle(4,3,1)



# transaction = db.transaction()
# daytum.transactional_update(transaction,"test","test",{"radius":data.radius,"coordinates":{"x":data.x,"y":data.y},"trilat":circleinfo})
# pulledcircles = daytum.select_field("test","trilat","mac")
# print(pulledcircles)
# insufficient_circles = {i:circle(pulledcircles[i]["x"],pulledcircles[i]["y"],pulledcircles[i]["radius"]) for i in pulledcircles }
# print(insufficient_circles)
# Sample Data Variant
data_variant = {
    "accessPoints": [{'ssid': 'Darius’s iPhone', 'signalStrength': -46, 'bssid': '7e:f3:ed:c5:27:52', 'frequency': 5745}, {'ssid': 'NPWirelessx', 'signalStrength': -88, 'bssid': '60:b9:c0:7e:93:8b', 'frequency': 5220}, {'ssid': 'POLITE-CET', 'signalStrength': -88, 'bssid': '60:b9:c0:7e:93:8c', 'frequency': 5220}, {'ssid': 'NPWireless', 'signalStrength': -89, 'bssid': '60:b9:c0:7e:93:8d', 'frequency': 5220}, {'ssid': 'NP-Guest', 'signalStrength': -88, 'bssid': '60:b9:c0:7e:93:8e', 'frequency': 5220}, {'ssid': 'SIT-POLY', 'signalStrength': -88, 'bssid': '60:b9:c0:7e:93:8f', 'frequency': 5220}, {'ssid': 'NPWirelessx', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:ac:8b', 'frequency': 5180}, {'ssid': 'POLITE-CET', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:ac:8c', 'frequency': 5180}, {'ssid': 'NPWireless', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:ac:8d', 'frequency': 5180}, {'ssid': 'NP-Guest', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:ac:8e', 'frequency': 5180}, {'ssid': 'SIT-POLY', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:ac:8f', 'frequency': 5180}, {'ssid': 'NPWireless', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:c9:42', 'frequency': 2462}, {'ssid': 'NP-Guest', 'signalStrength': -80, 'bssid': '60:b9:c0:7e:c9:41', 'frequency': 2462}, {'ssid': 'POLITE-CET', 'signalStrength': -80, 'bssid': '60:b9:c0:7e:c9:43', 'frequency': 2462}, {'ssid': 'NPWirelessx', 'signalStrength': -73, 'bssid': '60:b9:c0:7e:ac:84', 'frequency': 2437}, {'ssid': 'BlackVue590X-EDC54D', 'signalStrength': -89, 'bssid': '00:25:42:ed:c5:4d', 'frequency': 2437}, {'ssid': 'SIT-POLY', 'signalStrength': -73, 'bssid': '60:b9:c0:7e:ac:80', 'frequency': 2437}, {'ssid': 'POLITE-CET', 'signalStrength': -72, 'bssid': '60:b9:c0:7e:ac:83', 'frequency': 2437}, {'ssid': 'NPWireless', 'signalStrength': -72, 'bssid': '60:b9:c0:7e:ac:82', 'frequency': 2437}, {'ssid': 'NP-Guest', 'signalStrength': -72, 'bssid': '60:b9:c0:7e:ac:81', 'frequency': 2437}, {'ssid': 'NP-Guest', 'signalStrength': -70, 'bssid': '60:b9:c0:7e:9c:e1', 'frequency': 2412}, {'ssid': 'SIT-POLY', 'signalStrength': -69, 'bssid': '60:b9:c0:7e:9c:e0', 'frequency': 2412}]
}
mac = ["60:b9:c0:7e:29:4c","60:b9:c0:7e:33:8c","60:b9:c0:7e:2b:0c","60:b9:c0:7e:6c:8c"]
# Sample User Location
user_loc = (90, 20)
# pulledcircles = daytum.select_field("Access Point     s","trilat","mac")  
# print(pulledcircles)
from trilateration import ignoremac
ap = daytum.get_collection_names("Access Points")
# for i in ap:
#     if i not in ignoremac:
#         print("delete")
#         daytum.delete("Access Points",i)
# import time
# start = time.time()
# data = {"accessPoints":[{'ssid': 'ArthurHome', 'signalStrength': -61, 'bssid': '58:ef:68:32:a1:3b', 'frequency': 5765}, {'ssid': '', 'signalStrength': -77, 'bssid': 'e8:9c:25:ac:d2:48', 'frequency': 5745}, {'ssid': '', 'signalStrength': -90, 'bssid': '8c:3b:ad:c2:63:72', 'frequency': 5580}, {'ssid': 'ArthurHome', 'signalStrength': -51, 'bssid': '58:ef:68:32:a2:0c', 'frequency': 5200}, {'ssid': 'CKGJS_5G-1', 'signalStrength': -85, 'bssid': 'e8:9c:25:ac:d2:44', 'frequency': 5180}, {'ssid': 'ArthurHome', 'signalStrength': -59, 'bssid': '80:69:1a:87:b3:7c', 'frequency': 2472}, {'ssid': '', 'signalStrength': -85, 'bssid': 'de:ec:5e:7c:0a:b1', 'frequency': 2467}, {'ssid': '', 'signalStrength': -86, 'bssid': '72:a0:67:53:e9:8d', 'frequency': 2462}, {'ssid': '', 'signalStrength': -84, 'bssid': '7e:e9:31:02:3e:4b', 'frequency': 2457}, {'ssid': 'TP-Link_AH_Home', 'signalStrength': -83, 'bssid': '5c:e9:31:02:3e:4b', 'frequency': 2457}, {'ssid': 'ArthurHome', 'signalStrength': -42, 'bssid': '58:ef:68:32:a2:0b', 'frequency': 2452}, {'ssid': 'ArthurHome', 'signalStrength': -63, 'bssid': '58:ef:68:32:a1:39', 'frequency': 2452}, {'ssid': '', 'signalStrength': -42, 'bssid': '5e:ef:68:32:a2:0b', 'frequency': 2452}, {'ssid': 'Razarusu_Room', 'signalStrength': -75, 'bssid': '34:60:f9:d3:84:97', 'frequency': 2427}, {'ssid': 'Razarusu_Room', 'signalStrength': -60, 'bssid': '08:bf:b8:b6:13:98', 'frequency': 2427}, {'ssid': 'alone iphone', 'signalStrength': -19, 'bssid': 'e2:e2:41:3c:f6:be', 'frequency': 5745}]}
# find_new_APs(data,(0,0),db)
# elapsed = time.time()-start
# print(f"elapsed: {elapsed}")
for i in mac:
    daytum.add("Access Points",i.lower(), {"coordinates":{"x":None, "y":None},"mac":i.lower(),"radius":0,"trilat":[]})
