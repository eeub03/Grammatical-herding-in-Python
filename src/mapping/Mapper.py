# For maths functions
import numpy as np

# PONYGE's tree file. We use the Grammar File in our Parameters .py file.
from PGEGrammar import tree as tr
# Parameters for tree construction
from src.parameters.parameters import params
# If BNF is pyBNF we need to convert the grammar to python code with proper indentation
from src.python_filter import python_filter

"""
NOT MY CODE PONYGE'S 
"""

def mapper(herd_member):
    """
    Mapping function for an individual of the herd. Turns their Genotype into a coordinate as
    well as into a phenotype to mapped into a program from a grammar and tree.
    :param herd_member: Individual from herd to be mapped to a grammar tree
    :return tree: The phenotype of the individual that was mapped.
    :return genotype_int: The coordinate of the individual in the search space
    :return nodes: The nodes in the phenotype tree
    :return invalid: Whethere the individuals Phenotype is invalid
    :return depth: The depth of the tree of the mapped individual
    :return used_codons: The codons that were used by the tree
    """
    if herd_member:
        genotype = herd_member.genotype

        tree, genotype_int, nodes, invalid, depth, used_codons = map_tree_from_member(genotype)
    else:
        print("invalid")

    if params['BNF'].python_mode and not invalid:
        # Grammar contains python code

        tree = python_filter(tree)

    if invalid:
        # Set values for invalid individuals.
        tree, genotype_int, nodes, depth, used_codons = None, np.NaN, np.NaN, np.NaN, np.NaN

    return tree, genotype_int, nodes, invalid, depth, used_codons


def convert_bs_to_int(genotype):
    """
    This function converts a Binary String Genotype into integer coordinates.
    Assumes Bitstring is one long connected string consisting of 0's and 1's e.g "000000101010"
    :param genotype: Bitstring of the herd member
    :return genotype_int: The coordinate of the individual in the search space
    """

    genotype_int = []

    genotype_list = [str(x) for x in genotype]
    try:
        for i in range(params['NUMBER_OF_CODONS']):
            current_codon = i * params['CODON_SIZE']

            gl = genotype_list[current_codon: (current_codon + params['CODON_SIZE'])]
            gs = ""
            genotype_string = gs.join(gl)

            genotype_int.append(int(genotype_string, 2))
    except ValueError:

        # error checking when converting to integer
        print(len(genotype_list))
        print(genotype_string)
        raise ValueError("Check the genotype being passed is a Binary String")

    return genotype_int

"""
NOT MY CODE PONYGE'S 
"""
def map_tree_from_member(genotype):

    """
    Creates the tree from the genotype of a Herd member by converting their Genotype into an
    integer coordinate in the search space and mapping that into a tree.
    :param genotype: The bitstring of the individual to be mapped
    :return:
    """
    # Initialise an instance of the tree class

    tree1 = tr.Tree(params['BNF'].start_rule["symbol"], None)
    genotype_int = convert_bs_to_int(genotype)

    # Map tree from the given genome
    output, used_codons, nodes, depth, max_depth, invalid = \
        map_tree(tree1, genotype, genotype_int, [], 0, 0, 0, 0)

    phenotype = "".join(output)

    if invalid:
        return None, genotype_int, nodes, invalid, max_depth, used_codons
    else:
        return phenotype, genotype_int, nodes, invalid, max_depth, used_codons

"""
NOT MY CODE PONYGE'S 
"""
def map_tree(tree, genotype, genotype_int, phenotype_output, index, depth, max_depth, nodes, invalid=False):

    """
    This is a recursive function that maps nodes to the tree and checks the depth to see if the individual is invalid
    Also maps coordinates of individual into production rules for Phenotype mapping
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


    if not invalid and index < len(genotype_int) * (params['MAX_WRAPS'] + 1):
        # If the solution is not invalid thus far, and if we still have
        # remaining codons in the genome, then we can continue to map the tree.

        if params['MAX_TREE_DEPTH'] and (max_depth > params['MAX_TREE_DEPTH']):
            # We have breached our maximum tree depth limit.
            print("Max breached")
            invalid = True

        # Increment and set number of nodes and current depth.
        nodes += 1
        depth += 1
        tree.id, tree.depth = nodes, depth

        # Shows the different production choices and also how many of these choices there are that can
        # currently be made
        production_choices = params['BNF'].rules[tree.root]['choices']

        no_choices = params['BNF'].rules[tree.root]['no_choices']

        # Sets our codon tree value
        tree.codon = genotype_int[index % len(genotype_int)]

        # Here we use my production rule function instead of PONYGE's to get the production rule
        selection = tree.codon % no_choices
        chosen_prod_rule = production_choices[selection]

        index += 1

        tree.children = []
        for symbol in chosen_prod_rule['choice']:
            # Add children to the derivation tree by creating a new instance
            # of the representation.tree.Tree class for each child.

            if symbol["type"] == "T":
                # Append the child to the parent node. Child is a terminal, do
                # not recurse.
                tree.children.append(tr.Tree(symbol["symbol"], tree))

                phenotype_output.append(symbol["symbol"])

            elif symbol["type"] == "NT":
                # Append the child to the parent node.

                tree.children.append(tr.Tree(symbol["symbol"], tree))

                # Recurse by calling the function again to map the next
                # non-terminal from the genome.
                phenotype_output, index, nodes, d, max_depth, invalid = \
                    map_tree(tree.children[-1], genotype, genotype_int, phenotype_output,
                             index, depth, max_depth, nodes,
                             invalid=invalid)


    else:
        # Mapping incomplete, solution is invalid.

        return phenotype_output, index, nodes, depth, max_depth, True

    # Find all non-terminals in the chosen production choice.
    NT_kids = [kid for kid in tree.children if kid.root in
               params['BNF'].non_terminals]

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

        if params['MAX_TREE_DEPTH'] and (max_depth > params['MAX_TREE_DEPTH']):
            # If our maximum depth exceeds the limit, the solution is invalid.
            print("MAX_DEPTH BREACHED")
            invalid = True

    return phenotype_output, index, nodes, depth, max_depth, invalid
