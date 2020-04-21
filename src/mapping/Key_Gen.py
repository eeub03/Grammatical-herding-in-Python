def get_geno_key(ind, genotype_int):
    assert ind or genotype_int
    assert not (ind and genotype_int)
    if ind:
        list_int = ind.genotype_int
    else:
        list_int = genotype_int
    i = 0
    str_int = ""
    while i < len(list_int):
        str_int += str(list_int[i])
        i += 1
    str_int = str_int.replace('.', '')
    str_int = str_int.replace('-', '')
    str_int = str_int.replace('[', ' ')
    str_int = str_int.replace(']', '')
    str_int = str_int.replace('\n', '')
    str_int = str_int.replace('  ', ' ')
    str_int = str_int.replace('   ', ' ')
    str_int = str_int.replace(' ', '')

    if str_int[0] == " ":
        str_int = list(str_int)
        str_int[0] = ""
        str_int = "".join(str_int)
    key = int(str_int)
    return key