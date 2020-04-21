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
    :return
    """

    results, pool = [], None

    if params['MULTICORE']:
        pool = params['POOL']
    total_fitness = 0

    fitness_herd = []
    herd = []
    invalids = 0
    normal_herd = 0
    total_herd_fitness = 0
    if params['BATCH'] == True:
        import importlib
        module = importlib.import_module('src.fitness.' + params['FITNESS_FUNCTION'])
        fitness_class = getattr(module, params['FITNESS_FUNCTION'])
        fitness_herd = fitness_class(individuals)
        for i in range(len(individuals)):
            individuals[i].fitness = fitness_herd[i]

    if stats['generation'] != 0:
        print(stats['average_fitness'][stats['generation'] - 1])
    for i in range(len(individuals)):
        ind = individuals[i]
        if ind.invalid:
            invalids += 1
        else:
            ind.fitness = 0
            ind.get_fitness()
            if ind.fitness > ind.best_fitness:
                ind.best_genotype_int = ind.genotype_int
                ind.best_phenotype = ind.phenotype
                ind.best_fitness = ind.fitness



        if stats['generation'] != 0:

            #if ind.best_fitness <= stats['average_herd_fitness'][stats['generation'] - 1]:
            if ind.best_fitness <= stats['herd_movement']:
                random_alpha = set_beta(alphas)
                alpha = alphas[random_alpha]

                ind.best_genotype_int = alpha.best_genotype_int


        total_fitness += ind.best_fitness
        herd.append([i, ind.fitness])
        fitness_herd.append([i, ind.best_fitness])


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


        stats['average_fitness'].append(average_fitness
                                        )
        sorted_herd = sorted(fitness_herd, key=lambda x:-x[1])
        sorted_herd_fitness = sorted(herd, key=lambda x: -x[1])

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
                stats['herd_movement'] += betas[i].best_fitness
                if i < params['NUMBER_OF_ALPHAS'] - 1:
                    alpha = individuals[sorted_herd[i][0]]

                    alphas[i] = alpha
        best_member = None

        best_fitness = None
        print(invalids)
        if invalids < params['HERD_SIZE']:
            best_member = individuals[sorted_herd[0][0]]

            best_fitness = best_member.best_fitness
            print("Best")
            print(best_member.best_fitness)
            print(best_member.best_steps)
            print(sorted_herd_fitness[0][1])
        i = 0
        wandering = 0
        # here we check each valid individuals fitness and use the betas to move them closer to higher areas of fitness
        for n in range(len(individuals)):
            sorted_ind = individuals[n]
            if n > params['NUMBER_OF_BETAS']:
                normal_herd += 1
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

                elif current_position == target_position:


                    wander = params['WANDER']
                    new_position.append(
                        current_position + np.random.randint(wander, dtype="uint64") - np.random.randint(wander,
                                                                                                         dtype="uint64")
                    )


            key = get_geno_key(None, new_position)
            if key in geno_int_cache:
                sorted_ind.genotype_int = new_position
                sorted_ind.phenotype = geno_int_cache[key]
                sorted_ind.fitness = pheno_cache[sorted_ind.phenotype]
                print("FOUND")
            else:
                results = eval_or_append(sorted_ind, results, pool, new_position)
            if params['MULTICORE'] == False:
                individuals[n] = sorted_ind
    if params['MULTICORE']:
        for result in results:
            print(result)
            sorted_ind = result.get()

            individuals[sorted_ind.index] = sorted_ind
    average_fitness_herd = (total_herd_fitness / normal_herd)

    stats['average_herd_fitness'].append(average_fitness_herd)
    stats['best_iteration_fitness'] = sorted_herd_fitness[0][1]

    return individuals, average_fitness, best_fitness, best_member

def eval_or_append(ind, results, pool, new_position):
    if params['MULTICORE']:

        results.append(pool.apply_async(ind.change_genotype_to, ([new_position])))
        return results
    else:
        ind.change_genotype_to(new_position)


def set_beta(betas):
    if len(betas) > 1:
        rand_beta_index = np.random.randint(0, len(betas) - 1)
    else:
        rand_beta_index = 0
    return rand_beta_index

