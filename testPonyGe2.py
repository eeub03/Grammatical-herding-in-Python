# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 15:27:35 2019

@author: Joe
"""

from ponyge2.src.algorithm.parameters import params,set_params
from ponyge2.src.stats.stats import get_stats


import sys


def mane():
    """ Run program """
    print("hello")
    # Run evolution
    individuals = params['SEARCH_LOOP']()

    # Print final review
    get_stats(individuals, end=True)


if __name__ == "__main__":
    set_params(sys.argv[1:])  # exclude the ponyge.py arg itself
    mane()
