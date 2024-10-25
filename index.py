from flask import Flask, jsonify, render_template_string, request, render_template
from flask_socketio import SocketIO
import random
import os
import time
import matplotlib
import database_methods as daytum
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
        "rectLeftX": 20,
        "rectBottomY": -4,
        "rectWidth": 10,
        "rectHeight": 8
    },
    "Workzone B": {
        "rectLeftX": 10,
        "rectBottomY": -4,
        "rectWidth": 2,
        "rectHeight": 1
    },
    "Workzone C": {
        "rectLeftX": 30,
        "rectBottomY": -4,
        "rectWidth": 14,
        "rectHeight": 8
    },
    "Workzone D": {
        "rectLeftX": 0,
        "rectBottomY": -4,
        "rectWidth": 1,
        "rectHeight": 4
    },
    "Workzone E": {
        "rectLeftX": 0,
        "rectBottomY": 0,
        "rectWidth": 1,
        "rectHeight": 4
    },
    "Workzone F": {
        "rectLeftX": 3,
        "rectBottomY": 0,
        "rectWidth": 4,
        "rectHeight": 4
    },
}




@app.route('/')
def index():
    """Render the main page with real-time updates."""
    global workzones

    
    def inrect(rect, point) -> bool:
        # Extract rectangle properties
        rect_left_x = rect['rectLeftX']
        rect_bottom_y = rect['rectBottomY']
        rect_width = rect['rectWidth']
        rect_height = rect['rectHeight']
        
        # Calculate the boundaries of the rectangle
        rect_right_x = rect_left_x + rect_width
        rect_top_y = rect_bottom_y + rect_height
        
        # Extract point coordinates
        x = point['current_coordinates']['x']
        y = point['current_coordinates']['y']
        
        # Check if the point is within the rectangle
        if rect_left_x <= x <= rect_right_x and rect_bottom_y <= y <= rect_top_y:
            return True
        else:
            return False

    def users_in_workzones(workzones, users):
        in_workzones = {
            # workzone name: user name
        } # returned value (the number of workzones)
        for user in users: # Loop thru user

            user_in_workzone = False  # Flag to check if user is inside any workzone

            for workzone_name, workzone_rect in workzones.items():  # Loop through workzones
                if inrect(workzone_rect, user):  # Check if user is in the workzone
                    user_in_workzone = True
                    
                    # Initialize the list if the workzone is not already in the dictionary
                    if workzone_name not in in_workzones:
                        in_workzones[workzone_name] = []
                    
                    # Append the user name if not already in the list (to avoid duplicates)
                    if user.get('name') not in in_workzones[workzone_name]:
                        in_workzones[workzone_name].append(user.get('name'))

            # If the user wasn't found in any workzone, add them to "No workzone"
            if not user_in_workzone:
                if 'No workzone' not in in_workzones:
                    in_workzones['No workzone'] = []
                if user.get('name') not in in_workzones['No workzone']:
                    in_workzones['No workzone'].append(user.get('name'))
        return in_workzones


    users = [
        {
            "name": "Alice Johnson",
            "current_coordinates": {"x": 26, "y": 1.4},
            "tracking": True,
            "job": "Track Inspector",
            "email": "alice.johnson@example.com"
        },
        {
            "name": "Bob Smith",
            "current_coordinates": {"x": 24, "y": 1.3},
            "tracking": False,
            "job": "Maintenance Worker",
            "email": "bob.smith@example.com"
        },
        {
            "name": "Charlie Davis",
            "current_coordinates": {"x": 12.7, "y": -1.9},
            "tracking": True,
            "job": "Construction Foreman",
            "email": "charlie.davis@example.com"
        },
        {
            "name": "Dana Lee",
            "current_coordinates": {"x": 9.2, "y": 3},
            "tracking": True,
            "job": "Safety Officer",
            "email": "dana.lee@example.com"
        },
        {
            "name": "Evan Brown",
            "current_coordinates": {"x": 14.1, "y": -3},
            "tracking": False,
            "job": "Signal Technician",
            "email": "evan.brown@example.com"
        }
    ]
    
    data = {
        "users": users,
        "workzones": workzones,
        "inWorkzones": users_in_workzones(workzones, users)
    }



    return render_template("index.html", data=data)

