from enum import Enum
import csv

# STRUCTURE
class Disease:
    def __init__(self, name, infection, recovery, mortality):
        self.name = name               # Disease name
        self.infection = infection     # Probability of infection when adjacent to an infected individual
        self.recovery = recovery       # Number of turns for an infected individual to recover
        self.mortality = mortality    # Probability of death for an infected individual

class State(Enum):
    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"
    DEAD = "D"

class Region:
    def __init__(self, name, population, land_area, population_density):
        self.name = name
        self.populaton = population
        self.land_area = land_area
        self.populaton_density = population_density
        self.region_stats = Statistics.__new__(self)


class Statistics(Region):
    def __init__(self, Region):
        self.susceptible_count = 0
        self.infected_count = 0
        self.recovered_count = 0
        self.dead_count = 0
        self.percent_dead = 0
        self.percent_infected = 0
        self.percent_susceptible = 0
    
    def update_percentages(self):
        if (self.population <= 0):
            raise ValueError('A population below or equal to 0 is not possible.')
                
        self.percent_dead = self.dead_count / self.population
        self.percent_infected = self.infected_count / self.population
        self.percent_susceptible = self.susceptible_count / self.population


if __name__ == '__main__':
    with open('./Data Files/KY-Population-Data.csv', newline='') as dataFile:
        reader = csv.reader(dataFile, delimiter= ',', quotechar= '|')
        header = next(reader)
        print(header)
        county_column_index = header.index("ï»¿Region")
        
        #This seperates the csv into counties - just a rough start and outline of how we can parse the data
        counties = []
        for row in reader:
            county = row[county_column_index]
            counties.append(county)
        print(counties)
        
