
def mapping(phenotype):
    production_Rules = [0] * len(phenotype)
    print(type(production_Rules))
    for i in range (0, len(phenotype)):
        production_Rules[i] = phenotype[i] % 10
    return production_Rules
