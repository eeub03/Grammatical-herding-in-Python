from PGEGrammar.grammar import Grammar
from socket import gethostname


hostname = gethostname().split('.')
machine_name = hostname[0]
import os
params = {

    'HERD_SIZE': 40, # Herd size
    'ITERATIONS' : 1, # Iterations/generations
    'HILL_CLIMBING_HISTORY' : 500, # Hill climbing history
    'SCHC_COUNT_METHOD': "count_all", # SCHC Counting method
    'ITERATIONS' : 1,# Number of runs


    'CODON_MIN' : 1, # Min_Codon min number of codons
    'CODON_MAX' : 500, # Max_Codon max number of codons
    'CODON_SIZE' : 1000, # Size_Codon size of codon



    'GRAMMAR_FILE' : "grammars/letter.bnf", #BNF File path

    'MAX_TREE_DEPTH' : 17,
    'MAX_WRAPS' : 0,

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

    # GRAMMATICAL HERDING PARAMETERS
    'NUMBER_OF_BETAS' : 10,
    'NUMBER_OF_ALPHAS' : 2
}
def grammarFileInit():
    params['BNF'] = Grammar(os.path.join(params['GRAMMAR_FILE']))
