def createPhenotype(self, genotype, codon_Size, no_Of_Codons):
    phenotype = [0]* no_Of_Codons
    binary2DecBits = []
    last = 0.5
    for k in range(codon_Size):
        # What this does is generate our integer conversion based on our codon size, the size of the codon
        # determines how many bits are in one. Converting to Denary is based on powers of 2 in binary
        # so for the size of codon we add the extra conversion bit.
        # E.g. for codon size 4 for we get the array [8 4 2 1] for 8 we get [128 64 32 16 8 4 2 1]
        currentBit = 2 * last  # This is the current bit so our first one would be 1.
        binary2DecBits.append(currentBit)  # Adds the bit to the conversion array
        last = currentBit  # Sets the currentBit to last bit for next iteration
    # Here we convert our bitString to integers based on codon size. Because of our last for loop, "binary2DecBits"
    # Is the same size as our codon size.

    for i in range(len(genotype)):
        for j in range(len(binary2DecBits)):


            # Here we convert the Bistring to integers, splitting it based on the codon size.
            phenotype[i] = (phenotype[i] + (genotype[i][j] * binary2DecBits[j]))

    print("Returning phenotype")
    return phenotype