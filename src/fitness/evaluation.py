import numpy as np

from src.mapping.Key_Gen import get_geno_key
from src.parameters.parameters import params
from stats.statistics import geno_int_cache
from stats.statistics import pheno_cache
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

    """
    # Variables for future Multi-processing
    results, pool = [], None
    # NEEDS TO BE IMPLEMENTED, CAN BE IGNORED
    if params['MULTICORE']:
        pool = params['POOL']
    # Total fitness used to calculate average fitness of the Herd
    total_fitness = 0
    # Herd, sorted by their personal best fitness.
    fitness_herd = []

    # Number of invalids
    invalids = 0
    # Reset Alpha average fitness for current generation
    stats['herd_movement'] = 0
    total_herd_fitness = 0

    if stats['generation'] != 0:
        print("Average Fitness")
        print(stats['average_fitness'][stats['generation'] - 1])
    for i in range(len(individuals)):
        ind = individuals[i]
        if ind.invalid:
            invalids += 1
        else:
            ind.fitness = 0
            # Calculate the fitness of the individual at its current location
            ind.get_fitness()
            # If it is greater than it's know best_fitness we set its new personal bests
            if ind.fitness > ind.best_fitness:
                ind.best_genotype_int = ind.genotype_int
                ind.best_phenotype = ind.phenotype
                ind.best_fitness = ind.fitness
            if ind.fitness == ind.best_fitness:
                if ind.steps < ind.best_steps:
                    ind.best_steps = ind.steps
                    ind.best_phenotype = ind.phenotype
                    ind.best_genotype_int = ind.genotype_int

        if stats['generation'] != 0:

            # We move low fitness individuals to an Alpha's position.
            # Note: we do not calculate its fitness, we only make it aware of the best position of the herd
            if ind.best_fitness <= stats['alphas_fitness'][stats['generation' ] - 1]:
                random_alpha = set_beta(alphas)
                alpha = alphas[random_alpha]
                ind.best_genotype_int = alpha.best_genotype_int
                ind.invalid = False

        # Add the members fitness to the total fitness
        total_fitness += ind.best_fitness
        # Add the member to the herd
        fitness_herd.append([i, ind.best_fitness])

    # The current average best fitness
    average_fitness = 0

    stats['number_of_invalids'].append(invalids)
    print("INVALIDS")
    print(invalids)
    # Check to see how many valids we have
    valids = len(individuals) - invalids

    if (valids <= 0):
        print("ALL individuals invalid")
        print(invalids)
    else:
        average_fitness = (total_fitness / params['HERD_SIZE'])

        # Sets the average fitness of the Herd at this generation
        stats['average_fitness'].append(average_fitness)
        # Array of the Herd sorted by their personal best fitness
        sorted_herd = sorted(fitness_herd, key=lambda x: -x[1])

        if params['NUMBER_OF_ALPHAS'] >= params['NUMBER_OF_BETAS']:
            raise Exception('ERROR: Number of Alphas cannot be higher or equal to the number of Betas')
        else:
            # Checking to see if parameters are correctly set
            if params['NUMBER_OF_BETAS'] > params['HERD_SIZE']:
                raise Exception("WARNING: Number of Betas is set to greater than population")
            if params['NUMBER_OF_BETAS'] > valids:
                raise Exception('ERROR Number of Betas is greater than valid individuals, change parameter settings')
                # Sets the individuals with the best fitness to Betas and Alphas
            for i in range(params['NUMBER_OF_BETAS']):

                # Adds the herd member to the
                betas[i] = individuals[sorted_herd[i][0]]
                # This stat is checked to move low fitness members towards an alpha's position

                if i < params['NUMBER_OF_ALPHAS']:
                    alpha = individuals[sorted_herd[i][0]]
                    stats['herd_movement'] += betas[i].best_fitness
                    alphas[i] = alpha

        # Set average alpha fitness for weak herd members
        stats['alphas_fitness'].append((stats['herd_movement']) / params['NUMBER_OF_ALPHAS'])

        best_member = None
        best_fitness = None

        if invalids < params['HERD_SIZE']:
            best_member = individuals[sorted_herd[0][0]]
            best_fitness = best_member.best_fitness

            print("Best Fitness")
            print(best_member.best_fitness)
            print("best steps")
            print(best_member.best_steps)


        # here we check each valid individuals fitness and use the betas to move them closer to higher areas of fitness
        for n in range(len(individuals)):
            sorted_ind = individuals[n]
            if sorted_ind.invalid == False:
                if n > params['NUMBER_OF_BETAS']:
                    total_herd_fitness += sorted_ind.best_fitness
                rand_beta_index = set_beta(betas)
                random_beta = betas[rand_beta_index]

                beta = random_beta

                # CALCULATION FOR NEW FITNESS OF HERD MEMBER, using a random beta

                new_position = []
                for i in range(sorted_ind.no_of_codons):
                    # Best position of beta
                    target_position = beta.best_genotype_int[i]
                    # Best position of current herd member
                    current_position = sorted_ind.best_genotype_int[i]
                    # If target_position coordinate is greater
                    if target_position > current_position:
                        range_p = target_position - current_position
                        new_position.append(
                            target_position - np.random.randint(range_p, dtype="uint64") + np.random.randint(0, range_p,
                                                                                                             dtype="uint64"),
                        )
                    # If current_position coordinate is greater
                    elif current_position > target_position:
                        range_p = current_position - target_position
                        new_position.append(
                            current_position - np.random.randint(range_p, dtype="uint64") + np.random.randint(range_p,
                                                                                                              dtype="uint64")
                        )
                    # If they are equal, we have an alpha who needs to wander the search space
                    elif current_position == target_position:
                        wander = params['WANDER']
                        new_position.append(
                            current_position + np.random.randint(wander, dtype="uint64") - np.random.randint(wander,
                                                                                                             dtype="uint64")
                        )

                # Check if solution has been found and if so we don't need to map a new genotype
                key = get_geno_key(None, new_position)
                if key in geno_int_cache:
                    sorted_ind.genotype_int = new_position
                    sorted_ind.phenotype = geno_int_cache[key]
                    sorted_ind.fitness = pheno_cache[sorted_ind.phenotype]
                else:
                    # Else we need to map the new position
                    results = eval_or_append(sorted_ind, results, pool, new_position)
                if params['MULTICORE'] == False:
                    individuals[n] = sorted_ind

    if params['MULTICORE']:
        for result in results:
            print(result)
            sorted_ind = result.get()

            individuals[sorted_ind.index] = sorted_ind

    return individuals, average_fitness, best_fitness, best_member


def eval_or_append(ind, results, pool, new_position):
    # IGNORE, FOR MULTI PROCESSING TO SPEED UP ALGORITHM
    if params['MULTICORE']:
        results.append(pool.apply_async(ind.change_genotype_to, ([new_position])))
        return results
    else:
        # Changes current position of Herd Member in search space
        ind.change_genotype_to(new_position)


# Function that returns an index based on a list.
def set_beta(betas):
    if len(betas) > 1:
        rand_beta_index = np.random.randint(0, len(betas) - 1)
    else:
        rand_beta_index = 0
    return rand_beta_index
