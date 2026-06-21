import random
from utils.tour_utils import generate_random_tour
from utils.tour_utils import calculate_tour_length

def generate_population(population_size, number_of_cities):
    population = []
    for _ in range(population_size):
        tour = generate_random_tour(number_of_cities)
        population.append(tour)
    return population

def calculate_fitness(tour, distance_matrix):
    tour_length = calculate_tour_length(tour, distance_matrix)
    # Prevent division by zero
    if tour_length == 0:
        return float("inf")
    return 1 / tour_length

def tournament_selection(population, distance_matrix, tournament_size=3):
    # Randomly choose tournament_size tours
    candidates = random.sample(population, tournament_size)
    # Assume the first candidate is the best
    winner = candidates[0]
    best_fitness = calculate_fitness(winner, distance_matrix)
    # Compare with the remaining candidates
    for candidate in candidates[1:]:
        fitness = calculate_fitness(candidate, distance_matrix)
        if fitness > best_fitness:
            winner = candidate
            best_fitness = fitness
    # Return a copy to avoid accidental modification
    return winner.copy()

def order_crossover(parent1, parent2):
    number_of_cities = len(parent1)
    child = [-1] * number_of_cities
    start = random.randint(0, number_of_cities - 2)
    end = random.randint(start + 1, number_of_cities - 1)
    child[start:end+1] = parent1[start:end+1]    # Copy middle segment
    current_position = (end + 1) % number_of_cities
    parent_position = (end + 1) % number_of_cities
    while -1 in child:
        city = parent2[parent_position]
        if city not in child:
            child[current_position] = city
            current_position = (current_position + 1) % number_of_cities
        parent_position = (parent_position + 1) % number_of_cities
    return child

def swap_mutation(tour, mutation_rate=0.02):
    # Make a copy so the original isn't modified
    mutated_tour = tour.copy()
    # Decide whether mutation occurs
    if random.random() < mutation_rate:
        # Select two different positions
        i, j = random.sample(range(len(mutated_tour)), 2)
        # Swap the cities
        mutated_tour[i], mutated_tour[j] = (
            mutated_tour[j],
            mutated_tour[i]
        )
    return mutated_tour

def find_best_individual(population, distance_matrix):
    best_tour = population[0]
    best_distance = calculate_tour_length(best_tour, distance_matrix)
    for tour in population[1:]:
        distance = calculate_tour_length(tour, distance_matrix)
        if distance < best_distance:
            best_tour = tour
            best_distance = distance
    return best_tour.copy(), best_distance

def genetic_algorithm(
    distance_matrix,
    initial_tour=None,
    population_size=150,
    generations=500,
    mutation_rate=0.03
):
    number_of_cities = len(distance_matrix)
    population = generate_population(    # Generate initial population
        population_size,
        number_of_cities
    )
    best_tour, best_distance = find_best_individual(    # Initial best solution
        population,
        distance_matrix
    )
    for generation in range(generations):    # Main evolution loop
        new_population = []
        # -------- Elitism --------
        new_population.append(best_tour.copy())
        # Fill remaining population
        while len(new_population) < population_size:
            parent1 = tournament_selection(
                population,
                distance_matrix
            )
            parent2 = tournament_selection(
                population,
                distance_matrix
            )
            child = order_crossover(
                parent1,
                parent2
            )
            child = swap_mutation(
                child,
                mutation_rate
            )
            new_population.append(child)
        population = new_population
        current_best, current_distance = find_best_individual(        # Update best solution
            population,
            distance_matrix
        )
        if current_distance < best_distance:
            best_tour = current_best
            best_distance = current_distance
    return best_tour, best_distance