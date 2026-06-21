"""
============================================================
Tour Utilities
Chen Yap Koh; Vincent Tay Yong Jun; Lew Zi Xin
Description:
    Common functions shared by

    - Local Search
    - Genetic Algorithm
    - Ant Colony Optimization
============================================================
"""

import random


def generate_random_tour(number_of_cities):
    #Generate a random valid tour.
    # Create list of city indices
    tour = list(range(number_of_cities))
    # Shuffle randomly
    random.shuffle(tour)

    return tour


def calculate_tour_length(tour, distance_matrix):
    """
    Calculate the total distance of a tour.
    Parameters
    ----------
    tour : list
    distance_matrix : list
    Returns
    -------
    float
    """

    total_distance = 0
    number_of_cities = len(tour)

    # Calculate every edge

    for i in range(number_of_cities):
        current_city = tour[i]
        # Return back to the first city
        next_city = tour[(i + 1) % number_of_cities]
        total_distance += distance_matrix[current_city][next_city]

    return total_distance


def print_tour(tour):
    #Display a tour.
    print(" -> ".join(map(str, tour)))
    print(" ->", tour[0])