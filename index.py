from flask import Flask, jsonify, render_template_string, request, render_template
from flask_socketio import SocketIO
import random
import os
import time

template_folder = template_folder=os.path.join(os.path.dirname(__file__), 'templates')
# The path name is because to change the path name
app = Flask(__name__, template_folder=template_folder)
# Enable CORS for all routes
socketio = SocketIO(app)

# Define a User class to hold each user's name and coordinates
class User:
    def __init__(self, name):
        self.name = name
        self.current_coordinates = {"x": random.randint(0, 100), "y": random.randint(0, 100)}
        self.previous_coordinates = {"x": None, "y": None}
        self.wifi_scan_data = None  # Store WiFi scan data
        self.accelerator_data = None  # Store Accelerator data

# Create a dictionary to hold all users
users = {
    "Alice": User("Alice"),
    "Bob": User("Bob"),
    "Charlie": User("Charlie"),
}

@app.route('/')
def index():
    """Render the main page with real-time updates."""
    return render_template("index.html")

wifi_scan_requests = []

@app.route('/wifiscan')
def wifiscan():
    """Render the WiFi scan page with a black background and display all requests."""
    return render_template('wifiscan.html')

@app.route('/accelerator')
def accelerator():
    """Render the accelerator page."""
    return render_template('accelerator.html')


# Route to handle POST requests for WiFi scan data
wifi_scan_requests = []

@app.route('/update_wifi_scan', methods=['POST'])
def update_wifi_scan():
    """Handle POST requests from Postman and store all data."""
    global wifi_scan_requests
    data = request.json  # Get the JSON data from the POST request

    # Add the new data to the list of all requests
    wifi_scan_requests.append(data)
    
    # Emit the updated list to all clients
    socketio.emit('update_wifi_scan', wifi_scan_requests)
    
    # Return a success response
    return jsonify({"status": "WiFi scan data updated successfully"}), 200


# Route to handle POST requests for Accelerator data
@app.route('/update_accelerator', methods=['POST'])
def update_accelerator():
    data = request.json
    for user_name, acc_data in data.items():
        if user_name in users:
            users[user_name].accelerator_data = acc_data  # Store the Accelerator data for the user
    # Emit the updated Accelerator data to all connected clients
    socketio.emit('update_accelerator', {user.name: user.accelerator_data for user in users.values()})
    return jsonify({"status": "Accelerator data updated successfully"}), 200


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

@app.route('/update-coordinate', methods=['POST'])
def post_coordinates():
    """Function to update the coordinate of the user specified by the api."""
    data = request.json
    # TODO: Put trilateration portion here
    
    all_coordinates = {}  # Dictionary to hold coordinates for all users
    
    print("Updated Coordinates:", all_coordinates)  # Print all coordinates at once
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