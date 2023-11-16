import random

def run_simulation(self, regions, disease_stats, num_days):
    # Load in the data from each region

    # Load in the disease stats
    infection_rate = disease_stats.infection
    recovery_rate = disease_stats.recovery
    mortality_rate = disease_stats.mortality

    # Start the infection in a random region
    def start_infection(self):
        start_region = random.choice(regions)
        start_region.infected_count += 1


    # Iterate through each "day" in the simulation
    for day in range(1, num_days):
        # Iterate through each region
        for region in regions: 
            # Calculate the number of new infections
            new_infections = region.infect(infection_rate)

            # Calculate the number of recoveries
            new_recoveries = region.recover(recovery_rate)

            # Calculate the number of deaths
            new_deaths = region.die(mortality_rate)

            # Update the counts in the region structure
            region.infection_count -= new_recoveries
            region.infection_count += new_infections
            region.recovered_count += new_recoveries
            region.death_count += new_deaths

            # Update the percentages
            region.update_percentages()


