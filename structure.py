"""
Defines classes for diseases, regions, and statistics. Reads population data from a CSV file.
"""

from enum import Enum
import csv


# STRUCTURE

# Represents a disease with attributes such as name, infection probability, recovery duration, and mortality
# probability.
class Disease:
    def __init__(self, name, infection, recovery, mortality):
        self.name = name  # Disease name
        self.infection = infection  # Probability of infection when adjacent to an infected individual
        self.recovery = recovery  # Number of turns for an infected individual to recover
        self.mortality = mortality  # Probability of death for an infected individual


# Enumerates different states an individual can be in, such as SUSCEPTIBLE, INFECTED, RECOVERED, and DEAD.
class State(Enum):
    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"
    DEAD = "D"


# Represents a geographical region with attributes like name, population, land area, and population density.
class Region:
    def __init__(self, name, population, land_area, population_density):
        self.name = name
        self.populaton = population
        self.land_area = land_area
        self.populaton_density = population_density
        self.region_stats = Statistics.__new__(self)


# Represents statistics for a region, including counts of susceptible, infected, recovered, and dead individuals,
# as well as percentages.
class Statistics(Region):
    def __init__(self, Region):
        self.susceptible_count = 0
        self.infected_count = 0
        self.recovered_count = 0
        self.dead_count = 0
        self.percent_dead = 0
        self.percent_infected = 0
        self.percent_susceptible = 0

    # Provides a method to update percentage values based on the current counts.
    def update_percentages(self):
        if (self.population <= 0):
            raise ValueError('A population below or equal to 0 is not possible.')

        self.percent_dead = self.dead_count / self.population
        self.percent_infected = self.infected_count / self.population
        self.percent_susceptible = self.susceptible_count / self.population


# Main block: Reads population data from a CSV file and prints each row.
if __name__ == '__main__':
    with open('./Data Files/KY-Population-Data.csv', newline='') as dataFile:
        reader = csv.reader(dataFile, delimiter=' ', quotechar='|')
        for row in reader:
            print(', '.join(row))
