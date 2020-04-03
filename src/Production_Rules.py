
def mapping(intString, choices):
    production_Rules = [0] * len(intString)
    print(type(production_Rules))
    for i in range (0, len(intString)):
        production_Rules[i] = intString[i] % choices
    return production_Rules
