

from mesa import *
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def compute_food(model):
    food_eaten = [agent.food_eaten for agent in model.schedule.agents]
    return food_eaten
def get_id(model):
    return model.id


class AntAgent(Agent):
    def __init__(self,unique_id, model, ind):
        super().__init__(unique_id, model)
        self.type = "ANT"
        self.facing = 0 # default is right
        self.facing_pos = (0,0)
        self.food_eaten = 0
        self.ind = ind
        self.complete_ind = None

    def move(self):
        x, y = self.pos
        if self.facing == 0:
            new_pos = self.facing_pos
            self.facing_pos = (x + 2, y)

        if self.facing == 1:
            new_pos = (x, y - 1)
            self.facing_pos = (x, y - 2)


        if self.facing == 2:
            new_pos = self.facing_pos
            self.facing_pos = (x - 2, y)


        if self.facing == 3:
            new_pos = self.facing_pos
            self.facing_pos = (x , y + 2)

        if self.facing_pos[0] > 31:
            self.facing_pos = (0,self.facing_pos[1])
        if self.facing_pos[1] > 31:
            self.facing_pos = (self.facing_pos[0], 0)
        if self.facing_pos[0] < 0:
            self.facing_pos = (31, self.facing_pos[1])
        if self.facing_pos[1] < 0:
            self.facing_pos = (self.facing_pos[0], 31)



        self.model.grid.move_agent(self, new_pos)
        self.model.schedule.steps += 1

        food = self.model.grid.get_cell_list_contents([self.pos])
        if len(food) > 1:
            self.food_eaten += 1

            for i in range(len(food)):
                if food[i].type == "FOOD":
                    food_object = food[i]

            self.model.grid.remove_agent(food_object)



    def left(self):
        self.model.schedule.steps += 1
        self.facing = self.facing - 1
        if self.facing == -1:
            self.facing = 3


    def right(self):
        self.model.schedule.steps += 1
        self.facing = self.facing + 1
        if self.facing == 4:
            self.facing = 0

    def is_food_ahead(self):

        self.model.schedule.steps += 1
        food = self.model.grid.get_cell_list_contents([self.facing_pos])

        if len(food) > 0:
            return True

    def step(self):
        # If our agent eats all the food, achieving 100% fitness. Then the best solution is found
        if self.food_eaten == 89:
            if self.ind.best_steps > self.model.schedule.steps:
                self.ind.best_steps = self.model.schedule.steps
                self.complete_ind = self.ind
        if self.model.schedule.steps == 900:
            if self.ind.best_steps == 0:
                self.ind.best_steps = 900
            self.complete_ind = self.ind
        else:
            exec(self.model.get_actions())

    def return_ind(self):
        return self.ind

class Food(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.type = "FOOD"

class Ant_Model(Model):
    """A model with some number of agents."""
    def __init__(self, index, actions, ant):
        self.id = index
        self.actions = actions
        self.ants = []
        self.schedule = RandomActivation(self)
        # Initialise a grid of the same size as Santa Fe Trail
        self.grid = MultiGrid(32, 32, True)
        # Create agents
        self.max_food = 89
        a = AntAgent(0, self, ant)
        self.schedule.add(a)
        self.ants.append(a)
        # Place our ant at the start of the model
        self.grid.place_agent(a,(0,31))
        f = open("C:/Users/Joe/Documents/3 YEAR PROJECT IMPORTANT/code/src/fitness/santa_fe/trail/data.dat")
        lines = f.readlines()
        j = -1
        for x in lines:
            j += 1

            row = x.split()
            for i in range(len(row[0]) - 1):
                if row[0][i] == "x":

                    f = Food(x * i,self)

                    self.grid.place_agent(f, (i,31 - j ))

        self.data_collector = DataCollector(
            model_reporters={"Model_id": get_id, "Food_eaten": compute_food},
        )

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()

    def return_agent(self):
        ant = self.ants[0]
        return ant.complete_ind, ant.food_eaten
    def get_actions(self):
        return self.actions


