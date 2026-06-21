"""
============================================================
2-Opt Local Search

Author : Chen Yap Koh; Vincent Tay Yong Jun; Lew Zi Xin
============================================================
"""
from utils.tour_utils import calculate_tour_length


def two_opt_swap(tour, i, j):
    new_tour = tour.copy()    # Create a copy of the tour
    new_tour[i:j + 1] = reversed(new_tour[i:j + 1])    # Reverse the segment between i and j
    return new_tour


def two_opt(distance_matrix, initial_tour):
    best_tour = initial_tour.copy()    # Keep a copy of the current best solution
    best_distance = calculate_tour_length(best_tour, distance_matrix)    # Calculate its length
    number_of_cities = len(best_tour)
    improved = True
    while improved:
        improved = False
        # Store the best improvement found in this iteration
        candidate_tour = None
        candidate_distance = best_distance

        for i in range(number_of_cities - 1):        # Try every possible swap
            for j in range(i + 1, number_of_cities):
                new_tour = two_opt_swap(best_tour, i, j)
                new_distance = calculate_tour_length(
                    new_tour,
                    distance_matrix
                )

                if new_distance < candidate_distance:       #check if this is the best improvement found so far
                    candidate_distance = new_distance
                    candidate_tour = new_tour
        # After checking ALL swaps,accept the best one.
        if candidate_tour is not None:
            best_tour = candidate_tour
            best_distance = candidate_distance
            improved = True

    return best_tour, best_distance