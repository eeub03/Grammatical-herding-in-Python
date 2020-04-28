from fitness.santa_fe.ant_model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    if agent.type == "ANT":
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "red",
                     "r": 0.5}
    else:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "green",
                     "r": 0.5}

    return portrayal

class ant:
    def __init__(self):
        self.index = 1
        self.phenotype ="if self.is_food_ahead(): \n  self.move()\n  self.move()\n  self.move()\n  self.right()\nelse: \n  self.left()\n  self.left()\nif self.is_food_ahead(): \n  self.right()\nelse: \n  self.left()\n  self.move()\nself.left()"
        self.best_steps = 900
        print(self.phenotype)
ant1 = ant()

grid = CanvasGrid(agent_portrayal, 32, 32, 500, 500)
server = ModularServer(Ant_Model,
                       [grid],
                       "Ant Model",
                       {"ant":ant1})
server.port = 8521 # The default
server.launch()