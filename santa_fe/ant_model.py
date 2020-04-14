
from src.parameters.parameters import params
from mesa import *
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def compute_food(model):
    food_eaten = [agent.food_eaten for agent in model.schedule.agents]
    return food_eaten
def steps(agent):
    return agent.steps
class AntAgent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.facing = 0 # default is right
        self.facing_pos = (0,0)
        self.food_eaten = 0
        self.steps = 0
    def move(self):
        x, y = self.pos
        if self.facing == 0:
            new_pos = self.facing_pos
            self.facing_pos = (x + 2, y)
            self.model.grid.move_agent(self, new_pos )
        if self.facing == 1:
            new_pos = (x, y - 1)
            self.facing_pos = (x, y - 2)
            self.model.grid.move_agent(self, new_pos)

        if self.facing == 2:
            new_pos = self.facing_pos
            self.facing_pos = (x - 2, y)
            self.model.grid.move_agent(self, new_pos)

        if self.facing == 3:
            new_pos = self.facing_pos
            self.facing_pos = (x , y + 2)
            self.model.grid.move_agent(self, new_pos)
        self.steps += 1
        food = self.model.grid.get_cell_list_contents([self.pos])
        if food > 1:
            self.food_eaten += 1
            food_object = self.random.choice(food)
            del food_object

    def left(self):
        self.facing = self.facing - 1
        if self.facing == -1:
            self.facing = 3


    def right(self):
        self.facing = self.facing + 1
        if self.facing == 4:
            self.facing = 0

    def is_food_ahead(self):
        food = self.model.grid.get_cell_list_contents([self.facing_pos])
        if len(food) > 1:
            return True

class Food(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

class Ant_Model(Model):
    """A model with some number of agents."""
    def __init__(self,max_steps):
        ants = []
        self.schedule = RandomActivation(self)
        # Initialise a grid of the same size as Santa Fe Trail
        self.grid = MultiGrid(32, 32, True)
        # Create agents
        self.max_food = 89
        self.max_steps = max_steps
        a = AntAgent(0, self)
        self.schedule.add(a)
        ants.append(a)
        # Place our ant at the start of the model
        self.grid.place_agent(a,(0,0))
        f = open("trail\data.dat")
        lines = f.readlines()
        j = -1
        for x in lines:
            j += 1

            row = x.split()
            for i in range(len(row[0]) - 1):
                if row[0][i] == "x":

                    f = Food(x * i,self)

                    self.grid.place_agent(f, (j, i))

        self.data_collector = DataCollector(
            model_reporters={"Food_eaten": compute_food},
            agent_reporters={"Steps": steps}
        )

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()

    def agent_actions(self, actions):
