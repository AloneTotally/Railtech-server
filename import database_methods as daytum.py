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
x = circle(1,2,3)
all_coordinates = daytum.add("test","test",{"data":classtodict(x)})
print(all_coordinates)
all_coordinates = dicttoclass(daytum.get_field("test","test","data"))
print(all_coordinates.radius)

