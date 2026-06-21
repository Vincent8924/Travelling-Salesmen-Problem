"""
============================================================
Distance Matrix Generator(The distance matrix in Lab Questions)
Author : Chen Yap Koh; Vincent Tay Yong Jun; Lew Zi Xin
Description:
    Builds the Euclidean distance matrix from city coordinates.
============================================================
"""

import math
from turtle import distance


def euclidean_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return round(distance)


def build_distance_matrix(coordinates):
    number_of_cities = len(coordinates)
    distance_matrix = []
    # Loop through every city
    for i in range(number_of_cities):
        row = []
        # Calculate distance to every other city
        for j in range(number_of_cities):
            distance = euclidean_distance(
                coordinates[i],
                coordinates[j]
            )
            row.append(distance)
        distance_matrix.append(row)
    return distance_matrix