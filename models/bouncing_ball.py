import numpy as np


def dynamics(t, state, params):
    gravity = params["gravity"]

    height = state[0]
    velocity = state[1]

    acceleration = -gravity

    state_derivative = np.array([velocity, acceleration])
    return state_derivative


def generate_params():
    params = {
        "gravity": 9.81,
        "mass": 1.0,
        "restitution": 0.7,
    }
    return params


def calculate_energy(state, params):
    gravity = params["gravity"]
    mass = params["mass"]

    height = state[0]
    velocity = state[1]

    kinetic_energy = 0.5 * mass * velocity**2
    potential_energy = mass * gravity * height

    return kinetic_energy, potential_energy