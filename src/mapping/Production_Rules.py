
def mapping(intString, choices):
    production_Rules = [0] * len(intString)
    for i in range (0, len(intString)):
        production_Rules[i] = int(intString[i] % choices)
    return production_Rules
