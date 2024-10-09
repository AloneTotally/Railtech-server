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
all_coordinates = daytum.select_field("Users","current_coordinates")
print(all_coordinates)