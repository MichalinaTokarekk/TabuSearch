import random
import math
from copy import deepcopy
import time
import matplotlib.pyplot as plt

from utils import (
    connect_beginning_to_end,
    tour_length,
)


def accept_solution(delta, temperature):
    if delta < 0:
        return True, 1

    r = random.random()

    acceptance_th = math.exp(-delta / temperature)

    if r < acceptance_th:
        return True, acceptance_th

    return False, acceptance_th


def generate_new_solution_permutation(tour):
    new_tour = tour[:]
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour


def simulated_annealing(
    tour, t_max=500, t_min=0.1, e_th=5, a=1 + 1e-3, plot_data=False
):
    # T_max = the maximum temperature
    # T_min = the minimum temperature for stopping the algorithm
    # E_th = the energy threshold to stop the algorithm
    # alpha = the cooling factor

    tour = deepcopy(tour)

    temperature = t_max
    energy = tour_length(tour)

    ths = []
    ts = []

    while temperature > t_min and energy > e_th:
        #print(temperature, a)
        ts.append(temperature)
        candidate_tour = generate_new_solution_permutation(tour)
        candidate_energy = tour_length(connect_beginning_to_end(candidate_tour))
        energy_delta = candidate_energy - energy

        accept, th = accept_solution(energy_delta, temperature)
        ths.append(th)

        if accept:
            tour = candidate_tour
            energy = candidate_energy

        temperature = temperature / a

    return connect_beginning_to_end(tour)
