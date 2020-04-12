from PGEGrammar.grammar import Grammar
from socket import gethostname


hostname = gethostname().split('.')
machine_name = hostname[0]
import os
params = {

    'HERD_SIZE': 700, # Herd size
    'ITERATIONS' : 1, # Iterations/generations
    # GRAMMATICAL HERDING PARAMETERS
    'NUMBER_OF_BETAS': 40,
    'NUMBER_OF_ALPHAS': 10,

    'NUMBER_OF_CODONS' : 30,
    'CODON_SIZE' : 4, # The size of the codon.

    'TARGET_FITNESS' : 100,

    'GRAMMAR_FILE' : "grammars/letter.bnf", #BNF File path

    'MAX_TREE_DEPTH' : 6,
    'MAX_WRAPS' : 10,

    'SEED_INVIDIUALS' : [],
    # Fitness_function
    'FITNESS_FUNCTION': "string_match",
    # INITIALISATION.
    'TARGET' : 'Hello world!',
    # Set the maximum tree depth for initialisation.
    'MAX_INIT_TREE_DEPTH': 10,
    # Set the minimum tree depth for initialisation.
    'MIN_INIT_TREE_DEPTH': None,
    'PERMUTATION_RAMPS': 5,


}
def grammarFileInit():
    params['BNF'] = Grammar(os.path.join(params['GRAMMAR_FILE']))
