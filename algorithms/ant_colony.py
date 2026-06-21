# algorithms/ant_colony.py
import random
from utils.tour_utils import calculate_tour_length
class Ant:
    def __init__(self):
        self.tour = []              # Tour constructed by this ant
        self.length = float("inf")  # Total tour length
        self.current_city = None    # Current city
        self.visited = set()        # Visited cities


def initialize_pheromone_matrix(number_of_cities, initial_pheromone=1.0):
    pheromone_matrix = []
    for i in range(number_of_cities):
        row = []
        for j in range(number_of_cities):
            row.append(initial_pheromone)
        pheromone_matrix.append(row)
    return pheromone_matrix

def calculate_visibility_matrix(distance_matrix):
    number_of_cities = len(distance_matrix)
    visibility_matrix = []

    for i in range(number_of_cities):
        row = []
        for j in range(number_of_cities):
            if i == j:
                row.append(0)
            else:
                row.append(1 / distance_matrix[i][j])
        visibility_matrix.append(row)
        if i != j and distance_matrix[i][j] == 0:
            print(f"Zero distance: {i} -> {j}")
    return visibility_matrix

def calculate_transition_probabilities(
    current_city,
    unvisited,
    pheromone_matrix,
    visibility_matrix,
    alpha=1.0,
    beta=5.0
):
    probabilities = {}
    total = 0
    # Calculate denominator
    for city in unvisited:
        value = (
            pheromone_matrix[current_city][city] ** alpha
        ) * (
            visibility_matrix[current_city][city] ** beta
        )
        probabilities[city] = value
        total += value
    if total == 0:
        equal_prob = 1.0 / len(unvisited)
        for city in unvisited:
            probabilities[city] = equal_prob
        return probabilities
    # Normalize
    for city in probabilities:
        probabilities[city] /= total
    return probabilities

def select_next_city(probabilities):
    random_number = random.random()
    cumulative_probability = 0
    for city, probability in probabilities.items():

        cumulative_probability += probability

        if random_number <= cumulative_probability:
            return city
    return list(probabilities.keys())[-1]    # Safety fallback

def construct_ant_tour(
    pheromone_matrix,
    visibility_matrix,
    distance_matrix,
    alpha=1.0,
    beta=5.0
):
    number_of_cities = len(distance_matrix)
    ant = Ant()
    # Random starting city
    ant.current_city = random.randint(0, number_of_cities - 1)
    ant.tour.append(ant.current_city)
    ant.visited.add(ant.current_city)
    while len(ant.tour) < number_of_cities:
        unvisited = []
        for city in range(number_of_cities):

            if city not in ant.visited:
                unvisited.append(city)
        probabilities = calculate_transition_probabilities(
            ant.current_city,
            unvisited,
            pheromone_matrix,
            visibility_matrix,
            alpha,
            beta
        )
        next_city = select_next_city(probabilities)
        ant.tour.append(next_city)
        ant.visited.add(next_city)
        ant.current_city = next_city

    ant.length = calculate_tour_length(
        ant.tour,
        distance_matrix
    )
    return ant

def construct_colony(
    number_of_ants,
    pheromone_matrix,
    visibility_matrix,
    distance_matrix,
    alpha=1.0,
    beta=5.0
):
    colony = []
    for _ in range(number_of_ants):
        ant = construct_ant_tour(
            pheromone_matrix,
            visibility_matrix,
            distance_matrix,
            alpha,
            beta
        )
        colony.append(ant)
    return colony

def find_best_ant(colony):  
    best_ant = colony[0]
    for ant in colony[1:]:
        if ant.length < best_ant.length:

            best_ant = ant
    return best_ant

def evaporate_pheromone(
    pheromone_matrix,
    evaporation_rate=0.5
):
    number_of_cities = len(pheromone_matrix)
    for i in range(number_of_cities):
        for j in range(number_of_cities):
            pheromone_matrix[i][j] *= (1 - evaporation_rate)

def deposit_pheromone(
    pheromone_matrix,
    colony,
    q=100
):
    for ant in colony:
        contribution = q / ant.length
        number_of_cities = len(ant.tour)
        for i in range(number_of_cities):
            city1 = ant.tour[i]
            city2 = ant.tour[(i + 1) % number_of_cities]
            pheromone_matrix[city1][city2] += contribution
            pheromone_matrix[city2][city1] += contribution
    
def ant_colony_optimization(
    distance_matrix,
    initial_tour=None,#ant colony wont use initial tour, its just for easy function call in main
    iterations=300,
    alpha=1.0,
    beta=5.0,
    evaporation_rate=0.5,
    q=100
):

    number_of_cities = len(distance_matrix)
    number_of_ants = number_of_cities
    pheromone_matrix = initialize_pheromone_matrix(
        number_of_cities
    )
    visibility_matrix = calculate_visibility_matrix(
        distance_matrix
    )
    best_tour = None
    best_distance = float("inf")
    for iteration in range(iterations):
        colony = construct_colony(
            number_of_ants,
            pheromone_matrix,
            visibility_matrix,
            distance_matrix,
            alpha,
            beta
        )
        best_ant = find_best_ant(colony)
        if best_ant.length < best_distance:
            best_distance = best_ant.length
            best_tour = best_ant.tour.copy()

        evaporate_pheromone(
            pheromone_matrix,
            evaporation_rate
        )
        deposit_pheromone(
            pheromone_matrix,
            colony,
            q
        )
    return best_tour, best_distance