@app.route('/qrcode-gen')
def qrcode():
    data = [
        {
            "id": 'SBST123456789A'
        },
        {
            "id": 'SBST123456789A'
        },
        {
            "id": 'SBST123456789A'
        }
    ]
    return render_template('railtech-qr.html', data=data)

@app.route('/employees')
def employees():
    """Render the employees page."""
    workers = [
        {
            "name": "Alice Johnson",
            "current_coordinates": {"x": 10.5, "y": 20.3},
            "tracking": True,
            "job": "Track Inspector",
            "email": "alice.johnson@example.com"
        },
        {
            "name": "Bob Smith",
            "current_coordinates": {"x": 15.0, "y": 25.6},
            "tracking": False,
            "job": "Maintenance Worker",
            "email": "bob.smith@example.com"
        },
        {
            "name": "Charlie Davis",
            "current_coordinates": {"x": 12.7, "y": 18.9},
            "tracking": True,
            "job": "Construction Foreman",
            "email": "charlie.davis@example.com"
        },
        {
            "name": "Dana Lee",
            "current_coordinates": {"x": 9.2, "y": 22.5},
            "tracking": True,
            "job": "Safety Officer",
            "email": "dana.lee@example.com"
        },
        {
            "name": "Evan Brown",
            "current_coordinates": {"x": 14.1, "y": 19.0},
            "tracking": False,
            "job": "Signal Technician",
            "email": "evan.brown@example.com"
        }
    ]


    return render_template("employees.html",  data=workers)

@app.route('/no-food-for-dayan')
def no_food_for_dayan():
    """Render an example page."""
    return render_template("railtech-web.html")


@app.route('/home')
def home_page():
    data = {
            "listItems": [
                {
                    "title": 'Maintanence between Bukit Panjang and Cashew',
                    "type": 'TAR',
                    "id": 'SBST123456789A',
                    "status": 'Ongoing',
                },
                {
                    "title": 'Not Maintanence between Bukit Panjang and Cashew',
                    "type": 'EWR',
                    "id": 'SBST123456789A',
                    "status": 'Not Started',
                },
                {
                    "title": 'Testing Maintanence between Bukit Panjang and Cashew',
                    "type": 'TAR',
                    "id": 'SBST123456789A',
                    "status": 'Finished',
                }
            ]
        }
    """Render the main page."""
    return render_template("view-tars.html", data=data)

@app.route('/view-tar')
def view_tar():
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


   

    item = {
        "title": 'Maintenance between Bukit Panjang and Cashew',
        "type": 'TAR',
        "id": 'SBST123456789A',
        "status": 'Ongoing',
    }

    data = {
        "item": item,
        "activities": activities
    }
    return render_template("view-tar.html", data=data)

wifi_scan_requests = []

@app.route('/wifiscan')
def wifiscan():
    """Render the WiFi scan page with a black background and display all requests."""
    return render_template('wifiscan.html')

@app.route('/accelerator')
def accelerator():
    """Render the accelerator page."""
    return render_template('accelerator.html')

@app.route('/view_employee')
def view_employee():
    userinfo = {
        "Name": 'Alice Johnson',
        "Age": '20',
        "Email": 'AliceJohnson@gmail.com',
        "Contact number": '91234567',
        'Job Role': 'Train expert'
    }
       
    return render_template("view_employee.html", userinfo=userinfo)


@app.route('/view-checkin')
def checkin():
    """Render the Checkin page."""
    worker = [
        {
            "name": "Alice Johnson",
            "Date": "-",
            "time": "-",
            "status": None,
            "job": "Electrical Engineer"
        },
        {
            "name": "Bob Smith",
            "Date": "-",
            "time": "-",
            "status": None,
            "job": "Project Manager"
        },
        {
            "name": "Charlie Davis",
            "Date": "-",
            "time": "-",
            "status": None,
            "job": "Software Developer"
        },
        {
            "name": "Dana Lee",
            "Date": "-",
            "time": "-",
            "status": None,
            "job": "Data Analyst"
        },
        {
            "name": "Evan Brown",
            "Date": "-",
            "time": "-",
            "status": None,
            "job": "Mechanical Engineer"
        }
    ]

    return render_template("view_checkin.html", data=worker)




# Route to handle POST requests for WiFi scan data
wifi_scan_requests = []

