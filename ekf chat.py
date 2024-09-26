import numpy as np

class EKF:
    def __init__(self, dt, state_dim, meas_dim, F, H, Q, R, x0, P0):
        self.dt = dt
        self.state_dim = state_dim
        self.meas_dim = meas_dim
        self.F = F            # State transition model
        self.H = H            # Observation model
        self.Q = Q            # Process noise covariance
        self.R = R            # Measurement noise covariance
        self.x = x0           # Initial state estimate
        self.P = P0           # Initial state covariance estimate

    def predict(self):
        # Predict the next state
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        # Compute Kalman Gain
        y = z - np.dot(self.H, self.x)  # Innovation
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # Kalman gain

        # Update the state estimate
        self.x = self.x + np.dot(K, y)

        # Update the covariance estimate
        I = np.eye(self.state_dim)
        self.P = np.dot((I - np.dot(K, self.H)), self.P)

    def get_state(self):
        return self.x

# EKF Parameters
dt = 1.0  # Time step
state_dim = 4  # [x, y, vx, vy]
meas_dim = 1   # RSSI measurement (distance)

# State transition matrix (for constant velocity model)
F = np.array([[1, 0, dt, 0],
              [0, 1, 0, dt],
              [0, 0, 1,  0],
              [0, 0, 0,  1]])

# Observation matrix (we observe distance based on position)
def H_jacobian(x, AP_pos):
    # Nonlinear observation model for distance
    dx = x[0] - AP_pos[0]
    dy = x[1] - AP_pos[1]
    distance = np.sqrt(dx**2 + dy**2)
    H = np.array([[dx / distance, dy / distance, 0, 0]])
    return H

# Process noise covariance (how much uncertainty in the model)
Q = np.eye(state_dim) * 0.01

# Measurement noise covariance (RSSI noise)
R = np.array([[1.0]])

# Initial state and covariance estimates
x0 = np.array([0, 0, 0, 0])  # Initial position and velocity
P0 = np.eye(state_dim)

# EKF Object
ekf = EKF(dt, state_dim, meas_dim, F, None, Q, R, x0, P0)

# Parameters for the RSSI model
P_t = -40  # Transmission power in dBm
n = 2.0    # Path loss exponent

def rssi_to_distance(rssi, P_t, n):
    return 10 ** ((P_t - rssi) / (10 * n))

# Access Point position
AP_pos = np.array([10, 10])

# Simulate some RSSI measurements
rssis = [-60, -62, -61, -63, -64]  # Example RSSI values

# Print header
print("Estimated positions over time:")

for rssi in rssis:
    # Convert RSSI to distance
    distance = rssi_to_distance(rssi, P_t, n)
    
    # Perform prediction step
    ekf.predict()

    # Update step using the Jacobian H and distance measurement
    H = H_jacobian(ekf.get_state(), AP_pos)
    ekf.H = H  # Set the updated H
    ekf.update(np.array([distance]))

    # Get the estimated state
    estimated_state = ekf.get_state()
    print(f"Estimated Position: x={estimated_state[0]:.2f}, y={estimated_state[1]:.2f}")
