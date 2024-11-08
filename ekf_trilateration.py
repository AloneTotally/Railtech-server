# Import necessary libraries
import numpy as np  # For numerical operations with arrays and matrices
import matplotlib.pyplot as plt  # For plotting graphs
from easy_trilateration.model import Circle  # For defining circles and points for trilateration
from easy_trilateration.least_squares import easy_least_squares, solve_history  # For trilateration calculation using least squares
from math import log10  # For logarithmic operations 
from easy_trilateration.graph import *  

# Free-Space Path Loss constant (used for signal-to-distance conversion)
FSPL = 27.55  # Approximate constant for home routers and access points in dBm

# Class definition for Extended Kalman Filter (EKF)
class EKF:
    def __init__(self, dt, state_dim, meas_dim, F, Q, R, x0, P0):
        # Initialize EKF parameters
        self.dt = dt  # Time step
        self.state_dim = state_dim  # Dimension of the state (position, velocity)
        self.meas_dim = meas_dim  # Dimension of the measurements (RSSI distance)
        self.F = F  # State transition model (how the state changes over time)
        self.Q = Q  # Process noise covariance (uncertainty in the model)
        self.R = R  # Measurement noise covariance (uncertainty in the measurements)
        self.x = x0  # Initial state estimate (position, velocity)
        self.P = P0  # Initial state covariance (uncertainty in the initial estimate)

    def predict(self):
        # Predict the next state and its covariance
        self.x = np.dot(self.F, self.x)  # State prediction using F matrix
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q  # Covariance prediction

    def update(self, z, H, R):
        self.R = R
        # Update the state based on the measurement (RSSI)
        y = z - np.dot(H, self.x)[:2]  # Innovation: difference between measurement and predicted state
        S = np.dot(np.dot(H, self.P), H.T) + self.R  # Innovation covariance
        K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))  # Kalman gain (how much to trust the measurement)
        self.x = self.x + np.dot(K, y)  # Update the state estimate
        I = np.eye(self.state_dim)  # Identity matrix for dimension matching
        self.P = np.dot((I - np.dot(K, H)), self.P)  # Update the covariance estimate

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
    if distance == 0:
        distance = 1e-6  # Avoid division by zero by setting a small epsilon value
    H = np.array([[dx / distance, dy / distance, 0, 0],
                    [0, 0, 0, 1]])  # Jacobian matrix for distance measurement
    # H = np.array([[dx / distance, dy / distance, 0, 0],
    #                 [0, 0, 1, 0]])  # Jacobian matrix for distance measurement
    return H

# Process noise covariance matrix (how much uncertainty in the model)
# Q = np.eye(state_dim) * 0.1
Q = np.array([[0.01, 0, 0, 0],
              [0, 0.01, 0, 0],
              [0, 0, 0.001, 0],
              [0, 0, 0, 0.001]])

# Measurement noise covariance (uncertainty in RSSI measurement)
# R = np.array([[5.0]])
R = np.array([[1.0, 0], 
              [0, 1.0]])

# Initial state estimate and covariance
x0 = np.array([0, 0, 0, 0])  # Initial position and velocity (at origin with zero velocity)
# P0 = np.eye(state_dim) * 100  # Initial uncertainty (identity matrix)

# ChatGPTed initial covariance state
P0 = np.diag([2000, 2000, 4, 4])  # Assuming high uncertainty for position and lower uncertainty for velocity

# Create EKF object with initial parameters
ekf = EKF(dt, state_dim, meas_dim, F, Q, R, x0, P0)

# Parameters for signal-to-distance conversion (RSSI model)
dBm = -40  # Transmission power in dBm (negative for power loss)
n = 2.0  # Path loss exponent (environmental factor for signal decay)

# Convert signal strength (RSSI) to distance using Free-Space Path Loss formula
def signal_to_distance(mhz, dbm):
    return 10 ** ((FSPL - (20 * log10(mhz)) + abs(dbm)) / (10 * n))


