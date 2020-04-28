import json
from datetime import datetime

"""
 Attributes:
     generation (int): The current generation of the run
     best_fitness_list (array): List of the best fitness of each generation. Index is correlated to the generation.
     number_of_invalids (array): Stores array of invalids. Index is correlated to generation.
     best_fitness (int): Best fitness found by the Herd
     best_iteration_fitness (int): Generation where first full solution was found
     last_gen_improvement (int): Generation where the fitness stopped improving
     best_phenotype (string): Best phenotype of the best solution found by the run
     best_steps (int): Best steps of the best phenotype found by the run.
     average_fitness (array): Average fitness of the herd per generation. Index correlates to generation
     herd_movement (float): Total fitness of the betas
 """
stats = {

    "generation" : 0,
    "best_fitness_list": [],
    "number_of_invalids" : [],
    "best_fitness" : 0,
    "best_iteration_fitness": 0,
    "last_gen_improvement" : 0,
    "best_phenotype" : "",
    "best_steps" : 0,
    "average_fitness": [],
    "herd_movement": 0,

}
geno_int_cache = {}
pheno_cache = {}
# Saves the stats of the run with it's own time frame
def save():
    file_str = str(datetime.today()).replace(" ","-").replace(".","-").replace(":","-")
    filename = "stats-logs/stats-run-" + file_str + ".txt"
    with open(filename, "w") as f:
        json.dump(stats, f, sort_keys=True, indent= 4)