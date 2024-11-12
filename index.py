from flask import Flask, jsonify, render_template_string, request, render_template
from flask_socketio import SocketIO
import random
import os
import time
import matplotlib
from matplotlib import pyplot as plt
import database_methods as daytum
plt.close('all')
matplotlib.use('Agg')
db = daytum.setup()

template_folder = template_folder=os.path.join(os.path.dirname(__file__), 'templates')
# The path name is because to change the path name
app = Flask(__name__, template_folder=template_folder)
# Enable CORS for all routes
socketio = SocketIO(app)
# Define a User class to hold each user's name and coordinates
class User:
    def __init__(self, name, current_coordinates={"x": random.randint(0, 100), "y": random.randint(0, 100)}):
        self.name = name
        self.current_coordinates = current_coordinates
        self.previous_coordinates = {"x": None, "y": None}
        self.wifi_scan_data = None  # Store WiFi scan data
        self.accelerator_data = None  # Store Accelerator data

# Create a dictionary to hold all users
users = daytum.get_collection_names("Users")

workzones = {
     "Workzone A": {
        # "name": "Workzone A",
        "rectLeftX": 0,
        "rectBottomY": -15,
        "rectWidth": 7,
        "rectHeight": 30
    },
    "Workzone B": {
        # "name": "Workzone B",
        "rectLeftX": 8,  # Touching Workzone A
        "rectBottomY": -15,
        "rectWidth": 7,
        "rectHeight": 30
    },
    # "Workzone A": {
    #     "rectLeftX": 20,
    #     "rectBottomY": -4,
    #     "rectWidth": 10,
    #     "rectHeight": 8
    # },
    # "Workzone B": {
    #     "rectLeftX": 10,
    #     "rectBottomY": -4,
    #     "rectWidth": 2,
    #     "rectHeight": 1
    # },
    # "Workzone C": {
    #     "rectLeftX": 30,
    #     "rectBottomY": -4,
    #     "rectWidth": 14,
    #     "rectHeight": 8
    # },
    # "Workzone D": {
    #     "rectLeftX": 0,
    #     "rectBottomY": -4,
    #     "rectWidth": 1,
    #     "rectHeight": 4
    # },
    # "Workzone E": {
    #     "rectLeftX": 0,
    #     "rectBottomY": 0,
    #     "rectWidth": 1,
    #     "rectHeight": 4
    # },
    # "Workzone F": {
    #     "rectLeftX": 3,
    #     "rectBottomY": 0,
    #     "rectWidth": 4,
    #     "rectHeight": 4
    # },
}

taa_data = {
    "listItems": [
        {
            "title": 'Maintanence between Bukit Panjang and Cashew',
            "type": 'TAR',
            "id": 'SBST123456789A',
            "status": 'Ongoing',
            "workzones": [
                "Workzone A",
                "Workzone C",
                "Workzone E",
            ],
            "checkins": [
                {
                    "name": "alonzo",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Operations Lead"
                },
                {
                    "name": "Isaac",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Data Analyst"
                },
                {
                    "name": "Venti",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "UX Designer"
                },
                {
                    "name": "Darius",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Software Engineer"
                },
                {
                    "name": "Nash",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Quality Assurance"
                }
            ]
            ,
            "activitylog":[]
        },
        {
            "title": 'Not Maintanence between Bukit Panjang and Cashew',
            "type": 'EWR',
            "id": 'SMRT123456789A',
            "status": 'Not Started',
            "workzones": [
                "Workzone B",
                "Workzone D",
                "Workzone E",
            ],
            "checkins": [
                {
                    "name": "alonzo",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Operations Lead",
                },
                {
                    "name": "Isaac",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Data Analyst"
                },
                {
                    "name": "Venti",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "UX Designer"
                },

            ]
            ,
            "activitylog":[]
        },
        {
            "title": 'Testing Maintanence between Bukit Panjang and Cashew',
            "type": 'TAR',
            "id": 'SBST987654321A',
            "status": 'Finished',
            "workzones": [
                "Workzone A",
                "Workzone B",
                "Workzone C",
                "Workzone D",
                "Workzone E",
            ],
            "checkins": [
                {
                    "name": "jane",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Marketing Specialist"
                },
                {
                    "name": "Isaac",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Data Analyst"
                },
                {
                    "name": "Nash",
                    "Date": "-",
                    "time": "-",
                    "status": None,
                    "job": "Quality Assurance"
                }
            ]
            ,
            "activitylog":[]
        }
    ]
}

