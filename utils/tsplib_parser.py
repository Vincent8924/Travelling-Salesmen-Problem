"""
============================================================
TSPLIB Parser(TDA Project)
Author : Chen Yap Koh; Vincent Tay Yong Jun; Lew Zi Xin
Project: TDA Project - Traveling Salesman Problem (TSP)
Description:
    Reads a TSPLIB (.tsp) file and extracts
    1. Metadata
    2. City coordinates
This parser is written from scratch without using tsplib95.

"""


def load_tsplib(filepath):

    metadata = {}
    coordinates = []

    reading_coordinates = False


    with open(filepath, "r") as file:

        # Read every line
        for line in file:
            # to remove spaces and newline characters from the beginning and end of the line
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            if line == "NODE_COORD_SECTION":
                reading_coordinates = True
                continue

            # Stop reading if EOF is reached, EOF is inside the .tsp file
            if line == "EOF":
                break



            # PART 1 Read Metadata
            if not reading_coordinates:
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()


            # PART 2 Read Coordinates
            else:

                parts = line.split()
                # Ignore invalid rows
                if len(parts) >= 3:
                    city_id = int(parts[0])     # Not used now
                    x = float(parts[1])
                    y = float(parts[2])
                    coordinates.append((x, y))

    return metadata, coordinates