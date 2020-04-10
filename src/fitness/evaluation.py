from src.parameters.parameters import params
import numpy as np
from stats.statistics import stats
"""Based on Ponyge2's 'evaluation.py'  """

def takeSecond(elem):
    return elem[1]
def evaluate_herd(individuals):
    """
    Evaluate an entire population of individuals for invalid individuals. Invalid individuals are given
    a default bad fitness.
    :param individuals: A population of individuals to be evaluated.
    """
    total_fitness = 0
    betas = [] * len(individuals)
    fitness_herd = [[0,0]] * len(individuals)

    for i in range(len(individuals)):
        ind = individuals[i]
        if ind.invalid:
            stats['number_of_invalids'] += 1
        else:
            total_fitness += ind.fitness
            # Stores the index from Individuals for this herd member
            fitness_herd[i] = [i, ind.fitness]
            # Stores the fitness of the herd member

    print(fitness_herd)
    average_fitness = (total_fitness / (len(individuals) - stats['number_of_invalids']))

    sorted_herd = sorted(fitness_herd, key=lambda x:-x[1])

    if params['NUMBER_OF_ALPHAS'] >= params['NUMBER_OF_BETAS']:
        raise Exception('ERROR: Number of Alphas cannot be higher or equal to the number of Betas')
    else:
        if params['NUMBER_OF_BETAS'] > params['HERD_SIZE']:
            print("WARNING: Number of Betas is set to greater than population, setting Betas to population size")
            params['NUMBER_OF_BETAS'] = params['HERD_SIZE']
        # Sets the individuals with the best fitness to Betas and Alphas
        for i in range(params['NUMBER_OF_BETAS']):
            # Adds the herd member to the list
            betas.append(individuals[sorted_herd[i][0]])
            if i < params['NUMBER_OF_ALPHAS']:
                herd_index = sorted_herd[i][0]
                individuals[herd_index].isAlpha = True

    best_member = individuals[sorted_herd[0][0]]

    best_fitness = best_member.fitness

    return individuals, average_fitness, betas, best_fitness, best_member

