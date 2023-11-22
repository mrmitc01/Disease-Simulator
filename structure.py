"""
Defines classes for diseases, regions, and statistics. Reads population data from a CSV file.
"""

import random
from enum import Enum
import csv
import random
import matplotlib.pyplot as plt
import numpy as np

# REGIONS
RED_REGION_COUNTIES = ['Trimble', 'Oldham', 'Henry', 'Carroll', 'Shelby', 'Jefferson', 'Bullitt', 'Spencer']
YELLOW_REGION_COUNTIES = ['Meade', 'Grayson', 'Hardin', 'Larue', 'Washington', 'Marion', 'Taylor', 'Green', 'Hart',
                          'Edmonson', 'Breckinridge', 'Warren', 'Simpson', 'Barren', 'Allen', 'Metcalfe', 'Monroe',
                          'Nelson', 'Adair', 'Russell', 'Clinton', 'Cumberland']
ORANGE_REGION_COUNTIES = ['Hancock', 'Ohio', 'Butler', 'Logan', 'Todd', 'Muhlenberg', 'McLean', 'Daviess', 'Henderson',
                          'Webster', 'Union', 'Hopkins', 'Caldwell', 'Christian']
GRAY_REGION_COUNTIES = ['Crittenden', 'Lyon', 'Trigg', 'Livingston', 'Marshall', 'Calloway', 'McCracken', 'Graves',
                        'Ballard', 'Carlisle', 'Hickman', 'Fulton']
PINK_REGION_COUNTIES = ['Boone', 'Gallatin', 'Owen', 'Franklin', 'Anderson', 'Woodford', 'Scott', 'Grant', 'Kenton',
                        'Campbell', 'Pendleton', 'Harrison', 'Bourbon', 'Fayette', 'Jessamine', 'Bracken']
BROWN_REGION_COUNTIES = ['Whitley', 'Knox', 'Laurel', 'Jackson', 'Estill', 'Madison', 'Rockcastle', 'Pulaski',
                         'McCreary', 'Wayne', 'Casey', 'Boyle', 'Mercer', 'Garrard', 'Lincoln']
BLUE_REGION_COUNTIES = ['Bell', 'Clay', 'Owsley', 'Lee', 'Wolfe', 'Breathitt', 'Perry', 'Leslie', 'Harlan', 'Letcher',
                        'Knott', 'Magoffin', 'Johnson', 'Floyd', 'Pike', 'Martin']
MAROON_REGION_COUNTIES = ['Powell', 'Clark', 'Montgomery', 'Nicholas', 'Robertson', 'Mason', 'Fleming', 'Bath',
                          'Menifee', 'Morgan', 'Rowan', 'Lewis', 'Greenup', 'Carter', 'Elliott', 'Lawrence', 'Boyd']


# STRUCTURE
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
        self.population = population
        self.land_area = land_area
        self.populaton_density = population_density
        self.susceptible_count = population
        self.infected_count = 0
        self.recovered_count = 0
        self.dead_count = 0
        self.percent_dead = 0
        self.percent_infected = 0
        self.percent_susceptible = 100

    # Provides a method to update percentage values based on the current counts.
    def update_percentages(self):
        if self.population <= 0:
            raise ValueError('A population below or equal to 0 is not possible.')

        self.percent_dead = self.dead_count / self.population
        self.percent_infected = self.infected_count / self.population
        self.percent_susceptible = self.susceptible_count / self.population

    # Function updates the number of infected and susceptible people inside its own region based on the rates defined for the disease
    def infect(self, infection_rate):
        new_infections = min(self.susceptible_count, int(self.infected_count * infection_rate))
        self.susceptible_count -= new_infections
        self.infected_count += new_infections

    # Function updates the number of infected and susceptible people across regions based on the rates defined for the disease
    def infect_between_regions(self, infection_rate, regions):
        region_to_infect = random.choice(regions)
        new_infections = min(region_to_infect.susceptible_count,
                             int(self.infected_count + region_to_infect.infected_count * infection_rate))
        region_to_infect.susceptible_count -= new_infections
        region_to_infect.infected_count += new_infections

    # Function updates the number of infected and recovered people based on the rates defined for the disease
    def recover(self, recovery_rate):
        newly_recovered = int(self.infected_count * recovery_rate)
        self.infected_count -= newly_recovered
        self.recovered_count += newly_recovered
        return newly_recovered

    def die(self, mortality_rate):
        new_deaths = int(self.infected_count * mortality_rate)
        self.infected_count -= new_deaths
        self.dead_count += new_deaths
        return new_deaths

    def get_total_cases(self):
        return self.infected_count + self.dead_count + self.recovered_count


