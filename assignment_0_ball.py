import numpy as np
import matplotlib.pyplot as plt

from models import bouncing_ball as model
from integrators import rk4 as integrator


params = model.generate_params()

initial_state = np.array([1.0, 0.0])

timestep = 1e-5
sim_time = 5.0

n_timesteps = int(sim_time / timestep) + 1
time_traj = np.arange(n_timesteps) * timestep

state_traj = np.zeros((2, n_timesteps))
state_traj[:, 0] = initial_state


for step, t in enumerate(time_traj[:-1]):

    state_traj[:, step + 1] = integrator.integrate(
        model.dynamics,
        t,
        state_traj[:, step],
        timestep,
        params
    )

    # bounce when ball reaches the ground
    if state_traj[0, step + 1] <= 0 and state_traj[1, step + 1] < 0:
        state_traj[0, step + 1] = 0
        state_traj[1, step + 1] *= -params["restitution"]


# plot height
plt.figure()
plt.plot(time_traj, state_traj[0, :])
plt.xlabel("Time (s)")
plt.ylabel("Height (m)")
plt.title("Bouncing Ball Height")
plt.tight_layout()
plt.show()