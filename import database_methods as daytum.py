import database_methods as daytum
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
data = {"coordinates":{"x":4,"y":2},"mac":"ee:b8:5f:33:3d:41"

}

macs = daytum.get_collection_names("Access Points")
print(macs)
for i in macs:
    daytum.update_field("Access Points",i,"radius",5)