def trilaterate_ekf(data, ref_APs):
    ekf.predict()  # Predict next state

    arr = []
    # Loop through APs
    for accessPoint in data["accessPoints"]:
        print(accessPoint['bssid'])
        # If bssid of ap is in the ref ap keys
        if accessPoint['bssid'] in list(ref_APs.keys()):
            print(f"hi {accessPoint}")
          
            bssid = accessPoint['bssid']
            coords = ref_APs[bssid]

            distance = signal_to_distance(accessPoint["frequency"], accessPoint["signalStrength"])
            arr.append(Circle(coords["x"], coords["y"], distance))
    print(arr)
    # trilaterate_test(arr)
    try:
        trilaterated_position = easy_least_squares(arr)
        z = np.array([trilaterated_position[0].center.x, trilaterated_position[0].center.y])

        H = H_jacobian(ekf.get_state(), AP_pos)  # Compute Jacobian for the current AP
        # ekf.update(z, H, R = np.array([[5.0]]) )  # Update EKF with distance measurement and Jacobian
        ekf.update(z, H, R = np.array([[trilaterated_position[0].radius]]) )  # Update EKF with distance measurement and Jacobian

        # Get the estimated state (position and velocity)
        estimated_state = ekf.get_state()
        estimated_position = estimated_state[:2]
        new_coords = {'x': estimated_position[0], 'y': estimated_position[1], 'radius': trilaterated_position[0].radius}

        return new_coords
        
        # draw(arr)
    except Exception as e:
        print(f"Trilateration failed for AP {accessPoint['bssid']} due to: {e}")
        return []
    
# Positions of multiple access points (APs)
AP_positions = [
    np.array([0, 0]),    # AP at (0, 0)
    np.array([10, 0]),   # AP at (10, 0)
    np.array([5, 10])    # AP at (5, 10)
]

# Simulate some RSSI (Received Signal Strength Indicator) measurements for each AP
rssis_per_ap = [
    [-60, -62, -61, -63, -64, -50, -10, -5, -2, -100],  # AP 1 RSSIs
    [-55, -57, -59, -61, -60, -45, -15, -8, -3, -90],   # AP 2 RSSIs
    [-70, -65, -63, -67, -66, -55, -30, -25, -15, -95]  # AP 3 RSSIs
]

# Print header for output
print("Estimated positions over time:")


figure, axis = plt.subplots(2, 2)

# Loop through the simulated RSSI values for all APs
for time_step in range(len(rssis_per_ap[0])):  # Assuming equal length for all AP RSSIs
    ekf.predict()  # Predict next state

    distances = []
    # For each AP, use its RSSI at the current time step
    for i, AP_pos in enumerate(AP_positions):   
        dBm = rssis_per_ap[i][time_step]  # Get RSSI value from the i-th AP at current time step
        ghz = 5
        mhz = ghz * 1000
        distance = signal_to_distance(mhz, dBm)  # Convert RSSI to distance
        distances.append(distance)
       
        # Perform trilateration using the calculated distances and AP positions
    circles = [Circle(AP_positions[0][0], AP_positions[0][1],  distances[0]),
               Circle(AP_positions[1][0], AP_positions[1][1],  distances[1]),
               Circle(AP_positions[2][0], AP_positions[2][1],  distances[2])]
    trilaterated_position = easy_least_squares(circles)

    # Kalman Filter Update Step
    # Measurement vector (trilaterated position)
    z = np.array([trilaterated_position[0].center.x, trilaterated_position[0].center.y])

    H = H_jacobian(ekf.get_state(), AP_pos)  # Compute Jacobian for the current AP
    # ekf.update(z, H, R = np.array([[5.0]]) )  # Update EKF with distance measurement and Jacobian
    ekf.update(z, H, R = np.array([[trilaterated_position[0].radius]]) )  # Update EKF with distance measurement and Jacobian
    distances.append(distance)

    # Get the estimated state (position and velocity)
    estimated_state = ekf.get_state()
    print(f"Time step {time_step}: Estimated Position: x={estimated_state[0]:.2f}, y={estimated_state[1]:.2f}")
    # result, meta = easy_least_squares(circles) 
    # create_circle(result, target=True)
    # draw(circles)


    # Plotting the estimated positions over time
    axis[0, 0].plot(estimated_state[0], estimated_state[1], 'r*')
    axis[0, 1].plot(z[0], z[1], 'g*')
    # axis[1, 0].plot(estimated_state[0], time_step, 'r*')
    # axis[1, 0].plot(z[0], time_step, 'g*')
    # axis[1, 1].plot(estimated_state[1], time_step, 'r*')
    # axis[1, 1].plot(z[1], time_step, 'g*')
    axis[1, 0].plot(time_step, estimated_state[0], 'r*')
    axis[1, 0].plot(time_step, z[0], 'g*')
    axis[1, 1].plot(time_step,estimated_state[1], 'r*')
    axis[1, 1].plot(time_step, z[1], 'g*')


# Show the trajectory of the estimated positions over time
# axis[0, 0]._label('X Position')
# axis[0, 0].ylabel('Y Position')
# axis[0, 0].set_title('Estimated Position Over Time (trilaterated with ekf)')
# axis[0, 1]._label('X Position')
# axis[0, 1].ylabel('Y Position')
# axis[0, 1].set_title('Estimated Position Over Time (trilaterated)')
plt.show()