from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

from models import inverted_pendulum_walker as model

# Fixed controls for this visualization example.
params = {
    "gravity": 9.81,  # m/s^2
    "length": 1.0,  # m
    "mass": 1.0,  # kg
    "incline": 0.06,  # rad
    "angle_of_attack": np.pi / 8,  # rad
    "ankle_torque": 0.0,  # N m
}

initial_state = np.array([0.0, 3.0])
timestep = 1e-4
sim_time = 3.0
desired_number_of_steps = 3

n_timesteps = round(sim_time / timestep) + 1
time_traj = np.arange(n_timesteps) * timestep
state_traj = np.zeros((2, n_timesteps))
state_traj[:, 0] = initial_state
completed_steps = 0

# Simulation loop. Replace this Euler step with your own integrator as needed.
for step, t in enumerate(time_traj[:-1]):
    state = state_traj[:, step]
    next_state = state + timestep * model.dynamics(t, state, params)

    if model.event_guard(state, next_state, params):
        next_state = model.event_dynamics(next_state, params)
        completed_steps += 1

    state_traj[:, step + 1] = next_state
    if completed_steps == desired_number_of_steps:
        break

time_traj = time_traj[: step + 2]
state_traj = state_traj[:, : step + 2]

fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")


def draw_frame(index):
    # The massless swing leg is repositioned instantaneously at each impact.
    model.visualize(state_traj[:, index], params, ax=ax)
    ax.set_title(f"t = {time_traj[index]:.2f} s")


# Simulate at a small timestep, but render only 25 frames per second.
fps = 25
frame_stride = round(1 / (fps * timestep))
frame_indices = list(range(0, time_traj.size, frame_stride))
if frame_indices[-1] != time_traj.size - 1:
    frame_indices.append(time_traj.size - 1)

animation = FuncAnimation(
    fig, draw_frame, frames=frame_indices, interval=1000 / fps, repeat=False
)
output = Path("output/assignment_2")
output.mkdir(parents=True, exist_ok=True)
animation.save(output / "walker.gif", writer=PillowWriter(fps=fps))

# To save an MP4 instead, install FFmpeg and use:
# animation.save(output / "walker.mp4", writer="ffmpeg", fps=fps)
print(f"Saved {output / 'walker.gif'} ({completed_steps} footstrikes).")
plt.show()

def feedback_linearization(state,params,damping):
    gravity = params["gravity"]
    length = params["length"]
    mass = params["mass"]

    angle = state[0]
    angular_velocity = state[1]

    ankle_torque = (-2 * mass * gravity * length
        * np.sin(angle) - damping * angular_velocity)

    min_torque = -0.1 * mass * gravity * length
    max_torque = 0.05 * mass * gravity * length

    ankle_torque = np.clip(ankle_torque, min_torque, max_torque)

    return ankle_torque

def test_feedback_controller(initial_state, params, damping):
    params["ankle_torque"] = 0.0

    timestep = 1e-4
    sim_time = 5.0

    state = initial_state.copy()

    angle_stable_tolerance = 0.01
    angular_velocity_stable_tolerance = 0.01

    stable_time = 0.1
    stable_steps_required = round(stable_time / timestep)
    stable_steps = 0

    for t in np.arange(0, sim_time, timestep):

        params["ankle_torque"] = feedback_linearization(state, params, damping)

        state = state + timestep * model.dynamics(t, state, params)

        if (abs(state[0]) < angle_stable_tolerance and
                abs(state[1]) < angular_velocity_stable_tolerance):
            stable_steps += 1
        else:
            stable_steps = 0

        if stable_steps >= stable_steps_required:
            return True

    return False

# damping = 1.0

# initial_state = np.array([0.02, 0.0])

# result = test_feedback_controller(initial_state, params, damping)

# print(result)

def calculate_roa(params,damping):

    angle_values = np.linspace(-0.15, 0.15, 30)
    angular_velocity_values = np.linspace(-0.75, 0.75, 30)

    roa = np.zeros((len(angular_velocity_values), len(angle_values)))

    for i, angular_velocity in enumerate(angular_velocity_values):
        for j, angle in enumerate(angle_values):

            initial_state = np.array([angle, angular_velocity])

            if test_feedback_controller(initial_state, params, damping):
                roa[i, j] = 1

    return angle_values, angular_velocity_values, roa

damping = 1.0

angle_values, angular_velocity_values, roa = calculate_roa(params, damping)

plt.figure()

plt.imshow(
    roa,
    origin="lower",
    extent=[
        angle_values[0],
        angle_values[-1],
        angular_velocity_values[0],
        angular_velocity_values[-1]
    ],
    aspect="auto"
)

plt.xlabel("Angle (rad)")
plt.ylabel("Angular Velocity (rad/s)")
plt.title("Region of Attraction")
plt.show()

def roa_event_guard(state, angle_values, angular_velocity_values, roa):
    angle = state[0]
    angular_velocity = state[1]

    if (angle < angle_values[0] or angle > angle_values[-1] or
            angular_velocity < angular_velocity_values[0] or
            angular_velocity > angular_velocity_values[-1]):
        return False

    angle_index = np.argmin(np.abs(angle_values - angle))
    velocity_index = np.argmin(np.abs(angular_velocity_values - angular_velocity))

    return roa[velocity_index, angle_index] == 1