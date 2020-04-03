from PGEGrammar.grammar import Grammar
import os
params = {

    'HERD_SIZE': 4, # Herd size
    'ITERATIONS' : 1, # Iterations/generations
    'HILL_CLIMBING_HISTORY' : 500, # Hill climbing history
    'SCHC_COUNT_METHOD': "count_all", # SCHC Counting method
    'ITERATIONS' : 1,# Number of runs
      # Fitness_function

    'CODON_MIN' : 20, # Min_Codon min number of codons
    'CODON_MAX' : 20, # Max_Codon max number of codons
    'CODON_SIZE' : 8, # Size_Codon size of codon
    'NO_OF_CODONS' : 0, # Number of codons set by program

    'GRAMMAR_FILE' : "grammars/letter.bnf", #BNF File path

    'MAX_TREE_DEPTH' : 90,
    'MAX_WRAPS' : 0,

    'SEED_INVIDIUALS' : [],
    'FITNESS_FUNCTION' : 'fitness/string_match.py',
    # INITIALISATION
    # Set initialisation operator.

    # Set the maximum geneome length for initialisation.

    # Set the maximum tree depth for initialisation.
    'MAX_INIT_TREE_DEPTH': 10,
    # Set the minimum tree depth for initialisation.
    'MIN_INIT_TREE_DEPTH': None,
    'PERMUTATION_RAMPS': 5,

}
def grammarFileInit():
    params['BNF'] = Grammar(os.path.join(params['GRAMMAR_FILE']))
