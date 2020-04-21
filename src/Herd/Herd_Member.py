import importlib

import src.mapping.Genotype as gt
import src.mapping.Mapper as mp
from src.mapping.Key_Gen import get_geno_key
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

        module = importlib.import_module('src.fitness.' + params['FITNESS_FUNCTION'])
        self.fitness_class = getattr(module, params['FITNESS_FUNCTION'])

        self.get_fitness()

        if not self.invalid:
            key = get_geno_key(self, None)
            geno_int_cache[key] = self.phenotype
            self.best_genotype_int = self.genotype_int



    def generate_fitness(self):

        if params['BATCH'] == False:
            fitness_Object = self.fitness_class(self)
            self.fitness = fitness_Object.evaluate()

        pheno_cache[self.phenotype] = self.fitness

    def get_fitness(self):
        if self.invalid or self.phenotype == None:
            self.fitness = 0
        else:

            key = get_geno_key(self, None)
            if key in geno_int_cache and self.phenotype in pheno_cache:
                self.fitness = pheno_cache[self.phenotype]
            else:
                self.generate_fitness()
        if params['MULTICORE']:
            return self



    def change_genotype_to(self, genotype_int):

        self.genotype_int = genotype_int
        genotype = ""
        for i in range(self.no_of_codons):
            integer_val = format(int(genotype_int[i]), "b")
            integer_val = integer_val.replace("-","")
            integer_val = integer_val.replace(".", "")
            if len(integer_val) < params['CODON_SIZE']:
                zeros = params['CODON_SIZE'] - len(integer_val)
                string_zeros = "0" * zeros
                integer_val = string_zeros + integer_val

            genotype += integer_val



        self.genotype = genotype
        self.map_self()
        if not self.invalid:
            self.invalid = False
            key = get_geno_key(self, None)
            geno_int_cache[key] = self.phenotype



    def map_self(self):
        self.phenotype, self.genotype_int, self.nodes, \
        self.invalid, self.max_depth, self.used_codons = mp.mapper(self)
