from fitness.santa_fe.ant_model import *

from src.parameters.parameters import  params

from src.fitness.base_ff import base_ff



class sft(base_ff):
    """
        :param base_ff: Template class for fitness function

    """


    def __init__(self,ind):
        """
        All fitness functions which inherit from the bass fitness function
        class must initialise the base class during their own initialisation.
        """

        # Initialise base fitness function class.
        super().__init__()
        self.ind = ind

        model = Ant_Model(self.ind.index, self.ind.phenotype, self.ind)
        for i in range(params['MAX_STEPS']):
            model.step()
            self.ind, self.fitness = model.return_agent()
            if self.ind != None:
                break

    def evaluate(self, **kwargs):
        """
        Default fitness execution call for all fitness functions. When
        implementing a new fitness function, this is where code should be added
        to evaluate target phenotypes.

        There is no need to implement a __call__() method for new fitness
        functions which inherit from the base class; the "evaluate()" function
        provided here allows for this. Implementing a __call__() method for new
        fitness functions will over-write the __call__() method in the base
        class, removing much of the functionality and use of the base class.

        :param ind: An individual to be evaluated.
        :param kwargs: Optional extra arguments.
        :return: The fitness of the evaluated individual.
        """


        return self.fitness
    def get_ind_stats(self, ind,**kwargs):
        return self.ind