def find_taa_from_id(taa_id):
    for taa in taa_data["listItems"]:
        if taa["id"] == taa_id:
            return taa

def create_default_mapdata():
    global workzones
    global employee_names

    user_info = employee_names

    # user_locations = {
    #     "Alice Johnson": {"x": 26, "y": 0},
    #     "Bob Smith": {"x": 14, "y": 1.3},
    #     "Charlie Davis": {"x": 12.7, "y": -1.9},
    #     "Dana Lee": {"x": 9.2, "y": 3},
    #     "Evan Brown": {"x": 14.1, "y": -3}
    # }

    user_locations = {
        "Alonzo": {"x": 10, "y": 5},
        "Darius": {"x": 12, "y": -3.5},
        "Isaac": {"x": 8, "y": 2.1},
        "Nash": {"x": 15, "y": -1.2},
        "Venti": {"x": 20, "y": 4.4},
        "alonzo": {"x": 18, "y": 0.7},
        "jane": {"x": 11, "y": -4.3}
    }

    # users_info_test = []
    # for (name, coords) in user_locations.items():
    #     # print(name)
    #     userinfo = {
    #         "name": name,
    #         "current_coordinates": coords,
    #         "tracking": False,
    #         "job": "Signal Technician",
    #         "email": "evan.brown@example.com",
    #     }

    #     print(userinfo)
    #     users_info_test.append(userinfo)
    # # USERRRRRRSSSS=  {'Alonzo': {'y': -0.4879266504588531, 'x': 14.750897467714106}, 'Darius': {'y': 0, 'x': 0}, 'Isaac': {'y': 0, 'x': 0}, 'Nash': {'y': 0, 'x': 0}, 'Venti': {'y': 0, 'x': 0}, 'alonzo': {'y': 0.0, 'radius': 0.0, 'x': 0.0}, 'jane': {'y': -2.718541429794193, 'x': 1.3993322251110163}}
    # print("Users_info_test", users_info_test)

    global index_mapdata
    index_mapdata = {
        "Users": user_locations,
        "workzones": workzones,
        # MIGHT COMMENT OUT BECAUSE OF THE ACTUAL DATA BEING DIFF
        "inWorkzones": users_in_workzones(workzones, user_locations),
        "correctWorkzone": ["Workzone B"],
        "userInfo": user_info
    }

# !#############################################################! #
# !##   Route handlers below, miscellaneous functions above   ##! #
# !#############################################################! #

@app.route('/')
def index():
    """Render the main page with real-time updates."""
    
    # ! index_mapdata is defined at the bottom of this doc, not above this 
    # ! function as the above default function stuff relies on another function 
    # ! that is alot lower down in this file

    # return render_template("index.html")
    return render_template("index.html", data=index_mapdata)

@app.route('/<string:taa_id>/qrcode-gen')
def qrcode(taa_id):
    
    taa = find_taa_from_id(taa_id)
    return render_template('railtech-qr.html', data=taa["id"])


@app.route('/home')
def home_page():
    
    """Render the main page."""
    return render_template("view-tars.html", data=taa_data)


