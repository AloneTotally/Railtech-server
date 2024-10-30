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
    "accessPoints": [{'ssid': 'NPWirelessx', 'signalStrength': -88, 'bssid': '60:b9:c0:98:cf:2b', 'frequency': 5785}, {'ssid': 'POLITE-CET', 'signalStrength': -88, 'bssid': '60:b9:c0:98:cf:2c', 'frequency': 5785}, {'ssid': 'NPWireless', 'signalStrength': -88, 'bssid': '60:b9:c0:98:cf:2d', 'frequency': 5785}, {'ssid': 'NP-Guest', 'signalStrength': -87, 'bssid': '60:b9:c0:98:cf:2e', 'frequency': 5785}, {'ssid': 'SIT-POLY', 'signalStrength': -88, 'bssid': '60:b9:c0:98:cf:2f', 'frequency': 5785}, {'ssid': 'POLITE-CET', 'signalStrength': -89, 'bssid': 'c0:25:5c:de:cf:9b', 'frequency': 5745}, {'ssid': 'NPWirelessx', 'signalStrength': -88, 'bssid': '34:db:fd:66:4b:1e', 'frequency': 5805}, {'ssid': 'NPWireless', 'signalStrength': -88, 'bssid': 'c0:25:5c:de:cf:9f', 'frequency': 5745}, {'ssid': 'NP-Guest', 'signalStrength': -87, 'bssid': '60:b9:c0:98:f5:ae', 'frequency': 5660}, {'ssid': 'NPWirelessx', 'signalStrength': -67, 'bssid': '60:b9:c0:7e:9c:eb', 'frequency': 5620}, {'ssid': 'POLITE-CET', 'signalStrength': -67, 'bssid': '60:b9:c0:7e:9c:ec', 'frequency': 5620}, {'ssid': 'NPWireless', 'signalStrength': -67, 'bssid': '60:b9:c0:7e:9c:ed', 'frequency': 5620}, {'ssid': 'NP-Guest', 'signalStrength': -67, 'bssid': '60:b9:c0:7e:9c:ee', 'frequency': 5620}, {'ssid': 'SIT-POLY', 'signalStrength': -66, 'bssid': '60:b9:c0:7e:9c:ef', 'frequency': 5620}, {'ssid': 'SIT-POLY', 'signalStrength': -91, 'bssid': '60:b9:c0:7e:c9:4f', 'frequency': 5600}, {'ssid': 'NPWirelessx', 'signalStrength': -79, 'bssid': '60:b9:c0:7e:b9:ab', 'frequency': 5500}, {'ssid': 'POLITE-CET', 'signalStrength': -79, 'bssid': '60:b9:c0:7e:b9:ac', 'frequency': 5500}, {'ssid': 'NPWireless', 'signalStrength': -79, 'bssid': '60:b9:c0:7e:b9:ad', 'frequency': 5500}, {'ssid': 'NP-Guest', 'signalStrength': -79, 'bssid': '60:b9:c0:7e:b9:ae', 'frequency': 5500}, {'ssid': 'SIT-POLY', 'signalStrength': -79, 'bssid': '60:b9:c0:7e:b9:af', 'frequency': 5500}, {'ssid': 'LTE-WiFi_5G_1165', 'signalStrength': -87, 'bssid': '74:f8:db:6b:11:68', 'frequency': 5260}, {'ssid': 'NPWirelessx', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:93:8b', 'frequency': 5220}, {'ssid': 'POLITE-CET', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:93:8c', 'frequency': 5220}, {'ssid': 'NPWireless', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:93:8d', 'frequency': 5220}, {'ssid': 'NP-Guest', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:93:8e', 'frequency': 5220}, {'ssid': 'SIT-POLY', 'signalStrength': -81, 'bssid': '60:b9:c0:7e:93:8f', 'frequency': 5220}, {'ssid': 'NPWirelessx', 'signalStrength': -83, 'bssid': '60:b9:c0:7e:ac:8b', 'frequency': 5180}, {'ssid': 'POLITE-CET', 'signalStrength': -84, 'bssid': '60:b9:c0:7e:ac:8c', 'frequency': 5180}, {'ssid': 'NPWireless', 'signalStrength': -84, 'bssid': '60:b9:c0:7e:ac:8d', 'frequency': 5180}, {'ssid': 'NP-Guest', 'signalStrength': -84, 'bssid': '60:b9:c0:7e:ac:8e', 'frequency': 5180}, {'ssid': 'SIT-POLY', 'signalStrength': -84, 'bssid': '60:b9:c0:7e:ac:8f', 'frequency': 5180}, {'ssid': 'Koufu_Staff', 'signalStrength': -75, 'bssid': '60:d0:2c:69:7f:f8', 'frequency': 2472}, {'ssid': 'Kf@NAP', 'signalStrength': -76, 'bssid': '60:d0:2c:29:7f:f8', 'frequency': 2472}, {'ssid': 'POLITE-CET', 'signalStrength': -87, 'bssid': '60:b9:c0:7e:c9:43', 'frequency': 2462}, {'ssid': 'NPWireless', 'signalStrength': -85, 'bssid': '60:b9:c0:7e:c9:42', 'frequency': 2462}, {'ssid': 'POLITE-CET', 'signalStrength': -69, 'bssid': '60:b9:c0:7e:ac:83', 'frequency': 2437}, {'ssid': 'NPWireless', 'signalStrength': -69, 'bssid': '60:b9:c0:7e:ac:82', 'frequency': 2437}, {'ssid': 'NP-Guest', 'signalStrength': -69, 'bssid': '60:b9:c0:7e:ac:81', 'frequency': 2437}, {'ssid': 'SIT-POLY', 'signalStrength': -69, 'bssid': '60:b9:c0:7e:ac:80', 'frequency': 2437}, {'ssid': '\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5\uf8f5', 'signalStrength': -84, 'bssid': '7c:a7:b0:86:15:47', 'frequency': 2432}, {'ssid': 'Darius’s iPhone', 'signalStrength': -49, 'bssid': '7e:f3:ed:c5:27:52', 'frequency': 5745}, {'ssid': 'NPWireless', 'signalStrength': -63, 'bssid': '60:b9:c0:7e:9c:e2', 'frequency': 2412}, {'ssid': 'NP-Guest', 'signalStrength': -64, 'bssid': '60:b9:c0:7e:9c:e1', 'frequency': 2412}]
}
mac = ["60:B9:C0:7E:AC:8B",
"60:B9:C0:7E:9C:EB",
"60:B9:C0:7E:B9:AB"]
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

# for i in mac:
#     daytum.add("Access Points",i.lower(), {"coordinates":{"x":None, "y":None},"mac":i.lower(),"radius":0,"trilat":[]})
# x = daytum.select_field("Access Points","radius","mac")
# print(x)
ref_APs = {}
aps = daytum.get_collection_data("Access Points")
for i in aps:
    ref_APs[i["mac"]] = {"x":i["coordinates"]["x"],"y":i["coordinates"]["y"],"radius":i["radius"]}
from trilateration import trilaterate_actual
trilateratedata = []
for i in data_variant["accessPoints"]:
    try:
        if ref_APs[i["bssid"]]["x"] != None:
            trilateratedata.append(i)
    except:
        pass
from trilateration import signal_to_distance
filtereddata = []
for i in trilateratedata:
    print("hi")
    print(ref_APs[i["bssid"]]["radius"])
    if ref_APs[i["bssid"]]["radius"] <= 5:
        filtereddata.append(i)
if len(filtereddata)<3:
    x = trilateratedata
    x.sort(key=lambda accessPoint: signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"]))
    filtereddata = x[:5] if len(x) > 5 else x
result, meta = trilaterate_actual({"accessPoints":filtereddata}, ref_APs)
print(result)