def run_simulation(regions, disease_stats, num_days):
    # Load in the data from each region

    # Load in the disease stats
    infection_rate = disease_stats.infection
    recovery_rate = disease_stats.recovery
    mortality_rate = disease_stats.mortality

    start_infection(regions)
    # Iterate through each "day" in the simulation
    # print(f"{'Day':<5}{}")

    for day in range(num_days):
        # Iterate through each region
        for region in regions:
            # print(region.name, 'infected', region.infected_count, 'day', day)
            print(f"{day:<5}{region.name:<20}{region.infected_count:<15}")
            # Calculate the number of new infections
            new_infections = region.infect(infection_rate)

            region.infect_between_regions(infection_rate, regions)
            # Calculate the number of recoveries
            region.recover(recovery_rate)

            # Calculate the number of deaths
            region.die(mortality_rate)

            # Update the percentages
            region.update_percentages()

        print(f"Day {day + 1} - Total cases: {sum(region.get_total_cases() for region in regions)}")


# Start the infection in a random region
def start_infection(regions):
    start_region = random.choice(regions)
    start_region.infected_count += 1
    print(f"Initial infection started in {start_region.name}")


# DISEASES
COVID = Disease(name="Covid-19", infection=0.2025, recovery=14, mortality=0.027)
MEASLES = Disease(name="Measles", infection=0.6329, recovery=7, mortality=0.0001)
FLU = Disease(name="Generic flu", infection=0.0759, recovery=10, mortality=0.0001)
EBOLA = Disease(name="Ebola", infection=0.0886, recovery=30, mortality=0.60)

# Main block: Reads population data from a CSV file and prints each row.
if __name__ == '__main__':
    red_region = Region('Outer Bluegrass', 0, 0, 0)
    yellow_region = Region('Pennyroyal', 0, 0, 0)
    orange_region = Region('Western Coal Fields', 0, 0, 0)
    pink_region = Region('Inner Blugrass', 0, 0, 0)
    brown_region = Region('Mississipi Pleateu', 0, 0, 0)
    blue_region = Region('Eastern Coal Fields', 0, 0, 0)
    maroon_region = Region('Appalachia', 0, 0, 0)
    gray_region = Region('Jackson Purchase', 0, 0, 0)

    with open('./Data Files/KY-Population-Data.csv', newline='') as dataFile:
        reader = csv.reader(dataFile, delimiter=',', quotechar='|')
        header = next(reader)
        county_column_index = header.index("ï»¿Region")
        population_column_index = header.index('Total Population')
        land_area_column_index = header.index('Land Area')
        population_density_column_index = header.index('Population Density')

        # This separates the CSV into counties - just a rough start and outline of how we can parse the data
        for row in reader:
            county = row[county_column_index]
            if county in RED_REGION_COUNTIES:
                red_region.population += int(row[population_column_index])
                red_region.susceptible_count += int(row[population_column_index])
                red_region.land_area += float(row[land_area_column_index])
                red_region.populaton_density += float(row[population_column_index])
            elif county in YELLOW_REGION_COUNTIES:
                yellow_region.population += int(row[population_column_index])
                yellow_region.susceptible_count += int(row[population_column_index])
                yellow_region.land_area += float(row[land_area_column_index])
                yellow_region.populaton_density += float(row[population_column_index])
            elif county in ORANGE_REGION_COUNTIES:
                orange_region.population += int(row[population_column_index])
                orange_region.susceptible_count += int(row[population_column_index])
                orange_region.land_area += float(row[land_area_column_index])
                orange_region.populaton_density += float(row[population_column_index])
            elif county in PINK_REGION_COUNTIES:
                pink_region.population += int(row[population_column_index])
                pink_region.susceptible_count += int(row[population_column_index])
                pink_region.land_area += float(row[land_area_column_index])
                pink_region.populaton_density += float(row[population_column_index])
            elif county in BROWN_REGION_COUNTIES:
                brown_region.population += int(row[population_column_index])
                brown_region.susceptible_count += int(row[population_column_index])
                brown_region.land_area += float(row[land_area_column_index])
                brown_region.populaton_density += float(row[population_column_index])
            elif county in BLUE_REGION_COUNTIES:
                blue_region.population += int(row[population_column_index])
                blue_region.susceptible_count += int(row[population_column_index])
                blue_region.land_area += float(row[land_area_column_index])
                blue_region.populaton_density += float(row[population_column_index])
            elif county in MAROON_REGION_COUNTIES:
                maroon_region.population += int(row[population_column_index])
                maroon_region.susceptible_count += int(row[population_column_index])
                maroon_region.land_area += float(row[land_area_column_index])
                maroon_region.populaton_density += float(row[population_column_index])
            elif county in GRAY_REGION_COUNTIES:
                gray_region.population += int(row[population_column_index])
                gray_region.susceptible_count += int(row[population_column_index])
                gray_region.land_area += float(row[land_area_column_index])
                gray_region.populaton_density += float(row[population_column_index])

    All_Regions = [red_region, orange_region, yellow_region, pink_region, brown_region, blue_region, maroon_region,
                   gray_region]
    run_simulation(All_Regions, COVID, 10)