@app.route('/<string:taa_id>')
def view_tar(taa_id):
    # changing of data format to the below condensed format
    # can be handled on in this function instead

    # TODO: handle the processing of the activity log (previously an arr) and 
    # TODO: convert to a clustered array or smt


    # Each document just prob has like the info of what happened
    # (only sent if got change in workzone)
    # activities = []
    #find_taa_from_id(taa_id)["activitylog"]
    activities = [
        {
            "title": "Checked in - Workzone A",
            "timestamp": "1:30 AM",
            "alert": False,
            "origin": None,
            "note": "",
            "target": "checked in",
            "details": [
                {
                    "name": "Alonzo",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-1.jpg",
                    "timestamp": "1:30 AM"
                },
                {
                    "name": "Darius",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-2.jpg",
                    "timestamp": "1:30 AM"
                },
                {
                    "name": "Isaac",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-4.jpg",
                    "timestamp": "1:30 AM"
                },
                {
                    "name": "Venti",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-4.jpg",
                    "timestamp": "1:30 AM"
                }
            ]
        },
        {
            "title": "Workzone A - Workzone B",
            "timestamp": "1:30 AM",
            "alert": False,
            "origin": "Workzone A",
            "target": "Workzone B",
            "note": "Alonzo, Isaac, Darius",
            "details": [
                {
                    "name": "Alonzo",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-1.jpg",
                    "timestamp": "1:30 AM"
                },
                {
                    "name": "Isaac",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-2.jpg",
                    "timestamp": "1:30 AM"
                },
                {
                    "name": "Darius",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-4.jpg",
                    "timestamp": "1:30 AM"
                }
            ]
        },
        {
            "title": "Workzone B - Workzone C",
            "timestamp": "1:30 AM",
            "alert": True,
            "origin": "Workzone B",
            "target": "Workzone C",
            "note": "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Qui, provident!",
            "details": [
                {
                    "name": "Alonzo",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-1.jpg",
                    "timestamp": "1:30 AM"
                }
            ]
        },
        {
            "title": "Workzone B - Workzone D",
            "timestamp": "2:00 AM",
            "alert": False,
            "origin": "Workzone B",
            "target": "Workzone D",
            "note": "Alonzo, Isaac",
            "details": [
                {
                    "name": "Alonzo",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-3.jpg",
                    "timestamp": "2:00 AM"
                },
                {
                    "name": "Isaac",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-5.jpg",
                    "timestamp": "2:00 AM"
                }
            ]
        },
        {
            "title": "Workzone D - Workzone E",
            "timestamp": "2:30 AM",
            "alert": True,
            "origin": "Workzone D",
            "target": "Workzone E",
            "note": "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Nulla, modi!",
            "details": [
                {
                    "name": "Isaac",
                    "profile_image": "https://flowbite.com/docs/images/people/profile-picture-5.jpg",
                    "timestamp": "2:30 AM"
                }
            ]
        }
    ]

    item = find_taa_from_id(taa_id)


    data = {
        "item": item,
        "activities": activities
    }
    return render_template("view-tar.html", data=data)

# ! employee_names variable is located at the bottom

@app.route('/employees')
def employees():
    """Render the employees page."""


    return render_template("employees.html",  data=employee_names)


@app.route('/employees/<string:employee_name>')
def view_employee_updated(employee_name):

    for element in employee_names:
        if element["name"] == employee_name:
            element = {key.replace('_', ' ').capitalize(): value for key, value in element.items()}
            return render_template("view_employee.html", userinfo=element)

@app.route('/<string:taa_id>/view-checkin')
def checkin(taa_id):
    """Render the Checkin page."""

    item = find_taa_from_id(taa_id)

    # return render_template("view_checkin.html", data=worker)
    return render_template("view_checkin.html", data=item)

@app.route('/check-in', methods=['POST'])
def post_checkin():
    """
    data class CheckInObject(
        val user: String,
        val checkIn: Boolean,
        val sessionID: String
    )
    """
    data = request.json
    print("CHECK IN DATA RECEIVED :DDDDD", data)
    
    taa = find_taa_from_id(data["sessionID"])
    print(taa)
    worker = taa["checkins"]

    username = data['user']
    # Find the index of the item with the matching name
    i = next((index for index, item in enumerate(worker) if item['name'] == username), None)

    from datetime import datetime
    current_date = datetime.now()
    date_string = current_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as 'YYYY-MM-DD HH:MM:SS'
    
    # Split date and time
    date, time = date_string.split(' ')

    # user checked in
    if data["checkIn"]:

        if i is not None:
            
            # Update the item's properties
            worker[i]['time'] = time
            worker[i]['Date'] = date
            worker[i]['status'] = True
            update = {
            "title": "Checked in",
            "timestamp": time,
            "alert": False,
            "origin": None,
            "note": "",
            "target": "checked in",
            "details":[{"name": username}]
            }
            taa["activitylog"].append(update)
        else:
            print(f"User '{username}' not found in data.")

        # Probably should include the session ID in here which is tied to QR code? im not so sure
        socketio.emit(f'checkInData-{data["sessionID"]}', data)
    # user checked out
    else:
        update = {
            "title": "Checked Out",
            "timestamp": time,
            "alert": False,
            "origin": None,
            "note": "",
            "target": "checked Out",
            "details":[{"name": username}]
        }

        taa["activitylog"].append(update)
        worker[i]['status'] = False
        socketio.emit(f'checkOutData-{data["sessionID"]}', data)
    print(taa["activitylog"])
    return jsonify({"status": "Check in data updated successfully"}), 200

