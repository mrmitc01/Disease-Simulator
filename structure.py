from enum import Enum
import csv

# STRUCTURE
class Disease:
    def __init__(self, name, infection, recovery, mortality):
        self.name = name             # Disease name
        self.infection = infection   # Probability of infection when adjacent to an infected individual
        self.recovery = recovery     # Number of turns for an infected individual to recover
        self. mortality = mortality  # Probability of death for an infected individual

class State(Enum):
    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"
    DEAD = "D"

class Statistics:
    def __init__(self):
        self.susceptible_count = 0
        self.infected_count = 0
        self.recovered_count = 0
        self.dead_count = 0

class Region:
    def __init__(self, name, population, land_area, population_density):
        self.name = name
        self.populaton = population
        self.land_area = land_area
        self.populaton_density = population_density


if __name__ == '__main__':
    with open('./Data Files/KY-Population-Data.csv', newline='') as dataFile:
        reader = csv.reader(dataFile, delimiter= ' ', quotechar= '|')
        for row in reader:
            print(', '.join(row))
