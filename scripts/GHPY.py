
"""
Created on Sat Oct 12 13:28:49 2019

@author: Joseph Morgan
@name: Grammatical Herding in Python
@version: 1.0
"""
import src.Herd.Herd as Herd
from src.parameters.parameters import params
# Initialises Herd
Herd1 = Herd.Herd()
def pool_init(params_):
    """
    When initialising the pool the original params dict (params_) is passed in
    and used to update the newly created instance of params, as Windows does
    not retain the system memory of the parent process.

    :param params_: original params dict
    :return: Nothing.
    """

    from platform import system

    if system() == 'Windows':
        params.update(params_)


def main():

    import stats.statistics as stats
    from src.parameters.parameters import params
    from multiprocessing import Pool
    if params['MULTICORE']:

        # initialize pool once, if mutlicore is enabled
        params['POOL'] = Pool(processes=params['CORES'], initializer=pool_init,
                              initargs=(params,))  # , maxtasksperchild=1)



    # Start run of herd
    Herd1.start_evaluation()

    stats.save()
    if params['MULTICORE']:
        params['POOL'].close()




if __name__ == '__main__':
    main()