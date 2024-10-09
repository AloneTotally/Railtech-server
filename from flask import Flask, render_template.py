from flask import Flask, render_template_string, jsonify
from flask_socketio import SocketIO
from geopy.distance import geodesic

app = Flask(__name__)
socketio = SocketIO(app)

# Store coordinates and distances for all users
user_data = {}

@app.route('/')
def index():
    """Render the main page with JavaScript to get and update user location."""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Real-Time Coordinates and Distance</title>
    </head>
    <body>
        <h1>Real-Time User Coordinates and Distance</h1>
        <p id="status">Fetching your location...</p>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            const socket = io();

            // Check if the browser supports Geolocation
            if (navigator.geolocation) {
                navigator.geolocation.watchPosition(function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    document.getElementById('status').textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;

                    // Send coordinates to the server via WebSocket
                    socket.emit('send_coordinates', { latitude: latitude, longitude: longitude });
                }, function(error) {
                    document.getElementById('status').textContent = 'Unable to fetch location: ' + error.message;
                });
            } else {
                document.getElementById('status').textContent = 'Geolocation is not supported by this browser.';
            }

            // Listen for updated data (coordinates and distance) from the server
            socket.on('update_coordinates', function(data) {
                document.getElementById('status').innerHTML = '';
                for (const [user, info] of Object.entries(data)) {
                    document.getElementById('status').innerHTML += `<p>${user}: Current Location (Lat: ${info.latitude}, Long: ${info.longitude}) - Distance Traveled: ${info.total_distance.toFixed(2)} meters</p>`;
                }
            });
        </script>
    </body>
    </html>
    ''')

@socketio.on('send_coordinates')
def handle_coordinates(data):
    """Handle incoming coordinates and calculate distance traveled."""
    # Assume all users have a unique session ID (for simplicity, use a timestamp or unique identifier)
    user_id = request.sid  # Use the socket session ID as the user's identifier

    # Get the new coordinates
    new_lat = data['latitude']
    new_lon = data['longitude']
    
    # If the user exists, calculate the distance from the last known position
    if user_id in user_data:
        prev_coords = user_data[user_id]['last_coordinates']
        new_coords = (new_lat, new_lon)
        # Calculate the distance between the last and new coordinates using geopy's geodesic function
        distance_traveled = geodesic(prev_coords, new_coords).meters
        
        # Update the user's total distance traveled
        user_data[user_id]['total_distance'] += distance_traveled
        
        # Update the user's last known coordinates
        user_data[user_id]['last_coordinates'] = new_coords
    else:
        # First time user, initialize their data
        user_data[user_id] = {
            'last_coordinates': (new_lat, new_lon),
            'total_distance': 0.0  # Initial distance is 0
        }

    # Prepare the data to send to the client
    response_data = {
        user_id: {
            'latitude': new_lat,
            'longitude': new_lon,
            'total_distance': user_data[user_id]['total_distance']
        }
    }

    # Broadcast the updated coordinates and distance to all clients
    socketio.emit('update_coordinates', response_data)

@app.route('/coordinates', methods=['GET'])
def get_coordinates():
    """Return all current coordinates and distances traveled."""
    # Format the user data for the API response
    api_response = {
        user_id: {
            "latitude": data['last_coordinates'][0],
            "longitude": data['last_coordinates'][1],
            "total_distance": data['total_distance']
        }
        for user_id, data in user_data.items()
    }
    return jsonify(api_response)

if __name__ == '__main__':
    socketio.run(app, debug=True)
