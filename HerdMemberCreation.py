import numpy as np
import Phenotype as ph
import Production_Rules as PR
class HerdMember:
    def __init__(self, index, codon_Min, codon_Max, codon_Size, BNF_Path):
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
        # Creates codonSize many bitstring codons of pre defined codon size
        if codon_Min != codon_Max:
            minMaxCodon = np.random.randint(codon_Min+2, codon_Max+2)
        else:
            minMaxCodon = np.random.randint(codon_Max+2)
        print("minMaxCodon: " + str(minMaxCodon))
        self.codon = []
        for i in range(minMaxCodon):
            self.codon.append(np.random.randint(0,2, size=(codon_Size)))
        self.bitString = self.codon
        self.phenotype = ph.createPhenotype(self, self.bitString, codon_Size, minMaxCodon)

    def getFitness(self):
        return self.fitness
    def getProduction(self):
        return PR.mapping(self.phenotype)


