from math import sqrt
import random


def distance(point_1, point_2):
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    return sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)


def connect_beginning_to_end(points):
    return [points[i] for i in range(len(points) - 1)] + [points[-1], points[0]]


def generate_tour(num_points, x_range, y_range):
    return [
        (random.randint(*x_range), random.randint(*y_range)) for _ in range(num_points)
    ]


def tour_length(tour):
    total = 0
    for i, vertex in enumerate(tour):
        next_i = i + 1 if i + 1 < len(tour) else 0
        total += distance(vertex, tour[next_i])

    return total
