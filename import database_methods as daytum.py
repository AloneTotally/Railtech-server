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
mac = ["c6:3f:a1:3e:e7:af","c6:37:08:bb:91:a0","a2:02:a5:de:62:96"]
# 60:b9:c0:97:c6:ac is esc np wireless x ap
# 88:d7:f6:a8:b1:7c is esc own router
data = circle(4,3,1)


mac = daytum.get_collection_names("Access Points")
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

# Sample User Location
user_loc = (90, 20)
# pulledcircles = daytum.select_field("Access Points","trilat","mac")
# print(pulledcircles)
find_new_APs(data_variant,user_loc,db)

