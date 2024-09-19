from flask import Flask, jsonify
import random
import threading
import time

app = Flask(__name__)

# Define a User class to hold each user's name and coordinates
class User:
    def __init__(self, name):
        self.name = name
        self.current_coordinates = {"x": random.randint(0, 100), "y": random.randint(0, 100)}
        self.previous_coordinates = {"x": None, "y": None}  # Initialize previous coordinates as None

def fetch_new_coordinates(user):
    """Simulate fetching new coordinates for a user."""
    # Replace this with your actual calculation or data fetching logic
    return {
        "x": random.randint(0, 100),
        "y": random.randint(0, 100)
    }

def update_coordinates():
    """Function to update the coordinates of each user every 5 seconds."""
    global users
    while True:
        time.sleep(5)  # Wait for 5 seconds
        for user in users.values():
            # Store current coordinates as previous before updating
            user.previous_coordinates = user.current_coordinates.copy()
            # Fetch new coordinates using the external function
            new_coords = fetch_new_coordinates(user)
            user.current_coordinates = new_coords
            print(f"Updated {user.name}: {user.current_coordinates}")  # Print the updated coordinates

# Create a dictionary to hold all users
users = {
    "Alice": User("Alice"),
    "Bob": User("Bob"),
    "Charlie": User("Charlie"),
}

# Start a background thread to update the coordinates
threading.Thread(target=update_coordinates, daemon=True).start()

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
    app.run(debug=True)
