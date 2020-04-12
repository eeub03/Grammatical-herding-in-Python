from src.parameters.parameters import params
import numpy as np

import src.mapping.Mapper as mp
from stats.statistics import stats
"""Based on Ponyge2's 'evaluation.py'  """

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
            fitness_herd[i] = [i, ind.fitness]
            # Stores the fitness of the herd member


    average_fitness = (total_fitness / (len(individuals) - stats['number_of_invalids']))

    sorted_herd = sorted(fitness_herd, key=lambda x:-x[1])

    if params['NUMBER_OF_ALPHAS'] >= params['NUMBER_OF_BETAS']:
        raise Exception('ERROR: Number of Alphas cannot be higher or equal to the number of Betas')
    else:
        if params['NUMBER_OF_BETAS'] > params['HERD_SIZE']:
            print("WARNING: Number of Betas is set to greater than population, setting Betas to population size - 1")
            params['NUMBER_OF_BETAS'] = params['HERD_SIZE'] - 1
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
            list_b = [str(x) for x in random_beta.genotype_int]


            # CALCULATION FOR NEW FITNESS OF HERD MEMBER, using a random beta
            new_position = [0]*ind.no_of_codons
            for i in range(ind.no_of_codons):

                target_position = random_beta.genotype_int[i]
                current_position = ind.genotype_int[i]
                if current_position == None or target_position == None:
                    break
                print(len(str(ind.genotype_int[i])))

                if target_position > current_position:
                    range_p = target_position - current_position
                    print(type(range_p))
                    new_position.append(target_position - np.random.randint(0, range_p, dtype="uint64") + np.random.randint(0, range_p,dtype="uint64"),)
                elif current_position > target_position:
                    range_p = current_position - target_position
                    new_position.append(current_position - np.random.randint(range_p, dtype="uint64") + np.random.randint(range_p,dtype="uint64"))
                # We have an alpha
                else:
                    wander = str((np.random.randint(0, 2, params['CODON_SIZE'])))
                    # Formatting for our bitstring to make allow it to be read for conversion into int
                    wander = wander.replace('[', '')
                    wander = wander.replace(']', '')
                    wander = wander.replace('\n', '')
                    wander = wander.replace(' ', '')
                    wander_range = int(wander,2) + 1
                    print(wander_range)

                    new_position.append(current_position + np.random.randint(0, wander_range,dtype="uint64") - np.random.randint(0, wander_range,dtype="uint64"))
            ind.change_genotype_to(None, new_position)








    best_member = individuals[sorted_herd[0][0]]

    best_fitness = best_member.fitness

    return individuals, average_fitness, betas, best_fitness, best_member

