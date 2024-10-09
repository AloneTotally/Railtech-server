# Import necessary libraries
from ast import arg  # For argument handling (though not used in this code)
import numpy as np  # For numerical operations with arrays and matrices
import matplotlib.pyplot as plt  # For plotting graphs
import time  # For performance measurement (timing code execution)
from easy_trilateration.model import *  # For defining circles and points for trilateration
from easy_trilateration.least_squares import easy_least_squares, solve_history  # For trilateration calculation using least squares
from easy_trilateration.graph import *  # For graphing the trilateration result
from math import log10  # For logarithmic operations

# Free-Space Path Loss constant (used for signal-to-distance conversion)
FSPL = 27.55  # Approximate constant for home routers and access points in dBm

# Class definition for Extended Kalman Filter (EKF)
class EKF:
    def __init__(self, dt, state_dim, meas_dim, F, H, Q, R, x0, P0):
        # Initialize EKF parameters
        self.dt = dt  # Time step
        self.state_dim = state_dim  # Dimension of the state (position, velocity)
        self.meas_dim = meas_dim  # Dimension of the measurements (RSSI distance)
        self.F = F  # State transition model (how the state changes over time)
        self.H = H  # Observation model (how we measure the state)
        self.Q = Q  # Process noise covariance (uncertainty in the model)
        self.R = R  # Measurement noise covariance (uncertainty in the measurements)
        self.x = x0  # Initial state estimate (position, velocity)
        self.P = P0  # Initial state covariance (uncertainty in the initial estimate)

    def predict(self):
        # Predict the next state and its covariance
        self.x = np.dot(self.F, self.x)  # State prediction using F matrix
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q  # Covariance prediction

    def update(self, z):
        # Update the state based on the measurement (RSSI)
        y = z - np.dot(self.H, self.x)  # Innovation: difference between measurement and predicted state
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R  # Innovation covariance
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # Kalman gain (how much to trust the measurement)
        self.x = self.x + np.dot(K, y)  # Update the state estimate
        I = np.eye(self.state_dim)  # Identity matrix for dimension matching
        self.P = np.dot((I - np.dot(K, self.H)), self.P)  # Update the covariance estimate

    def get_state(self):
        # Return the current state estimate
        return self.x

# EKF parameters setup
dt = 1.0  # Time step (1 second)
state_dim = 4  # State dimensions: [x, y, vx, vy] (position and velocity in 2D)
meas_dim = 1  # Measurement dimension: RSSI (distance estimate)

# State transition matrix (for constant velocity model)
F = np.array([[1, 0, dt, 0],
              [0, 1, 0, dt],
              [0, 0, 1,  0],
              [0, 0, 0,  1]])

# Jacobian for the observation model, linearizing around the current state
def H_jacobian(x, AP_pos):
    dx = x[0] - AP_pos[0]  # Difference in x-position
    dy = x[1] - AP_pos[1]  # Difference in y-position
    distance = np.sqrt(dx**2 + dy**2)  # Euclidean distance
    H = np.array([[dx / distance, dy / distance, 0, 0]])  # Jacobian matrix for distance measurement
    return H

# Process noise covariance matrix (how much uncertainty in the model)
Q = np.eye(state_dim) * 0.01

# Measurement noise covariance (uncertainty in RSSI measurement)
R = np.array([[1.0]])

# Initial state estimate and covariance
x0 = np.array([0, 0, 0, 0])  # Initial position and velocity (at origin with zero velocity)
P0 = np.eye(state_dim)  # Initial uncertainty (identity matrix)

# Create EKF object with initial parameters
ekf = EKF(dt, state_dim, meas_dim, F, None, Q, R, x0, P0)

# Parameters for signal-to-distance conversion (RSSI model)
dBm = -40  # Transmission power in dBm (negative for power loss)
n = 2.0  # Path loss exponent (environmental factor for signal decay)

# Convert signal strength (RSSI) to distance using Free-Space Path Loss formula
def signal_to_distance(mhz, dbm):
    return 10 ** ((FSPL - (20 * log10(mhz)) + abs(dbm))) / (10 * n)

# Position of the access point (AP)
AP_pos = np.array([10, 10])  # AP located at (10, 10) in a 2D space

# Simulate some RSSI (Received Signal Strength Indicator) measurements
rssis = [-60, -62, -61, -63, -64, -50, -10, -5, -2, -100]  # Example RSSI values from the environment

# Trilateration visualization and formulas (using circles to estimate position)
def trilaterate(arr):
    result, meta = easy_least_squares(arr)  # Perform least-squares trilateration
    create_circle(result, target=True)  # Visualize the estimated position
    print(result)  # Print the result of trilateration (estimated position)
    draw(arr)  # Draw circles and estimated position

# Define four circles representing access points with known positions and distances
arr = [
    Circle(100, 100, 50),  
    Circle(100, 50, 50),  
    Circle(50, 50, 50),  
    Circle(50, 100, 50)
]  

# Print header for output
print("Estimated positions over time:")

# Loop through the simulated RSSI values
for dBm in rssis:
    # Convert RSSI to distance based on signal strength and frequency (5 GHz in this case)
    ghz = 5
    mhz = ghz * 1000
    distance = signal_to_distance(mhz, dBm)
    
    # Perform the prediction step of the EKF (estimate next state)
    ekf.predict()

    # Update the EKF with the new measurement (RSSI-based distance)
    H = H_jacobian(ekf.get_state(), AP_pos)  # Calculate the Jacobian (linearized observation model)
    ekf.H = H  # Set the updated observation model
    ekf.update(np.array([distance]))  # Update the EKF with the new distance measurement

    # Get the estimated state (position and velocity)
    estimated_state = ekf.get_state()
    print(f"Estimated Position: x={estimated_state[0]:.2f}, y={estimated_state[1]:.2f}")  # Print the estimated position

    # Plotting the estimated positions over time
    plt.rcParams["figure.figsize"] = [7.50, 3.50]  # Set figure size for plot
    plt.rcParams["figure.autolayout"] = True  # Enable automatic layout for better spacing

    x = estimated_state[0]  # Extract x-coordinate of the estimated position
    y = estimated_state[1]  # Extract y-coordinate of the estimated position

    plt.plot(x, y, 'r*')  # Plot the estimated position as a red star

plt.show()  # Show 