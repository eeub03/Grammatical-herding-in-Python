from PGEGrammar.grammar import Grammar
from socket import gethostname


hostname = gethostname().split('.')
machine_name = hostname[0]
import os
params = {

    'HERD_SIZE': 700, # Herd size
    'ITERATIONS' : 500, # Iterations/generations
    # GRAMMATICAL HERDING PARAMETERS
    'NUMBER_OF_BETAS': 40,
    'NUMBER_OF_ALPHAS': 10,
    'WANDER': 10,

    'NUMBER_OF_CODONS' : 20,
    'CODON_SIZE' : 8, # The size of the codon.

    'TARGET_FITNESS' : 100,

    'GRAMMAR_FILE' : "grammars/SFT.pybnf", #BNF File path

    'MAX_TREE_DEPTH' : 0,
    'MAX_WRAPS' : 30,

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

}
def grammarFileInit():

    params['BNF'] = Grammar(os.path.join("C:/Users/Joe/Documents/3 YEAR PROJECT IMPORTANT/code/src",params['GRAMMAR_FILE']))

