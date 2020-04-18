import importlib

import src.mapping.Genotype as gt
import src.mapping.Mapper as mp
from src.parameters.parameters import params
from stats.statistics import geno_int_cache, pheno_cache


class Herd_Member:
    def __init__(self, index):
        """:param index: Unique identifier for the Herd member"""
        self.index = index  # Unique Identifier for herd members
        self.no_of_codons = params['NUMBER_OF_CODONS']
        self.fitnessPath = params['FITNESS_FUNCTION']
        self.phenotype = None  # Tree mapped by mapper
        self.genotype_int = []  # Bitstring converted into integers
        self.best_genotype_int = [0] * self.no_of_codons # Position in search space
        self.nodes = None  # Nodes on tree
        self.invalid = None  # Whether individual is valid for evaluation
        self.max_depth = None  # Max depth of tree
        self.used_codons = None  # Codons used by individual
        self.fitness = 0
        self.best_phenotype = None

        self.best_fitness = 0
        self.genotype = gt.genotype(self)
        self.steps = 0
        self.best_steps = 0
        self.map_self()

        self.get_fitness()
        if not self.invalid:
            key = self.get_geno_key()
            geno_int_cache[key] = self.phenotype
            pheno_cache[self.phenotype] = self.fitness
            self.best_genotype_int = self.genotype_int

    def get_geno_key(self):

        list_int = self.genotype_int
        i =0
        str_int = ""
        while i < len(list_int):

            str_int += str(list_int[i])
            i += 1
        str_int = str_int.replace('.','')
        str_int = str_int.replace('-', '')
        key = int(str_int)
        return key

    def get_fitness(self):
        
        module = importlib.import_module('src.fitness.' + params['FITNESS_FUNCTION'])
        fitness_class = getattr(module, params['FITNESS_FUNCTION'])

        if self.invalid:
            self.fitness = 0
        else:
            fitness_Object = fitness_class(self)
            self.fitness = fitness_Object.evaluate()



    def change_genotype_to(self,genotype_int):

        self.genotype_int = genotype_int

        key = self.get_geno_key()

        if key in geno_int_cache:

            self.phenotype = geno_int_cache[key]
            if self.phenotype in pheno_cache:
                self.fitness = pheno_cache[self.phenotype]
            else:
                self.get_fitness()
                pheno_cache[self.phenotype] = self.fitness
        else:
            genotype = ""
            for i in range(len(genotype_int)):
                integer_val = format(int(genotype_int[i]), "b")
                if len(integer_val) < params['CODON_SIZE']:
                    zeros = params['CODON_SIZE'] - len(integer_val)
                    string_zeros = "0" * zeros
                    integer_val = string_zeros + integer_val

                genotype += integer_val

            genotype = genotype.replace("-", "")
            genotype = genotype.replace(" ", "")

            self.genotype = genotype
            self.map_self()
            if not self.invalid:
                self.invalid = False
                key = self.get_geno_key()
                geno_int_cache[key] = self.phenotype
                self.get_fitness()
                pheno_cache[self.phenotype] = self.fitness




    def map_self(self):
        self.phenotype, self.genotype_int, self.nodes, \
        self.invalid, self.max_depth, self.used_codons = mp.mapper(self)
