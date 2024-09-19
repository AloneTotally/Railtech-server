from flask import Flask, jsonify, render_template_string
from flask_socketio import SocketIO
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Define a User class to hold each user's name and coordinates
class User:
    def __init__(self, name):
        self.name = name
        self.current_coordinates = {"x": random.randint(0, 100), "y": random.randint(0, 100)}
        self.previous_coordinates = {"x": None, "y": None}
        self.random_value = random.randint(1, 100)  # New random value for each user

def fetch_new_coordinates(user):
    """Simulate fetching new coordinates for a user."""
    return {
        "x": random.randint(0, 100),
        "y": random.randint(0, 100)
    }

def update_coordinates():
    """Function to update the coordinates of each user every 5 seconds."""
    global users
    while True:
        time.sleep(5)  # Wait for 5 seconds
        all_coordinates = {}  # Dictionary to hold coordinates for all users
        for user in users.values():
            user.previous_coordinates = user.current_coordinates.copy()  # Store previous
            new_coords = fetch_new_coordinates(user)  # Get new coordinates
            user.current_coordinates = new_coords  # Update current coordinates
            all_coordinates[user.name] = user.current_coordinates  # Store in dictionary
        
        print("Updated Coordinates:", all_coordinates)  # Print all coordinates at once
        # Emit the updated coordinates to all connected clients
        socketio.emit('update_coordinates', all_coordinates)

# Create a dictionary to hold all users
users = {
    "Alice": User("Alice"),
    "Bob": User("Bob"),
    "Charlie": User("Charlie"),
}

@app.route('/')
def index():
    """Render the main page with real-time updates."""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Real-Time Coordinates</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    </head>
    <body>
        <h1>Real-Time User Coordinates</h1>
        <div id="coordinates"></div>
        <h1><a href="/wifiscan">Go to WiFi Scan</a></h1>
        <h1><a href="/accelerator">Go to Accelerator</a></h1>
        <script>
            const socket = io();

            socket.on('update_coordinates', function(data) {
                const coordinatesDiv = document.getElementById('coordinates');
                coordinatesDiv.innerHTML = ''; // Clear the previous content
                for (const [name, coords] of Object.entries(data)) {
                    coordinatesDiv.innerHTML += `<p>${name}: Current X: ${coords.x}, Current Y: ${coords.y}</p>`;
                }
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/wifiscan')
def wifiscan():
    """Render the WiFi scan page."""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WiFi Scan</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    </head>
    <body>
        <h1>WiFi Scan Results</h1>
        <div id="wifi-scans">Loading...</div>
        <h1><a href="/">Go back to Coordinates</a></h1>

        <script>
            const socket = io();

            socket.on('update_random_values', function(data) {
                const wifiDiv = document.getElementById('wifi-scans');
                wifiDiv.innerHTML = ''; // Clear previous results
                for (const [name, value] of Object.entries(data)) {
                    wifiDiv.innerHTML += `<p>${name}: Random Value: ${value}</p>`;
                }
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/accelerator')
def accelerator():
    """Render the accelerator page."""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Accelerator</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    </head>
    <body>
        <h1>Accelerator Results</h1>
        <div id="accelerator-results">Loading...</div>
        <h1><a href="/">Go back to Coordinates</a></h1>

        <script>
            const socket = io();

            socket.on('update_accelerator_values', function(data) {
                const acceleratorDiv = document.getElementById('accelerator-results');
                acceleratorDiv.innerHTML = ''; // Clear previous results
                for (const [name, value] of Object.entries(data)) {
                    acceleratorDiv.innerHTML += `<p>${name}: Random Value: ${value}</p>`;
                }
            });
        </script>
    </body>
    </html>
    ''')

def update_random_values():
    """Function to update random values for each user every 5 seconds."""
    global users
    while True:
        time.sleep(5)  # Wait for 5 seconds
        random_values = {}  # Dictionary to hold random values for all users
        for user in users.values():
            user.random_value = random.randint(1, 100)  # Update the random value
            random_values[user.name] = user.random_value  # Store in dictionary
        
        print("Updated Random Values:", random_values)  # Print all random values at once
        # Emit the updated random values to all connected clients
        socketio.emit('update_random_values', random_values)

def update_accelerator_values():
    """Function to update accelerator values for each user every 5 seconds."""
    global users
    while True:
        time.sleep(5)  # Wait for 5 seconds
        accelerator_values = {}  # Dictionary to hold accelerator values for all users
        for user in users.values():
            accelerator_value = random.randint(1, 100)  # Generate a random value
            accelerator_values[user.name] = accelerator_value  # Store in dictionary
        
        print("Updated Accelerator Values:", accelerator_values)  # Print all accelerator values at once
        # Emit the updated accelerator values to all connected clients
        socketio.emit('update_accelerator_values', accelerator_values)

# Start background threads for updating coordinates, random values, and accelerator values
threading.Thread(target=update_coordinates, daemon=True).start()
threading.Thread(target=update_random_values, daemon=True).start()
threading.Thread(target=update_accelerator_values, daemon=True).start()

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
    socketio.run(app, debug=True)