user_position = []

@app.route('/user-location')
def user_location():
    global user_position
    return jsonify({"user_position": user_position}), 200

@app.route('/update-user-location')
def update_userpos():
    global user_position
    user_position.append("hehehhehhehehe")
    return jsonify({"status": "User position updated successfully"}), 200



def inrect(rect, point) -> bool:
    # Extract rectangle properties
    rect_left_x = rect['rectLeftX']
    rect_bottom_y = rect['rectBottomY']
    rect_width = rect['rectWidth']
    rect_height = rect['rectHeight']
    
    # Calculate the boundaries of the rectangle
    rect_right_x = rect_left_x + rect_width
    rect_top_y = rect_bottom_y + rect_height
    
    print("point", point)
    # print("point['current_coordinates']", point['current_coordinates'])
    # print("point['current_coordinates']['x']", point['current_coordinates']['x'])
    # Extract point coordinates
    x = point['x']
    y = point['y']
    
    # Check if the point is within the rectangle
    if rect_left_x <= x <= rect_right_x and rect_bottom_y <= y <= rect_top_y:
        return True
    else:
        return False

def users_in_workzones(workzones, users):
    in_workzones = {
        # workzone name: user name
    } # returned value (the number of workzones)
    print("USERRRRRRSSSS: ", users)
    for [user, coords] in users.items(): # Loop thru user
        print(f"Current user atm: {user} with coords {coords}")
        user_in_workzone = False  # Flag to check if user is inside any workzone

        for workzone_name, workzone_rect in workzones.items():  # Loop through workzones
            if inrect(workzone_rect, coords):  # Check if user is in the workzone
                user_in_workzone = True
                
                # Initialize the list if the workzone is not already in the dictionary
                if workzone_name not in in_workzones:
                    in_workzones[workzone_name] = []
                
                # Append the user name if not already in the list (to avoid duplicates)
                if user not in in_workzones[workzone_name]:
                    in_workzones[workzone_name].append(user)

        # If the user wasn't found in any workzone, add them to "No workzone"
        if not user_in_workzone:
            if 'No workzone' not in in_workzones:
                in_workzones['No workzone'] = []
            if user not in in_workzones['No workzone']:
                in_workzones['No workzone'].append(user)
    return in_workzones


