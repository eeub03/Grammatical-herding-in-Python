# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:28:49 2019

@author: Joseph Morgan
@name: Grammatical Herding in Python
@version: 0.1a
"""

from src.Herd import Herd_Individual
from src.parameters.parameters import params
from src.parameters import parameters as par
from src.fitness.evaluation import evaluate_herd

import numpy as np


class Herd:
    def __init__(self):
        self.herd = []

        self.iterations = 1
        self.herd_Size = params['HERD_SIZE']
        self.BNF_Path = ""
        self.herd_Fitness = []
        self.codon_Min = 0
        self.codon_Max = 0
        self.codon_Size = 0
        self. max_Iterations = 0


        par.grammarFileInit()
        for i in range(0, self.herd_Size):
            # Sets our grammar file from the file path of the bnf
            self.herd.append(Herd_Individual.HerdMember(i))

    def evaluateHerd(self):
        self.herd_evaluated, self.average_Fitness, self.betas, self.best_fitness, self.best_member \
            = evaluate_herd(self.herd)
        self.best_phenotype = self.best_member.phenotype

Herd1 = Herd()
Herd1.evaluateHerd()
for i in range(Herd1.herd_Size):
    print(Herd1.herd[i].phenotype)
