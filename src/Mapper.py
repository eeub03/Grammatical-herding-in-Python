from PGEGrammar import tree as tr
import src.Production_Rules as pr
from parameters import parameters as par
import numpy as np


def mapper(tree, herd_member):
    assert (tree or herd_member)
    assert not (tree and herd_member)
    if herd_member:
        genotype = herd_member.bitString
        tree, genotype,  nodes, invalid, depth, used_codons = map_tree_from_member(genotype)
    else:
        output, invalid, depth, \
        nodes = tree.get_tree_info(par.params['GRAMMAR_FILE'].non_terminals.keys(),
                                   [], [])
        used_codons = len(herd_member.bitstring)

    if invalid:
        # Set values for invalid individuals.
        phenotype, nodes, depth, used_codons = None, np.NaN, np.NaN, np.NaN

    return tree, nodes, invalid, depth, used_codons

def convertBitstringToInteger(self, genotype,no_Of_Codons):
    """
    :param genotype: Bitstring of the herd member
    :param no_Of_Codons: The number of codons, used for the size of the phenotype
    """
    """What this does is generate our integer conversion based on our codon size. The size of the codon
        determines how many bits are in the bitstring. Converting to Denary is based on powers of 2 in binary
        so for the size of codon we add the extra conversion bit.
        E.g. for codon size 4 for we get the array [8 4 2 1] for 8 we get [128 64 32 16 8 4 2 1]
        Therefore to convert, we use a two for loops, one for the length of our Bitstring and another for the
        size of codon. Allowing us to go through the codons bit by bit and convert it denary
    """
    phenotype = [0]* no_Of_Codons
    binary2DecBits = []
    last = 0.5
    for k in range(par.params['CODON_SIZE']):

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


def map_tree_from_member(genotype):
    # Initialise an instance of the tree class

    tree1 = tr(par.params['BNF'].start_rule["symbol"], None)
    genotype_int = convertBitstringToInteger(genotype, par.params['NO_OF_CODONS'])

    # Map tree from the given genome
    output, used_codons, nodes, depth, max_depth, invalid = \
        map_tree(tree1, genotype, genotype_int, [], 0, 0, 0, 0)

    phenotype = "".join(output)

    if invalid:

        return tree1, genotype, nodes, invalid, max_depth, \
               used_codons
    else:
        return tree1, genotype, nodes, invalid, max_depth, \
            used_codons

def map_tree(tree, genotype, genotype_int, phenotype_output, index, depth, max_depth, nodes, invalid=False):
    """
      :param tree: Instance of the tree class
      :param genotype: Bitstring of the individual
      :param genotype_int: Integer conversion of the Bitstring
      :param phenotype_output: A list of all the terminal nodes in the subtree. This gets joined to become the phenotype
      :param index: Index of the location on the genotype
      :param depth: Current depth in the tree
      :param max_depth: The maximum depth in the tree so far
      :param nodes: Current total number of nodes in the tree so far
      :param invalid: Indicates whether the current individual is valid or not
      :return:index, the index of the current location on the genome,
             nodes, the total number of nodes in the tree thus far,
             depth, the current depth in the tree,
             max_depth, the maximum overall depth in the tree,
             invalid, a boolean flag indicating whether or not the
             individual is invalid.
    """
    """
    Edited version of PONYGE2'S GENOME_MAP function. Mostly my own code using my production rule selection
    function
    """

    if not invalid and index < len(genotype) * (par.params['MAX_WRAPS'] + 1):
        # If the solution is not invalid thus far, and if we still have
        # remaining codons in the genome, then we can continue to map the tree.

        if par.params['MAX_TREE_DEPTH'] and (max_depth > par.params['MAX_TREE_DEPTH']):
            # We have breached our maximum tree depth limit.
            invalid = True

        # Increment and set number of nodes and current depth.
        nodes += 1
        depth += 1
        tree.id, tree.depth = nodes, depth

        # Shows the different production choices and also how many of these choices there are that can
        # currently be made
        production_choices = par.params['BNF'].rules[tree.root]['choices']

        no_choices = par.params['BNF'].rules[tree.root]['no_choices']

        # Sets our codon tree value
        tree.codon = genotype_int[index % len(genotype_int)]

        # Here we use my production rule function instead of PONYGE's to get the production rule
        selection = pr.mapping(genotype_int, no_choices)
        chosen_prod_rule = production_choices[selection[index]]

        index += 1

        tree.children = []
        for symbol in chosen_prod_rule['choice']:
            # Add children to the derivation tree by creating a new instance
            # of the representation.tree.Tree class for each child.

            if symbol["type"] == "T":
                # Append the child to the parent node. Child is a terminal, do
                # not recurse.
                tree.children.append(tr(symbol["symbol"], tree))
                output.append(symbol["symbol"])

            elif symbol["type"] == "NT":
                # Append the child to the parent node.
                tree.children.append(tr(symbol["symbol"], tree))

                # Recurse by calling the function again to map the next
                # non-terminal from the genome.
                output, index, nodes, d, max_depth, invalid = \
                    map_tree(tree.children[-1], genotype, genotype_int,phenotype_output,
                                    index, depth, max_depth, nodes,
                                    invalid=invalid)


    else:
        # Mapping incomplete, solution is invalid.
        return phenotype_output, index, nodes, depth, max_depth, True

    # Find all non-terminals in the chosen production choice.
    NT_kids = [kid for kid in tree.children if kid.root in
               par.params['BNF'].non_terminals]

    if not NT_kids:
        # There are no non-terminals in the chosen production choice, the
        # branch terminates here.
        depth += 1
        nodes += 1

    if not invalid:
        # The solution is valid thus far.

        if depth > max_depth:
            # Set the new maximum depth.
            max_depth = depth

        if par.params['MAX_TREE_DEPTH'] and (max_depth > par.params['MAX_TREE_DEPTH']):
            # If our maximum depth exceeds the limit, the solution is invalid.
            invalid = True

    return output, index, nodes, depth, max_depth, invalid