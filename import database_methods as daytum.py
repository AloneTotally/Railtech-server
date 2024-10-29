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
    "accessPoints": [
        {
            "mac": "0a:0b:a7:68:7a:02",
            "frequency": 2412,  # 2.4 GHz frequency
            "signalStrength": -50  # Signal strength in dBm
        },
        {
            "mac": "60:b9:c0:97:c6:ac",
            "frequency": 5180,  # 5 GHz frequency
            "signalStrength": -70
        },
        {
            "mac": "9a:59:7a:97:1c:65",
            "frequency": 2412,
            "signalStrength": -60
        },
        {
            "mac": "wow",
            "frequency": 2412,
            "signalStrength": -20
        }
    ]
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
#     if i not in mac:
#         print("delete")
#         daytum.delete("Access Points",i)

for i in mac:
    daytum.add("Access Points",i.lower(), {"coordinates":{"x":None, "y":None},"mac":i.lower(),"radius":0,"trilat":[]})