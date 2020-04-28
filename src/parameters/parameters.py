from PGEGrammar.grammar import Grammar
from socket import gethostname

from multiprocessing import cpu_count
hostname = gethostname().split('.')
machine_name = hostname[0]
import os
"""
    Dictionary containing the parameters for a run of grammatical Herding
    attributes:
        HERD_SIZE (int): Number of Herd Members to create
        ITERATIONS (int): Number of times to move herd members and evaluate them
        NUMBER_OF_BETAS (int): amount of Beta's in the run
        NUMBER_OF_ALPHAS(int): Amount of Alpha's in the run 
        WANDER (int): The range wandering allowed for the alphas
        NUMBER_OF_CODONS (int): Amount of codons that the members can use
        CODON_SIZE (int): size of codon in bits
        TARGET_FITNESS (float): Optional target for fitness
        GRAMMAR_FILE (string): Path of grammar file
        MAX_TREE_DEPTH (int): Max depth that the grammar tree can reach
        MAX_WRAPS (int): Max number of wraps that can occur in mapping
        MULTICORE (Boolean): Option for multicore processing, Not implemented yet
        CORES (int): number of cores to use with multiprocessing
        SEED_INDIVIDUALS (arrays): Array of individuals for seeding
        FITNESS_FUNCTION (string): Path of fitness function to evaluate members with
        TARGET (object): A target for individuals to compare to for fitness
        MAX_INIT_TREE_DEPTH (int): Maximum initial depth of the grammar tree
        MIN_INIT_TREE_DEPTH (int): minimum intiial depth of the grammar tree
        PERMUTATION_RAMPS (int): Number of depths to analyse for Grammar
        MAX_STEPS (int): Max steps of an Ant in santa fe
    """
params = {

    'HERD_SIZE': 700, # Herd size
    'ITERATIONS' : 5, # Iterations/generations
    # GRAMMATICAL HERDING PARAMETERS
    'NUMBER_OF_BETAS': 20,
    'NUMBER_OF_ALPHAS': 5,
    'WANDER': 10,

    'NUMBER_OF_CODONS' : 20,
    'CODON_SIZE' : 8, # The size of the codon.

    'TARGET_FITNESS' : 100,

    'GRAMMAR_FILE' : "grammars/SFT2.pybnf", #BNF File path

    'MAX_TREE_DEPTH' : None,
    'MAX_WRAPS' : 10,
    'MULTICORE' : False,
    'CORES' : cpu_count(),

    'SEED_INDIVIDUALS' : [],
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

