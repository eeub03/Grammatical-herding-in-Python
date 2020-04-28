import importlib

import src.mapping.Genotype as gt
import src.mapping.Mapper as mp
from src.mapping.Key_Gen import get_geno_key
from src.parameters.parameters import params
from stats.statistics import geno_int_cache, pheno_cache


class Herd_Member:
    def __init__(self, index):
        """
        :param index: Unique identifier for Herd Member in the herd
        Attributes:
            index (int): Stores a unique number for each herd based on herd size.
            no_of_codons (int): Stores the number of codons the Herd Member should have for it's genotype
            fitness_path (string): Stores the path to the fitness function of the current run
            phenotype (string): Stores the current mapped phenotype of the current position of the Herd member
            genotype_int (array): Array of Ints that acts as the coordinate of the Herd member in the search space
            nodes (int): Stores the number of nodes in the individuals current phenotype tree
            invalid (boolean): Boolean value for whether the current mapping has lead to an invalid Herd member
            max_depth (int): Stores the max depth that the Members tree can reach
            used_codons (array): Stores the codons that the member has used
            fitness (float): Stores the current fitness of the members current phenotype
            best_phenotype (string): Stores the phenotype that the member has discovered that has the best fitness
            genotype (string): Stores the current Bitstring of the member. Used for mapping a solution.
            steps(int): Stores the current number of steps the current solution made in santa fe
            best_steps(int): Stores the best steps of the best phenotype found by the member
            fitness_class(object): Stores the current fitness class object for evaluation
        """
        self.index = index  # Unique Identifier for herd members
        self.no_of_codons = params['NUMBER_OF_CODONS']
        self.fitnessPath = params['FITNESS_FUNCTION']
        self.phenotype = None  # Tree mapped by mapper
        self.genotype_int = []  # Bitstring converted into integers
        self.best_genotype_int = [0] * self.no_of_codons  # Position in search space
        self.nodes = None  # Nodes on tree
        self.invalid = None  # Whether individual is valid for evaluation
        self.max_depth = None  # Max depth of tree
        self.used_codons = None  # Codons used by individual
        self.fitness = 0
        self.best_phenotype = None

        self.best_fitness = 0 # Best fitness found by Herd Member
        self.genotype = gt.genotype() # Creates random Unique Bitstring of Herd member
        self.steps = 0 # Steps taken by current generation
        self.best_steps = 900 # Best steps taken by best phenotype
        self.map_self() # Maps the genotype of the individual
        # Import the fitness function defined by user
        module = importlib.import_module('src.fitness.' + params['FITNESS_FUNCTION'])
        self.fitness_class = getattr(module, params['FITNESS_FUNCTION'])
        # Get the current fitness of the individual
        self.get_fitness()
        # If the individual is not invalid we then store it's location in the cache
        if not self.invalid:
            key = get_geno_key(self, None)
            geno_int_cache[key] = self.phenotype
            self.best_genotype_int = self.genotype_int

    def generate_fitness(self):
        """
        Function that is creates an instance of the fitness function class and gets the fitness of the individual
        """
        fitness_Object = self.fitness_class()
        self.fitness, self.steps = fitness_Object.evaluate(self)

        pheno_cache[self.phenotype] = self.fitness

    def get_fitness(self):
        """
        Function that checks is the individual is invalid and if it is, the fitness is set to 0.
        If the individual is valid, the function then checks to see if the location has been found before
        If it has been found we set the fitness to be the one stored in the cache.
        Else we then need to get the fitness of the individual by evaluating it
        """
        if self.invalid or self.phenotype == None:
            self.fitness = 0
        else:

            key = get_geno_key(self, None)
            if key in geno_int_cache and self.phenotype in pheno_cache:
                self.fitness = pheno_cache[self.phenotype]
            else:
                #
                self.generate_fitness()
        if params['MULTICORE']:
            return self

    def change_genotype_to(self, genotype_int):
        """

        :param genotype_int: Coordinate to change the current members coordinate to
        This functions changes the current members coordinate to a given coordinate.
        """
        self.genotype_int = genotype_int
        genotype = ""
        for i in range(self.no_of_codons):
            integer_val = format(int(genotype_int[i]), "b")
            integer_val = integer_val.replace("-", "")
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
        """
        Get's mapping from Mapper.py using Genotype of Herd member

        """

        self.phenotype, self.genotype_int, self.nodes, \
        self.invalid, self.max_depth, self.used_codons = mp.mapper(self)
