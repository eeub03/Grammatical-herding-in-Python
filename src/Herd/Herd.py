# -*- coding: utf-8 -*-


from src.Herd import Herd_Member
import src.parameters.parameters as par # imports the py file
from src.parameters.parameters import params # Imports the dict in the py file
from src.fitness.evaluation import evaluate_herd
from stats.statistics import stats


class Herd:
    def __init__(self):
        self.herd = []
        self.iterations = 1
        self.herd_Size = params['HERD_SIZE']
        self.BNF_Path = ""
        self.herd_Fitness = []
        self.herd_evaluated = []
        self.average_Fitness = 0
        self.betas = []
        self.best_fitness = 0
        self.best_member = None
        self.best_fitness_overall = 0
        self.best_member_overall = None
        self.best_phenotype = None
        self.target_fitness = params['TARGET_FITNESS']
        par.grammarFileInit()
        for i in range(0, self.herd_Size):
            # Sets our grammar file from the file path of the bnf
            self.herd.append(Herd_Member.HerdMember(i))

    def evaluate_herd(self):
        self.herd, self.average_Fitness, self.betas, self.best_fitness, self.best_member \
            = evaluate_herd(self.herd)
        if stats['number_of_invalids'][stats['generation']] < params['HERD_SIZE']:

            if self.best_fitness_overall < self.best_fitness:
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
                stats['best_fitness'] = self.best_fitness_overall
                stats['last_gen_improvement'] = stats['generation']
                stats['best_phenotype'] = self.best_phenotype
            if self.target_fitness is not None and self.target_fitness <= self.best_fitness:
                break

    def evaluate_herd_once(self):
        last_fitness = self.best_fitness
        stats['generation'] += 1
        self.evaluate_herd()


        if last_fitness < self.best_fitness:

            stats['last_gen_improvement'] = stats['generation']
            stats['best_phenotype'] = self.best_phenotype





