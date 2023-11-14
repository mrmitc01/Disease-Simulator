
# Function updates the number of infected and susceptible people based on the rates defined for the disease
def infect(self, infection_rate):
    new_infections = min(self.region_stats.susceptible_count, int(self.region_stats.infected_count * infection_rate))
    self.susceptible_count -= new_infections
    self.infected_count += new_infections
    return new_infections

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

def get_total_cases(self):
    return self.infected_count + self.susceptible_count + self.recovered_count

def run_simulation(self, regions, disease_stats, num_days):
    # Load in the data from each region

    # Load in the disease stats
    infection_rate = disease_stats.infection
    recovery_rate = disease_stats.recovery
    mortality_rate = disease_stats.mortality

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
            

