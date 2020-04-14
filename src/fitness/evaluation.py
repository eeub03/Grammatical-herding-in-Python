from src.parameters.parameters import params
import numpy as np
from stats.statistics import stats
"""Based on Ponyge2's 'evaluation.py' but adapted to Grammatical herding. Added beta and alpha wandering instead of
 crossover and mutation All code below is my own"""

def takeSecond(elem):
    return elem[1]
def evaluate_herd(individuals):
    """
    Evaluate an entire population of individuals for invalid individuals. Invalid individuals are given
    a default bad fitness.
    :param individuals: A population of individuals to be evaluated.
    :return
    """
    total_fitness = 0
    betas = [0] * params['NUMBER_OF_BETAS']
    alphas = [0] * params['NUMBER_OF_ALPHAS']


    fitness_herd = [[0, 0]] * len(individuals)

    for i in range(len(individuals)):
        ind = individuals[i]
        if ind.invalid:
            stats['number_of_invalids'] += 1
        else:
            total_fitness += ind.fitness
            # Stores the index from Individuals for this herd member
            fitness_herd[i][0] = i
            fitness_herd[i][1] = ind.fitness

            # Stores the fitness of the herd member
    sorted_herd = []
    average_fitness = 0
    valids = len(individuals) - stats['number_of_invalids']
    if (valids <= 0):
        print("ALL individuals invalid")
        print(stats['number_of_invalids'])
    else:
        average_fitness = (total_fitness / valids)
        print(fitness_herd)
        sorted_herd = sorted(fitness_herd, key=lambda x:-x[1])

        if params['NUMBER_OF_ALPHAS'] >= params['NUMBER_OF_BETAS']:
            raise Exception('ERROR: Number of Alphas cannot be higher or equal to the number of Betas')
        else:
            if params['NUMBER_OF_BETAS'] > params['HERD_SIZE']:
                print("WARNING: Number of Betas is set to greater than population, setting Betas to population size - 1")
                params['NUMBER_OF_BETAS'] = params['HERD_SIZE'] - 1
            if params['NUMBER_OF_BETAS'] > stats['number_of_invalids']:
                params['NUMBER_OF_BETAS'] = valids - 1
                params['NUMBER_OF_ALPHAS'] = params['NUMBER_OF_BETAS'] - 1
                # Sets the individuals with the best fitness to Betas and Alphas
                for i in range(params['NUMBER_OF_BETAS']):
                    # Adds the herd member to the list
                    betas[i] = individuals[sorted_herd[i][0]]
                    if i < params['NUMBER_OF_ALPHAS']:
                        herd_index = sorted_herd[i][0]
                        alphas[i] = individuals[sorted_herd[i][0]]


        # here we check each valid individuals fitness and use the betas to move them closer to higher areas of fitness
        for n in range(len(sorted_herd)):

            ind = individuals[sorted_herd[n][0]]

            if not ind.invalid:
                if params['NUMBER_OF_BETAS'] > 1:
                    rand_beta_index = np.random.randint(0, len(betas) - 1)
                else:
                    rand_beta_index = 0

                random_beta = betas[rand_beta_index]
                beta = individuals[random_beta]


                # CALCULATION FOR NEW FITNESS OF HERD MEMBER, using a random beta
                new_position = [0]*ind.no_of_codons
                for i in range(ind.no_of_codons):

                    target_position = beta.genotype_int[i]
                    current_position = ind.genotype_int[i]
                    if current_position == None or target_position == None:
                        break


                    if target_position > current_position:
                        range_p = target_position - current_position

                        new_position.append(target_position - np.random.randint(0, range_p, dtype="uint64") + np.random.randint(0, range_p,dtype="uint64"),)
                    elif current_position > target_position:
                        range_p = current_position - target_position
                        new_position.append(current_position - np.random.randint(range_p, dtype="uint64") + np.random.randint(range_p,dtype="uint64"))
                    # We have an alpha
                    else:
                        wander_range = params['WANDER']

                        new_position.append(current_position + np.random.randint(0, wander_range,dtype="uint64") - np.random.randint(0, wander_range,dtype="uint64"))
                ind.change_genotype_to(None, new_position)

    best_member = None

    best_fitness = None

    if stats['number_of_invalids'] < params['HERD_SIZE']:

        best_member = individuals[sorted_herd[0][0]]

        best_fitness = best_member.fitness

    return individuals, average_fitness, betas, best_fitness, best_member

