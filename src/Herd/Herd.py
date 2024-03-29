# -*- coding: utf-8 -*-


from Herd import Herd_Member
import parameters.parameters as par # imports the py file
from parameters.parameters import params # Imports the dict in the py file
from fitness.evaluation import evaluate_herd
from stats.statistics import stats


class Herd:
    """
    This is a class for a unique Herd that is run on a specified problem
    Attributes:
        herd (array): An array containing Herd_Member objects
        herd_size (int): The amount of Herd_member Objects to create.
        best_fitness (int): The amount of fitness that the best member of the current generation has achieved.
        best_member (Herd_Member): The Herd_Member with the best fitness of the current generation
        best_fitness_overall (int): The fitness of the Herd_member with the Best fitness so far in the run
        best_member_overall (Herd_Member): The Herd_member with the Best fitness so far in the run
        best_phenotype (String): The phenotype mapped from Mapper.py
        target_fitness: Optional Parameter for a target for the mapping.
    """
    def __init__(self):
        """
        Constructor for Herd Class
        """
        # Check parameters
        self.param_check()
        # Array of Herd members
        self.herd = []
        # Number of members to be created
        self.herd_size = params['HERD_SIZE']
        # Fitness value for the best member of this generation
        self.best_fitness = 0
        # The best member of the Herd of the current generation
        self.best_member = None
        # Best fitness of best herd member overall
        self.best_fitness_overall = 0
        # Best herd member overall
        self.best_member_overall = None
        # Best phenotype of the best member overall
        self.best_phenotype = None
        self.target_fitness = params['TARGET_FITNESS']

        par.grammarFileInit()
        for i in range(0, self.herd_size):
            # Creates Herd Members and stores them into an array
            self.herd.append(Herd_Member.Herd_Member(i))


    def evaluate_herd(self):
        """
        Function that puts the Herd through 'Evaluation.py' and stores the stats of the evaulation for the
        current generation
        """
        self.herd, self.average_fitness,  self.best_fitness, self.best_member \
            = evaluate_herd(self.herd)
        if stats['number_of_invalids'][stats['generation']] < params['HERD_SIZE']:

            if self.best_fitness_overall < self.best_fitness:
                self.best_fitness_overall = self.best_fitness
                self.best_member_overall = self.best_member
                self.best_phenotype = self.best_member.best_phenotype
                stats['best_fitness_iteration'] = stats['generation']
                stats['last_generation_improvement'] = stats['generation']
            elif self.best_fitness_overall == self.best_fitness:
                if self.best_member.best_steps < self.best_member_overall.best_steps:
                    self.best_fitness_overall = self.best_fitness
                    self.best_member_overall = self.best_member
                    self.best_phenotype = self.best_member.best_phenotype
                    self.best_member_overall.best_steps = self.best_member.best_steps
                    stats['last_generation_improvement'] = stats['generation']



    def start_evaluation(self):
        """
        Function that calls 'evaluate_herd' for the number of iterations specified
        Also stores the results of the entire run.
        """

        for i in range(params['ITERATIONS']):

            self.evaluate_herd()
            stats['generation'] += 1
            print("Generation: ")
            print(stats['generation'])
            stats['best_fitness_list'].append(self.best_fitness)
            if self.best_fitness == self.best_fitness_overall:

                stats['last_gen_improvement'] = stats['generation']



        stats['best_fitness'] = self.best_fitness_overall
        stats['best_phenotype'] = self.best_phenotype
        stats['average_fitness'] = self.average_fitness
        stats['best_steps'] = self.best_member_overall.best_steps


    # Error checking the parameters so input is of the right type
    def param_check(self):
        if type(params['HERD_SIZE']) != int:
            raise Exception("Paramater Error: 'HERD_SIZE' is not of type 'int'")
        if type(params['ITERATIONS']) != int:
            raise Exception("Paramater Error: 'ITERATIONS' is not of type 'int'")
        if type(params['NUMBER_OF_ALPHAS']) != int:
            raise Exception("Paramater Error: 'NUMBER_OF_ALPHAS' is not of type 'int'")
        if type(params['NUMBER_OF_BETAS']) != int:
            raise Exception("Paramater Error: 'NUMBER_OF_BETAS' is not of type 'int'")
        if type(params['WANDER']) != int:
            raise Exception("Paramater Error: 'WANDER' is not of type 'int'")
        if type(params['NUMBER_OF_CODONS']) != int:
            raise Exception("Paramater Error: 'NUMBER_OF_CODONS' is not of type 'int'")
        if type(params['CODON_SIZE']) != int:
            raise Exception("Paramater Error: 'CODON_SIZE' is not of type 'int'")
        if type(params['GRAMMAR_FILE']) != str:
            raise Exception("Paramater Error: 'GRAMMAR_FILE' is not of type 'str'")
        if type(params['MAX_TREE_DEPTH']) != int and params['MAX_TREE_DEPTH'] != None:
            raise Exception("Paramater Error: 'MAX_TREE_DEPTH is not of type 'int' or 'None'")
        if type(params['MAX_WRAPS']) != int:
            raise Exception("Paramater Error: 'MAX_WRAPS' is not of type 'int'")
        if type(params['MULTICORE']) != bool:
            raise Exception("Paramater Error: 'MULTICORE' is not of type 'bool'")
        if type(params['FITNESS_FUNCTION']) != str:
            raise Exception("Paramater Error: 'FITNESS_FUNCTION' is not of type 'str'")
        if type(params['TARGET']) != str and params['TARGET'] != None:
            raise Exception("Paramater Error: 'TARGET' is not of type 'str' or 'None'")
        if type(params['MIN_INIT_TREE_DEPTH']) != int and params['MIN_INIT_TREE_DEPTH'] != None:
            raise Exception("Paramater Error: 'MIN_INIT_TREE_DEPTH' is not of type 'int' or 'None'")
        if type(params['MAX_INIT_TREE_DEPTH']) != int:
            raise Exception("Paramater Error: 'MAX_INIT_TREE_DEPTH' is not of type 'int'")
        if type(params['PERMUTATION_RAMPS']) != int:
            raise Exception("Paramater Error: 'PERMUTATION_RAMPS' is not of type 'int'")
        if 'MAX_STEPS' in params:
            if type(params['MAX_STEPS']) != int:
                raise Exception("Paramater Error: 'MAX_STEPS' is not of type 'int'")