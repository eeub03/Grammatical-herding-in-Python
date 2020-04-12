import numpy as np
import src.mapping.Mapper as mp
from src.parameters.parameters import params
import importlib


class HerdMember:
    def __init__(self, index):
        """:param index: Unique identifier for the Herd member"""
        self.index = index  # Unique Identifier for herd members
        self.current_Position = None  # Position in Search space
        self.best_Position = None  # Best position from this member
        self.best_phenotype = None  # Best Phenotype from this member
        self.moves = None  # Number of moves made in the search space
        self.best_steps = None  # Best moves made
        self.phenotype = None  # Tree mapped by mapper
        self.genotype_int = None  # Bitstring converted into integers
        self.nodes = None  # Nodes on tree
        self.invalid = None  # Whether individual is valid for evaluation
        self.max_depth = None  # Max depth of tree
        self.used_codons = None  # Codons used by individual
        self.fitness = 0
        self.no_of_codons = params['NUMBER_OF_CODONS']
        self.fitnessPath = params['FITNESS_FUNCTION']

        self.genotype = ""
        for i in range(self.no_of_codons):
            self.genotype += str((np.random.randint(0, 2, params['CODON_SIZE'])))
        # Formatting for our bitstring to make allow it to be read for conversion into int
        self.genotype = self.genotype.replace('[', '')
        self.genotype = self.genotype.replace(']', '')
        self.genotype = self.genotype.replace('\n', '')
        self.genotype = self.genotype.replace(' ', '')


        self.map_self()

        self.get_fitness()



    def get_fitness(self):
        module = importlib.import_module('src.fitness.' + params['FITNESS_FUNCTION'])
        fitness_class = getattr(module, params['FITNESS_FUNCTION'])
        fitness_Object = fitness_class()
        if self.invalid:
            self.fitness = 0
        else:
            self.fitness = fitness_Object.evaluate(self)

    def change_genotype_to(self, member, genotype_int):
        assert member or genotype_int
        assert not (member and genotype_int)
        if member:
            self.genotype = member.genotype

            self.genotype_int = member.genotype
            self.phenotype = member.phenotype
        else:
            genotype = ""
            for i in range(len(genotype_int)):
                genotype += format(int(genotype_int[i]), "b")

            genotype = genotype.replace("-","")
            self.genotype = genotype
            self.map_self()
        self.get_fitness()

    def map_self(self):
        self.phenotype, self.genotype_int, self.nodes, \
        self.invalid, self.max_depth, self.used_codons = mp.mapper(self)
