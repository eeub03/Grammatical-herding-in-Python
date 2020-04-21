from PGEGrammar.grammar import Grammar
from socket import gethostname

from multiprocessing import cpu_count
hostname = gethostname().split('.')
machine_name = hostname[0]
import os
params = {

    'HERD_SIZE': 1000, # Herd size
    'ITERATIONS' : 400, # Iterations/generations
    # GRAMMATICAL HERDING PARAMETERS
    'NUMBER_OF_BETAS': 20,
    'NUMBER_OF_ALPHAS': 3,
    'WANDER': 10,

    'NUMBER_OF_CODONS' : 30,
    'CODON_SIZE' : 4, # The size of the codon.

    'TARGET_FITNESS' : 100,

    'GRAMMAR_FILE' : "grammars/SFT3.pybnf", #BNF File path

    'MAX_TREE_DEPTH' : None,
    'MAX_WRAPS' : 10,
    'MULTICORE' : False,
    'CORES' : cpu_count(),

    'SEED_INVIDIUALS' : [],
    # Fitness_function
    'FITNESS_FUNCTION': "sft",
    # INITIALISATION.
    'TARGET' : 'Hello world!',
    # Set the maximum tree depth for initialisation.
    'MAX_INIT_TREE_DEPTH': 10,
    # Set the minimum tree depth for initialisation.
    'MIN_INIT_TREE_DEPTH': None,
    'PERMUTATION_RAMPS': 5,

    # Santa Fe Trail params
    'MAX_STEPS' : 900,

    # MESA Settings
    'BATCH' : False,
}
def grammarFileInit():

    params['BNF'] = Grammar(os.path.join("C:/Users/Joe/Documents/3 YEAR PROJECT IMPORTANT/code/src",params['GRAMMAR_FILE']))

