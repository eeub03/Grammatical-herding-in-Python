# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 15:27:35 2019

@author: Joe
"""

import


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
