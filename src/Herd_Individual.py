import numpy as np
from parameters import parameters as par
import src.Mapper as mp
class HerdMember:
    def __init__(self, index):
        """:param index: Unique identifier for the Herd member"""
        self.index = index  # Unique Identifier for herd members
        self.phenotype = None  # Phenotype from the bitstring mapping
        self.current_Position = None  # Position in Search space
        self.isBeta = False
        self.isAlpha = False
        self.best_Position = None  # Best position from this member
        self.best_phenotype = None  # Best Phenotype from this member
        self.moves = None  # Number of moves made in the search space
        self.best_steps = None  # Best moves made
        self.fitness = None  # Current fitness of the herd members solution
        self.valid = False


        self.bitString = []
        for i in range(par.params['NO_OF_CODONS']):
            self.bitString.append(np.random.randint(0, 2, size=(par.params['CODON_SIZE'])))

        self.phenotype = mp. mapper(None, self)

    def getFitness(self):
        return self.fitness

    def getPhenotype(self):
        return self.phenotype
