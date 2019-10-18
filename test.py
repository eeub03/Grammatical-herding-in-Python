# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:28:49 2019

@author: Joseph Morgan
@name: Grammatical Herding in Python
"""

import numpy, matplolib, scipy, pandas, scikitlearn, bitstring, ponyge2



class Herding:
    def __init__(self,size):
        self.herd = ()
        self.sort_Herd = ()
        self.betas_Array =()
        self.iterations = 1
        self.average_Fitness = 0.0
        self.best_Position
        for i in range(0, size):
            self.herd.append(agent(),i)
        
        
    #Sets the number of times the algorithm evaluates the herd    
    def setIterations(self,times):
        self.iterations = times
    

    
class agent:
    def __init__(self,index):
        self.fitness = 0
        self.current_Position
        self.index = index
        