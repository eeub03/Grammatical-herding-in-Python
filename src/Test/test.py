from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from fitness.santa_fe.ant_model import *


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
        self.phenotype = "if self.is_food_ahead(): \n  self.move()\nelse: \n  self.right()\nself.move()\nif self.is_food_ahead(): \n  self.left()\nelse: \n  self.left()\n  self.move()\n  self.move()"
        self.best_steps = 900
        print(self.phenotype)
ant1 = ant()

step_chart = ChartModule([{"Label": "Steps",
                           "Color": "Black",}],
                           data_collector_name= 'data_collector')
grid = CanvasGrid(agent_portrayal, 32, 32, 500, 500)
server = ModularServer(Ant_Model,
                       [grid, step_chart],
                       "Ant Model",
                       {"ant":ant1})

server.port = 8521 # The default
server.launch()