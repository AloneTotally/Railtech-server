from flask import Flask, jsonify, render_template_string
from flask_socketio import SocketIO
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

class User:
    def __init__(self, name):
        self.name = name
        self.current_coordinates = {"x": random.randint(0, 100), "y": random.randint(0, 100)}
        self.previous_coordinates = {"x": None, "y": None}

def fetch_new_coordinates(user):
    return {
        "x": random.randint(0, 100),
        "y": random.randint(0, 100)
    }

def update_coordinates():
    global users
    while True:
        time.sleep(5)
        for user in users.values():
            user.previous_coordinates = user.current_coordinates.copy()
            new_coords = fetch_new_coordinates(user)
            user.current_coordinates = new_coords
            print(f"Updated {user.name}: {user.current_coordinates}")
            socketio.emit('update_coordinates', {user.name: user.current_coordinates})

users = {
    "Alice": User("Alice"),
    "Bob": User("Bob"),
    "Charlie": User("Charlie"),
}

threading.Thread(target=update_coordinates, daemon=True).start()

@app.route('/')
def index():
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

        <script>
            const socket = io();

            socket.on('update_coordinates', function(data) {
                const coordinatesDiv = document.getElementById('coordinates');
                coordinatesDiv.innerHTML = '';
                for (const [name, coords] of Object.entries(data)) {
                    coordinatesDiv.innerHTML += `<p>${name}: Current X: ${coords.x}, Current Y: ${coords.y}</p>`;
                }
            });
        </script>
    </body>
    </html>
    ''')

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@app.route('/coordinates', methods=['GET'])
def get_coordinates():
    return jsonify({
        user.name: {
            "current": user.current_coordinates,
            "previous": user.previous_coordinates
        } for user in users.values()
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)
