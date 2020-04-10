import numpy as np
import src.mapping.Mapper as mp
from src.parameters.parameters import params

import importlib

class HerdMember:
    def __init__(self, index):
        """:param index: Unique identifier for the Herd member"""
        self.index = index  # Unique Identifier for herd members
        self.current_Position = None  # Position in Search space
        self.isAlpha = False
        self.best_Position = None  # Best position from this member
        self.best_phenotype = None  # Best Phenotype from this member
        self.moves = None  # Number of moves made in the search space
        self.best_steps = None  # Best moves made
        self.valid = False
        self.fitness = 0
        self.no_of_Codons = self.setGenotypeLength()
        self.fitnessPath = params['FITNESS_FUNCTION']
        print(self.no_of_Codons)
        self.bitString = ""
        for i in range(self.no_of_Codons):
            self.bitString += str((np.random.randint(0, 2, params['CODON_SIZE'])))
        # Formatting for our bitstring to make allow it to be read for conversion into int
        self.bitString = self.bitString.replace('[', '')
        self.bitString = self.bitString.replace(']', '' )
        self.bitString = self.bitString.replace('\n', '')
        self.bitString = self.bitString.replace(' ','')

        self.phenotype, self.nodes, self.invalid, self.max_depth, self.used_codons = mp.mapper(self)

        self.fitness = self.getFitness()



    def setGenotypeLength(self):
        minMaxCodon = 0
        codon_Min = params['CODON_MIN']
        codon_Max = params['CODON_MAX']
        # Creates codonSize many bitstring codons of pre defined codon size
        if codon_Max > 0 and codon_Min > 0:
            if codon_Min != codon_Max:
                minMaxCodon = np.random.randint(codon_Min + 2, codon_Max + 2)
            else:
                minMaxCodon = codon_Max
        return minMaxCodon


    def getFitness(self):
        module = importlib.import_module('src.fitness.' + params['FITNESS_FUNCTION'])
        fitness_class = getattr(module, params['FITNESS_FUNCTION'])
        fitness_Object = fitness_class()
        if self.invalid:
            fitness = None
        else:
            fitness = fitness_Object.evaluate(self)
        return fitness