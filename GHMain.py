# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:28:49 2019

@author: Joseph Morgan
@name: Grammatical Herding in Python
@version: 0.1a
"""

import HerdMemberCreation

herd = []
sort_Herd = []
iterations = 1
average_Fitness = 0.0
best_Position = ()
herdSize = 0
valid = ()
BNF_Path = ""

codon_Min = 0
codon_Max = 0
codon_Size = 0
max_Iterations = 0


def initialiseHerd(size, iterations , min_Codon, max_Codon, size_Codon, BNF):
    herdSize = size
    max_Iterations = iterations
    codon_Min = min_Codon
    codon_Max = max_Codon
    codon_Size = size_Codon
    BNF_Path = BNF
    for i in range(0, herdSize):
        print("Running")
        herd.append(HerdMemberCreation.HerdMember(i, codon_Min, codon_Max, codon_Size, BNF_Path))

def evaluateHerd():
    itera = 0
    while itera < max_Iterations:
        itera = itera + 1



def getCodonMax():
    return codon_Max

def getCodonMin():
    return codon_Min

def getCodonSize():
    return codon_Size

def getBNF_Path():
    return BNF_Path

def getSize():
    return herdSize


initialiseHerd(4,1,20,20,8,"SFT.BNF")

print(herd[0].bitString)
print(herd[0].phenotype)