@app.route('/update_wifi_scan', methods=['POST'])
def update_wifi_scan():
    """Handle POST requests from Postman and store all data."""
    global wifi_scan_requests
    data = request.json  # Get the JSON data from the POST request

    # Add the new data to the list of all requests
    
    daytum.add("Users","alonzo",{"name": 1})
    wifi_scan_requests.append(data)
    # Emit the updated list to all clients
    socketio.emit('update_wifi_scan', wifi_scan_requests)
    
    # Return a success response
    return jsonify({"status": "WiFi scan data updated successfully"}), 200


# Route to handle POST requests for Accelerator data
# @app.route('/update_accelerator', methods=['POST'])
# def update_accelerator():
#     data = request.json
#     for user_name, acc_data in data.items():
#         if user_name in users:
#             users[user_name].accelerator_data = acc_data  # Store the Accelerator data for the user
#     # Emit the updated Accelerator data to all connected clients
#     socketio.emit('update_accelerator', {user.name: user.accelerator_data for user in users.values()})
#     return jsonify({"status": "Accelerator data updated successfully"}), 200


# @app.route('/update-coordinates', methods=['POST'])
# def post_coordinates():
#     """Function to update the coordinates of each user every 5 seconds."""
#     global users
#     for _ in range(3):
#         time.sleep(5)
#         all_coordinates = {}  # Dictionary to hold coordinates for all users
#         for user in users.values():
#             user.previous_coordinates = user.current_coordinates.copy()  # Store previous
#             new_coords = {
#                 "x": random.randint(0, 100),
#                 "y": random.randint(0, 100)
#             }  # Get new coordinates
#             user.current_coordinates = new_coords  # Update current coordinates
#             all_coordinates[user.name] = user.current_coordinates  # Store in dictionary
        
#         print("Updated Coordinates:", all_coordinates)  # Print all coordinates at once
#         # Emit the updated coordinates to all connected clients
#         socketio.emit('update_coordinates', all_coordinates)
#     return jsonify({"status": "Trilateration data updated successfully"}), 200

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
    
    # user checked in
    if data["checkIn"]:
        # Probably should include the session ID in here which is tied to QR code? im not so sure
        socketio.emit(f'checkInData-{data["sessionID"]}', data)
    # user checked out
    else:
        socketio.emit(f'checkOutData-{data["sessionID"]}', data)

    return jsonify({"status": "Check in data updated successfully"}), 200


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
        ref_APs[i["mac"]] = i["coordinates"]
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
    print(trilateratedata)
    result, meta = trilaterate_actual({"accessPoints":trilateratedata}, ref_APs)

    # TODO: Implement ekf here plsplsplspls
    new_coords = {'x': result.center.x, 'y': result.center.y}

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
        daytum.update_field("Users",user_name,"previous_coordinates",user["current_coordinates"])
        daytum.update_field("Users",user_name,"current_coordinates",new_coords)
        daytum.update_field("Users",user_name,"rssi",data["accessPoints"])
        user = daytum.get_document("Users",user_name)
        
    else:
        # TODO: Darius urm try not to change the schema of a variable instead create a new variable (u previously named it data)
        user_data = {"current_coordinates": new_coords,"previous_coordinates":{"x":None,"y":None},"tracking":True,"rssi":data["accessPoints"],"name":user_name}
        daytum.add("Users",user_name, user_data)
        users = daytum.get_collection_names("Users")
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
    
    # TODO: note that memo and insufficient_circles are to be replaced by
    # TODO: db as they are meant to be constantly changing
    from trilateration import find_new_APs
    find_new_APs(data, (new_coords["x"], new_coords["y"]),db)
    
    # TODO: store the location of the new APs using the trilateration.memo global var
    # TODO: update the APs on the map or smt
    # all_coordinates = {u.name: u.current_coordinates for u in users.values()}
    
    global workzones

    all_coordinates = {
        "Users": daytum.select_field("Users","current_coordinates","name"),
        "APs": daytum.select_field("Access Points","coordinates","mac"),
        "workzones": workzones
    }
    
    print("Updated Coordinates:", all_coordinates)  # Print all coordinates
    
    # Emit the updated coordinates to all connected clients
    socketio.emit('update_coordinates', all_coordinates)
    return jsonify({"status": "Trilateration data updated successfully"}), 200


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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)