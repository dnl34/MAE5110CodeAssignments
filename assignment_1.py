import numpy as np
import matplotlib.pyplot as plt

from models import rimless_wheel as model
from integrators import rk4 as integrator


params = model.generate_params()

state = np.array([
    params["downhill_inc"] - params["alpha"],
    2.0
])

dt = 1e-4
sim_time = 5.0

time = np.arange(0, sim_time, dt)
state_traj = np.zeros((2, len(time)))
state_traj[:, 0] = state


for i, t in enumerate(time[:-1]):

    state = integrator.integrate(
        model.dynamics,
        t,
        state,
        dt,
        params
    )

    if model.detect_impact(state, params):
        print("Before impact:", state)

        state = model.reset_impact(state, params)

        print("After impact:", state)
        print()

    state_traj[:, i + 1] = state


# plot angle
plt.figure()
plt.plot(time, state_traj[0, :])
plt.xlabel("Time (s)")
plt.ylabel("Angle (rad)")
plt.title("Rimless Wheel Angle")
plt.tight_layout()
plt.show()

# plot angular velocity
plt.figure()
plt.plot(time, state_traj[1, :])
plt.xlabel("Time (s)")
plt.ylabel("Angular Velocity (rad/s)")
plt.title("Rimless Wheel Angular Velocity")
plt.tight_layout()
plt.show()