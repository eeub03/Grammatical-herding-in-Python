# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:28:49 2019

@author: Joseph Morgan
@name: Grammatical Herding in Python
@version: 0.1a
"""

import HerdMemberCreation, os

herd = []
sort_Herd = []
iterations = 1
average_Fitness = 0.0
herd_Size = 0
BNF_Path = ""

codon_Min = 0
codon_Max = 0
codon_Size = 0
max_Iterations = 0


def initialiseHerd(size, iterations , min_Codon, max_Codon, size_Codon, BNF):
    herd_Size = size
    max_Iterations = iterations
    codon_Min = min_Codon
    codon_Max = max_Codon
    codon_Size = size_Codon
    BNF_Path = BNF
    for i in range(0, herd_Size):
        print("Running")
        herd.append(HerdMemberCreation.HerdMember(i, codon_Min, codon_Max, codon_Size, BNF_Path))

def initialiseHerdFile(filePath):
    parameters = [0]*6
    print(os.getcwd())
    try:
        f = open(filePath)
        for i in range(0, 5):
            line = f.readline(i)
            print("line = " + line + "\n")
            parameters[i] = ''.join(line.partition("#"))
            print("p[i] = " + parameters[i])
            if i < 5:
                p = parameters[i]
                parameters[i] = int(p)
        print(parameters)
        initialiseHerd(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5])
    except IOError:
        print("The file at " + filePath + " Could not be opened, IOError.")




def getAvgFitness():
    avg_Fitness = 0
    for i in range(herd_Size):

        avg_Fitness = avg_Fitness + herd[i].getFitness()

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
    return herd_Size


initialiseHerdFile('parameters\\initialiseHerd.txt')

print(herd[0].bitString)
print(herd[0].phenotype)
