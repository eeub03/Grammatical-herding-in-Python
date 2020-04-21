import json
stats = {
    "generation" : 0,
    "best_fitness_list": [],
    "population" : 0,
    "number_of_invalids" : [],
    "best_fitness" : 0,
    "last_gen_improvement" : 0,
    "best_phenotype" : "",
    "invalids": [],
    "best_steps" : 0,
    "average_steps" : 0,
    "average_fitness": [],
    "average_herd_fitness": [],
    "beta_fitness": 0,
    "herd_movement": 0,
    "best_iteration_fitness": 0,
}
geno_int_cache = {}
pheno_cache = {}
def save():
    with open("stats.txt", "w") as f:
        json.dump(stats, f, sort_keys=True, indent= 4)