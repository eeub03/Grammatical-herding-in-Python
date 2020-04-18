import numpy as np

from src.parameters.parameters import params
from stats.statistics import stats

"""Based on Ponyge2's 'evaluation.py' but adapted to Grammatical herding. Added beta and alpha wandering instead of
 crossover and mutation All code below is my own"""
""" MAKE MORE EFFICIENT, MOST COMPILE TIME LOST TO MAPPING NEW GENOTYPES"""
betas = [0] * params['NUMBER_OF_BETAS']
alphas = [0] * params['NUMBER_OF_ALPHAS']
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



    fitness_herd = []
    invalids = 0
    for i in range(len(individuals)):
        ind = individuals[i]
        if ind.invalid:
            invalids += 1
        else:
            if ind.fitness > ind.best_fitness:
                ind.best_genotype_int = ind.genotype_int
                ind.best_phenotype = ind.phenotype
                ind.best_fitness = ind.fitness

        total_fitness += ind.best_fitness
        fitness_herd.append([i, ind.best_fitness])
        if stats['generation'] != 0:
            if ind.best_fitness <= stats['alpha_average']:
                random_alpha = set_beta(alphas)
                alpha = alphas[random_alpha]

                ind.change_genotype_to(alpha.best_genotype_int)

    # Stores the fitness of the herd member
    sorted_herd = []
    average_fitness = 0
    stats['number_of_invalids'].append(invalids)
    print(invalids)
    valids = len(individuals) - invalids

    if (valids <= 0):
        print("ALL individuals invalid")
        print(invalids)
    else:
        average_fitness = (total_fitness / params['HERD_SIZE'])

        alpha_fitness = 0

        stats['average_fitness'].append(average_fitness
                                        )
        sorted_herd = sorted(fitness_herd, key=lambda x:-x[1])

        if params['NUMBER_OF_ALPHAS'] >= params['NUMBER_OF_BETAS']:
            raise Exception('ERROR: Number of Alphas cannot be higher or equal to the number of Betas')
        else:
            if params['NUMBER_OF_BETAS'] > params['HERD_SIZE']:
                print("WARNING: Number of Betas is set to greater than population, setting Betas to population size - 1")
                params['NUMBER_OF_BETAS'] = params['HERD_SIZE'] - 1
            if params['NUMBER_OF_BETAS'] > valids:
                params['NUMBER_OF_BETAS'] = valids - 1
            if params['NUMBER_OF_ALPHAS'] >= params['NUMBER_OF_BETAS']:
                params['NUMBER_OF_ALPHAS'] = params['NUMBER_OF_BETAS'] - 1
                # Sets the individuals with the best fitness to Betas and Alphas
            for i in range(params['NUMBER_OF_BETAS']):

                # Adds the herd member to the

                betas[i] = individuals[sorted_herd[i][0]]

                if i < params['NUMBER_OF_ALPHAS'] - 1:
                    alpha = individuals[sorted_herd[i][0]]
                    alpha_fitness += alpha.best_fitness
                    alphas[i] = alpha

        alpha_fitness = alpha_fitness / params['NUMBER_OF_ALPHAS']

        stats['alpha_average'] = alpha_fitness

        i = 0
        print(average_fitness)
        # here we check each valid individuals fitness and use the betas to move them closer to higher areas of fitness
        for n in range(len(sorted_herd)):
            sorted_ind = individuals[sorted_herd[n][0]]

            rand_beta_index = set_beta(betas)
            random_beta = betas[rand_beta_index]
            while random_beta.invalid:
                random_beta_index = set_beta(betas)
                random_beta = betas[random_beta_index]

            beta = random_beta

            # CALCULATION FOR NEW FITNESS OF HERD MEMBER, using a random beta

            new_position = []
            for i in range(sorted_ind.no_of_codons):

                target_position = beta.best_genotype_int[i]
                current_position = sorted_ind.best_genotype_int[i]

                if current_position == None or target_position == None:
                    break

                if target_position > current_position:
                    range_p = target_position - current_position

                    new_position.append(
                        target_position - np.random.randint(range_p, dtype="uint64") + np.random.randint(0, range_p,
                                                                                                         dtype="uint64"),
                    )
                elif current_position > target_position:
                    range_p = current_position - target_position
                    new_position.append(
                        current_position - np.random.randint(range_p, dtype="uint64") + np.random.randint(range_p,
                                                                                                          dtype="uint64")
                    )
                    # We have an
                elif current_position == target_position:
                    wander = params['WANDER']
                    new_position.append(
                        current_position + np.random.randint(wander, dtype="uint64") - np.random.randint(wander,
                                                                                                         dtype="uint64")
                    )
                else:
                    print("WHAT")

            sorted_ind.change_genotype_to(new_position)



    """for i in range(len(alphas)):
            ind = alphas[i]

            new_position = []
            for n in range(ind.no_of_codons):
                current_position = ind.best_genotype_int[i]
                new_position.append(
                    current_position + np.random.randint(wander, dtype="uint64") - np.random.randint(wander,
                                                                                                     dtype="uint64")
                )
            ind.change_genotype_to(new_position)"""


    best_member = None

    best_fitness = None

    if invalids < params['HERD_SIZE']:

        best_member = individuals[sorted_herd[0][0]]

        best_fitness = best_member.fitness
        print(best_member.best_steps)


    return individuals, average_fitness, betas, best_fitness, best_member

def set_beta(betas):
    if len(betas) > 1:
        rand_beta_index = np.random.randint(0, len(betas) - 1)
    else:
        rand_beta_index = 0
    return rand_beta_index

