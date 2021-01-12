# Function to determine the size of a sample: Reference: https://www.netquest.com/blog/br/blog/br/qual-e-o-tamanho-de-amostra-que-preciso
# Parameters:
#   n_population = total size of population
#   confidence = confidence interval: the probability of sample represent the population correctely (default: 0.95 or 95%)
#   error_margin = the percentage of variation that population can have in relation of the sample; for more and less; (default: between 0.95 and 0.99)
#   proportion = proportion expected of population values distribution (default 0.5)

def sample_size_calculator(n_population, confidence, error_margin, proportion):

    # Defining z through proportion expected of population
    if confidence == 0.9:
        z = 1.645
    elif confidence == 0.95:
        z = 1.96
    elif confidence == 0.99:
        z = 2.575
    elif confidence == 0.85:
        z = 1.44
    else:
        z = 0

    return round((n_population * (pow(z,2)) * proportion * (1 - proportion)) /
                 ((n_population - 1) * pow(error_margin,2) + pow(z,2) * proportion * (1-proportion))) + 1


# Set the parameters and see the size of your sample:
print(sample_size_calculator(4210, 0.95, 0.05, 0.5))