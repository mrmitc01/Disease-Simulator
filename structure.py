"""
Defines classes for diseases, regions, and statistics. Reads population data from a CSV file.
"""

from enum import Enum
import csv

RED_REGION_COUNTIES = ['Trimble', 'Oldham', 'Henry', 'Carroll', 'Shelby', 'Jefferson', 'Bullitt', 'Spencer']
YELLOW_REGION_COUNTIES = ['Meade', 'Grayson', 'Hardin', 'Larue', 'Washington', 'Marion', 'Taylor', 'Green', 'Hart', 'Edmonson', 'Breckinridge', 'Warren', 'Simpson', 'Barren', 'Allen', 'Metcalfe', 'Monroe', 'Nelson', 'Adair', 'Russell', 'Clinton', 'Cumberland']
ORANGE_REGION_COUNTIES = ['Hancock', 'Ohio', 'Butler', 'Logan', 'Todd', 'Muhlenberg', 'McLean', 'Daviess', 'Henderson', 'Webster', 'Union', 'Hopkins', 'Caldwell', 'Christian']
GRAY_REGION_COUNTIES = ['Crittenden', 'Lyon', 'Trigg', 'Livingston', 'Marshall', 'Calloway', 'McCracken', 'Graves', 'Ballard', 'Carlisle', 'Hickman', 'Fulton']
PINK_REGION_COUNTIES = ['Boone', 'Gallatin', 'Owen', 'Franklin', 'Anderson', 'Woodford', 'Scott', 'Grant', 'Kenton', 'Campbell', 'Pendleton', 'Harrison', 'Bourbon', 'Fayette', 'Jessamine', 'Bracken']
BROWN_REGION_COUNTIES = ['Whitley', 'Knox', 'Laurel', 'Jackson', 'Estill', 'Madison', 'Rockcastle', 'Pulaski', 'McCreary', 'Wayne', 'Casey', 'Boyle', 'Mercer', 'Garrard', 'Lincoln']
BLUE_REGION_COUNTIES = ['Bell', 'Clay', 'Owsley', 'Lee', 'Wolfe', 'Breathitt', 'Perry', 'Leslie', 'Harlan', 'Letcher', 'Knott', 'Magoffin', 'Johnson', 'Floyd', 'Pike', 'Martin']
MAROON_REGION_COUNTIES = ['Powell', 'Clark', 'Montgomery', 'Nicholas', 'Robertson', 'Mason', 'Fleming', 'Bath', 'Menifee', 'Morgan', 'Rowan', 'Lewis', 'Greenup', 'Carter', 'Elliott', 'Lawrence']
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
        reader = csv.reader(dataFile, delimiter= ',', quotechar= '|')
        header = next(reader)
        print(header)
        county_column_index = header.index("ï»¿Region")
        
        # This separates the CSV into counties - just a rough start and outline of how we can parse the data
        counties = []
        for row in reader:
            county = row[county_column_index]
            counties.append(county)

        print(len(counties))
