# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:28:49 2019

@author: Joseph Morgan
@name: Grammatical Herding in Python
@version: 0.1a
"""

from src import Herd_Individual
from parameters import parameters as par
import numpy as np
from PGEGrammar.grammar import Grammar
import os
import sys
herd = []
sort_Herd = []
iterations = 1
average_Fitness = 0.0
herd_Size = 0
BNF_Path = ""

codon_Min = 0
codon_Max = 0
codon_Size = 0
max_Iterations = 0

def initialiseHerd():
    for i in range(0, par.params['HERD_SIZE']):
        print("Running")
        # Sets our grammar file from the file path of the bnf
        par.grammarFileInit()

        minMaxCodon = 0
        codon_Min = par.params['CODON_MIN']
        codon_Max = par.params['CODON_MAX']
        # Creates codonSize many bitstring codons of pre defined codon size
        if codon_Max < 0 or codon_Min < 0:
            if codon_Min  != codon_Max:
                minMaxCodon = np.random.randint(codon_Min  + 2, codon_Max + 2)
            else:
                minMaxCodon = np.random.randint(codon_Max + 2)
        par.params['NO_OF_CODONS'] = minMaxCodon
        herd.append(Herd_Individual.HerdMember(i))

def getAvgFitness():
    avg_Fitness = 0
    for i in range(herd_Size):

        avg_Fitness = avg_Fitness + herd[i].getFitness()

def evaluateHerd():
    itera = 0
    while itera < max_Iterations:
        itera = itera + 1

def getCodonMax():
    # Returns the current herds Codon max size
    return codon_Max

def getCodonMin():
    return codon_Min

def getCodonSize():
    return codon_Size

def getBNF_Path():
    return BNF_Path

def getSize():
    return herd_Size


initialiseHerd()

print(herd[0].codon)
print(herd[0].phenotype)
print(herd[0].getProduction())
