from src.parameters.parameters import params
import numpy as np
def genotype():
    """
    Function that creates a random bitstring for the herd member
    :return: Bitstring containing only '0's and '1's
    """

    genotype1 = ""
    for i in range(params['NUMBER_OF_CODONS']):
        genotype1 += str((np.random.randint(0, 2, params['CODON_SIZE'])))
    # Formatting for our bitstring to make allow it to be read for conversion into int
    genotype1 = genotype1.replace('[', '')
    genotype1 = genotype1.replace(']', '')
    genotype1 = genotype1.replace('\n', '')
    genotype1 = genotype1.replace(' ', '')

    return genotype1