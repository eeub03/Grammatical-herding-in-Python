# -*- coding: utf-8 -*-


from src.Herd import Herd_Member
import src.parameters.parameters as par # imports the py file
from src.parameters.parameters import params # Imports the dict in the py file
from src.fitness.evaluation import evaluate_herd
from stats.statistics import stats


class Herd:
    def __init__(self):
        # Array of Herd members
        self.herd = []
        # Number of members to be created
        self.herd_Size = params['HERD_SIZE']
        # Fitness value for the best member
        self.best_fitness = 0
        # The best member of the Herd
        self.best_member = None

        self.best_fitness_overall = 0
        self.best_member_overall = None
        self.best_phenotype = None
        self.target_fitness = params['TARGET_FITNESS']
        par.grammarFileInit()
        for i in range(0, self.herd_Size):
            # Sets our grammar file from the file path of the bnf
            self.herd.append(Herd_Member.Herd_Member(i))
        if params['BATCH'] == True:
            import importlib
            module = importlib.import_module('src.fitness.' + params['FITNESS_FUNCTION'])
            fitness_class = getattr(module, params['FITNESS_FUNCTION'])
            fitness_herd = fitness_class(self.herd)
            for i in range(len(self.herd)):
                self.herd[i].fitness = fitness_herd[i]

    def evaluate_herd(self):
        self.herd, self.average_fitness,  self.best_fitness, self.best_member \
            = evaluate_herd(self.herd)
        if stats['number_of_invalids'][stats['generation']] < params['HERD_SIZE']:

            if self.best_fitness_overall < self.best_fitness:
                self.best_fitness_overall = self.best_fitness
                self.best_member_overall = self.best_member
                self.best_phenotype = self.best_member.phenotype
            elif self.best_fitness_overall == self.best_fitness:
                if self.best_member.best_steps < self.best_member_overall.best_steps:
                    self.best_fitness_overall = self.best_fitness
                    self.best_member_overall = self.best_member
                    self.best_phenotype = self.best_member.phenotype



    def start_evaluation(self):


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
        stats