@app.route('/update-coordinate', methods=['POST'])
def post_coordinates():
    """Function to update the coordinate of the user specified by the api."""
    global users

    data = request.json
    # TODO: ref_APs variable shld be in a database and should probably be modified to fit schema of memo (find new APs portion)
    # ref_APs = {
    #     'bssid1': (4, 0),
    #     'bssid2': (10, 9),    
    #     'bssid3': (1, 10)
    # } 
    ref_APs = {}
    aps = daytum.get_collection_data("Access Points")
    print(aps)
    for i in aps:
        ref_APs[i["mac"]] = {"x":i["coordinates"]["x"],"y":i["coordinates"]["y"],"radius":i["radius"]}
        print(i["coordinates"])
    from trilateration import trilaterate_actual
    trilateratedata = []
    for i in data["accessPoints"]:
        print(i)
        try:
            if ref_APs[i["bssid"]]["x"] != None:
                trilateratedata.append(i)
        except:
            pass
    from trilateration import signal_to_distance
    print(trilateratedata)
    filtereddata = []
    for i in trilateratedata:
        print("hi")
        print(ref_APs[i["bssid"]]["radius"])
        if ref_APs[i["bssid"]]["radius"] <= 5:
            filtereddata.append(i)
    print(filtereddata)
    if len(filtereddata)<3:
        x = trilateratedata
        x.sort(key=lambda accessPoint: signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"]))
        filtereddata = x[:3] if len(x) > 3 else x
    print(filtereddata)
        
    result, meta = trilaterate_actual({"accessPoints":filtereddata}, ref_APs)
    new_coords = {'x': result.center.x, 'y': result.center.y,"radius":result.radius}
    # The following two lines replaces the above two lines:
    # from ekf_trilateration import trilaterate_ekf
    # new_coords = trilaterate_ekf({"accessPoints":filtereddata}, ref_APs)


    # note that `data` is a dictionary and not the database reference
    user_name = data.get('user')
    access_points = data.get('accessPoints')
    
    if not user_name or not access_points:
        return jsonify({"error": "Invalid request data"}), 400

    # TODO: this whole part is to be replaced by the database request
    # not sure about the significance of the previous coordinates attribute tho... can be used in ekf maybe???
    # but imma just leave it there for now
    # Update the user's coordinates in the global `users` dictionary
    if user_name in users:
        # user = users[user_name]
        # user.previous_coordinates = user.current_coordinates.copy()  # Store previous
        # user.current_coordinates = new_coords  # Update current coordinates
        user = daytum.get_document("Users",user_name)
        updatingdata = {"previous_coordinates":user["current_coordinates"],"current_coordinates":new_coords,"rssi":data["accessPoints"]}
        daytum.update("Users",user_name,updatingdata)
        users = daytum.get_document("Users",user_name)
        
    else:
        # TODO: Darius urm try not to change the schema of a variable instead create a new variable (u previously named it data)
        user_data = {"current_coordinates": new_coords,"previous_coordinates":{"x":None,"y":None},"tracking":True,"rssi":data["accessPoints"],"name":user_name}
        daytum.add("Users",user_name, user_data)
        users = daytum.get_document("Users",user_name)
        # Create a new user if they don't exist
        # users[user_name] = User(name=user_name, current_coordinates=new_coords)
            # "name": user_name,
            # "current_coordinates": new_coords,
            # "previous_coordinates": None,
    # TODO:
    """
    Things to store in database:
    - currentLocation
    - previousLocation(idk if we really need this anymore)
    - circleData ([
        {
            "x": float,
            "y": float,
            "radius": float
        }
    ])
    - how many times trilaterated
    """ 

    # from trilateration import find_new_APs
    # for i in data["accessPoints"]:
    #     if i["bssid"] == "60:b9:c0:7e:93:8b":
    #         data = {"accessPoints":[i]}
    #         break
    # find_new_APs(data, (new_coords["x"], new_coords["y"]),db) 
    
    # all_coordinates = {u.name: u.current_coordinates for u in users.values()}
    received_users = daytum.select_field("Users","current_coordinates","name")
    received_aps = daytum.select_field("Access Points","coordinates","mac")
    global workzones

    
    all_coordinates = {
        "Users": received_users,
        "APs": received_aps,
        "workzones": workzones,
        "correctWorkzone": ["Workzone B"],
        "inWorkzones": [users_in_workzones(workzones, received_users)],
        "userInfo": employee_names,
    }
    for taa in taa_data["listItems"]:
        breaker = False
        print("hi")
        for activity in taa["activitylog"]:
            if activity["title"] == "Checked in":
                name = activity["details"][0]
                print(name)
                for workzone in all_coordinates["inWorkzones"][0]:
                    for user in all_coordinates["inWorkzones"][0][workzone]:
                        print(user)
                        if user == name:
                            activity["title"] += f" {workzone}"
                            breaker = True
                            break
                    if breaker:
                        break
            if breaker:
                print(activity)
                break
    def find_workzone(workzones,user):
        check = workzones.keys()
        count = 0
        for i in workzones.values():
            for a in i:
                if a == user:
                    return check[count]
            count += 1
        return "error"
    def find_taa_by_name(name):
        for taa in taa_data["listItems"]:
            for taauser in taa["checkins"]:
                if name == taauser["name"]:
                    return taa
        return ValueError()
    
    prev  = users_in_workzones(workzones, {user_name:users["previous_coordinates"]})
    current = users_in_workzones(workzones, {user_name:users["current_coordinates"]})
    if prev!= current:
        origin,target = find_workzone(prev,user_name),find_workzone(current,user_name)
        title = f'Moved from {origin} to {target}'
        try:
            from datetime import datetime
            current_date = datetime.now()
            date_string = current_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as 'YYYY-MM-DD HH:MM:SS'
            # Split date and time
            date, time = date_string.split(' ')
            taa = find_taa_by_name(user_name)
            update = {
            "title": title,
            "timestamp": time,
            "alert": False,
            "origin": origin,
            "note": "",
            "target": target,
            "details":[{"name": user_name}]
            }
            taa["activitylog"].append(update)
            print(taa["activitylog"])
        except:
            print("user is not in any taa")
    global index_mapdata
    import copy

    index_mapdata = copy.deepcopy(all_coordinates)
    import json
    print("All INFO TO SEND TO SOCKET:",json.dumps(all_coordinates))
    print("WORKZONES:",workzones)
    print("RECEIVED USERS:",received_users)
    

    print("Updated Coordinates:", all_coordinates)  # Print all coordinates

    global user_position
    for i in received_users.keys():
        print(i, end="(i), ")
        if i == 'alonzo':
            user_position.append(received_users[i])
            print("UPDATED ALONZOS POSITION IN THE GLOBAL:", user_position, "")

    
    # Emit the updated coordinates to all connected clients
    socketio.emit('update_coordinates', all_coordinates)

    # THIS WAS DONE USING CHATGPT
    workzone_list = [{"label": name, **attributes} for name, attributes in workzones.items()]
    userdata_forphone = [{"name": name, **attributes} for name, attributes in received_users.items()]

    inworkzones = all_coordinates["inWorkzones"][0]
    print("inworkzonesessdfsdgsddgsdf", inworkzones)
    inworkzones_forphone = [{"workzone": name, "people": attributes} for name, attributes in inworkzones.items()]
    
    all_coordinates["workzones"] = workzone_list # Changing the schema to fit with kotlins type annotation
    all_coordinates["Users"] = userdata_forphone # Changing the schema to fit with kotlins type annotation
    all_coordinates["inWorkzones"] = inworkzones_forphone # Changing the schema to fit with kotlins type annotation

    # Changing the schema to fit with the initial render of the website (because i accidentally
    # made it a tuple and i dont want to change all code depending on it so i just put this here)
    index_mapdata["inWorkzones"] = index_mapdata["inWorkzones"][0]

    return jsonify(all_coordinates), 200
    # return jsonify({"status": "Trilateration data updated successfully"}), 200


# Start the background thread for updating coordinates
# threading.Thread(target=update_coordinates, daemon=True).start()

@socketio.on('connect')
def handle_connect():
    """Handle a new client connection."""
    print("Client connected")

@app.route('/coordinates', methods=['GET'])
def get_coordinates():
    """Endpoint to return the current and previous coordinates as JSON."""
    return jsonify({
        user.name: {
            "current": user.current_coordinates,
            "previous": user.previous_coordinates
        } for user in users.values()
    })


# ! SOME GLOBALS DEFINED HERE
index_mapdata = {}
# Ensures that there is some default data before the data is overridden
# (Can be removed ngl)
employee_names = [
    {"name": "Alonzo", "job": "Project Manager", "email": "alonzo.manager@example.com", "contact_number": "+1111111111", "tracking": False},
    {"name": "Darius", "job": "Software Engineer", "email": "darius.dev@example.com", "contact_number": "+2222222222", "tracking": False},
    {"name": "Isaac", "job": "Data Analyst", "email": "isaac.data@example.com", "contact_number": "+3333333333", "tracking": False},
    {"name": "Nash", "job": "Quality Assurance", "email": "nash.qa@example.com", "contact_number": "+4444444444", "tracking": False},
    {"name": "Venti", "job": "UX Designer", "email": "venti.design@example.com", "contact_number": "+5555555555", "tracking": False},
    {"name": "alonzo", "job": "Operations Lead", "email": "alonzo.ops@example.com", "contact_number": "+6666666666", "tracking": False},
    {"name": "jane", "job": "Marketing Specialist", "email": "jane.marketing@example.com", "contact_number": "+7777777777", "tracking": False}
]
create_default_mapdata()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)