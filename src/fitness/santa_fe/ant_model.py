from mesa import *
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation


# Function that tracks the number of food eaten by the ant
def get_stats(model):
    food_eaten = [agent.food_eaten for agent in model.schedule.agents]
    #index = model.id
    #
    return food_eaten
def get_steps(model):
    steps = [agent.steps for agent in model.schedule.agents]
    return steps
# Class for ant that moves in the santa fe trail
class AntAgent(Agent):
    def __init__(self,unique_id, model, ind):
        super().__init__(unique_id, model)
        # Type of agent to differentiate the ant from a food agent
        self.type = "ANT"
        # Get the direction that ant is facing.
        # default is right
        self.facing = 0
        # Sets the patch in fron as the patch the ant is currently facing
        self.facing_pos = (1,31)
        # The number of food eaten by the ant
        self.food_eaten = 0
        # The current individuals Phenotype that is being used by the ant
        self.ind = ind
        # When the run is over return the completed ind
        self.complete_ind = None
        self.steps = 0

    def move(self):
        # Current location of ant in trail

        # Conditions that check where the ant is facing and sets the facing position to be moved into as the patch after
        new_pos = self.facing_pos

        self.model.grid.move_agent(self, new_pos)
        self.get_facing_pos()

        self.steps += 1

        food = self.model.grid.get_cell_list_contents([self.pos])
        if len(food) > 1:
            self.food_eaten += 1

            for i in range(len(food)):
                if food[i].type == "FOOD":
                    food_object = food[i]

            self.model.grid.remove_agent(food_object)


    def left(self):
        self.steps += 1
        self.facing = self.facing - 1
        if self.facing == -1:
            self.facing = 3
        self.get_facing_pos()



    def right(self):
        self.steps += 1
        self.facing = self.facing + 1
        if self.facing == 4:
            self.facing = 0
        self.get_facing_pos()

    def is_food_ahead(self):
        self.steps += 1

        food = self.model.grid.get_cell_list_contents([self.facing_pos])

        if len(food) > 0:
            return True

    def get_facing_pos(self):
        x, y = self.pos
        if self.facing == 0:
            self.facing_pos = (x + 1, y)
        # facing down
        elif self.facing == 1:
            self.facing_pos = (x, y - 1)
        # facing left
        elif self.facing == 2:

            self.facing_pos = (x - 1, y)
        # facing up
        else:
            self.facing_pos = (x, y + 1)

        # These conditions just allow the ant to loop round the world
        if self.facing_pos[0] > 31:
            self.facing_pos = (0, self.facing_pos[1])
        elif self.facing_pos[1] > 31:
            self.facing_pos = (self.facing_pos[0], 0)
        elif self.facing_pos[0] < 0:
            self.facing_pos = (31, self.facing_pos[1])
        elif self.facing_pos[1] < 0:
            self.facing_pos = (self.facing_pos[0], 31)

    def step(self):

        # If our agent eats all the food, achieving 100% fitness. Then the best solution is found
        if self.food_eaten == 89:
            print("YES")
        if self.food_eaten > 88:
            print("found")
            if self.ind.best_steps > self.steps:
                self.ind.best_steps = self.steps
            print(self.steps)
            self.complete_ind = self.ind

        elif self.steps >= 900:
            if self.ind.best_steps == 0:
                self.ind.best_steps = 900
            self.complete_ind = self.ind
            self.ind.steps = 900
        else:
            exec(self.model.get_actions())


class Food(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.type = "FOOD"

class Ant_Model(Model):
    """A model with some number of agents."""
    def __init__(self,ant):
        self.running = True
        self.id = ant.index
        self.actions = ant.phenotype
        # list for the agents in the model
        self.ants = []
        # Creates a schedule for stepping in the model
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
        # Scans the santa fe data file to recreate the trail in MESA
        f = open("C:/Users/Joe/Documents/3 YEAR PROJECT IMPORTANT/code/src/fitness/santa_fe/trail/data.dat")
        lines = f.readlines()
        j = -1
        for x in lines:
            j += 1

            row = x.split()
            for i in range(len(row[0]) - 1):
                if row[0][i] == "x":

                    food = Food(x * i,self)

                    self.grid.place_agent(food, (i,31 - j ))
        f.close()
        # Keeps track of the food eaten by the ant throughout the run
        self.data_collector = DataCollector(
            model_reporters={"Stats":get_stats, "Steps":get_steps}
        )

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()

    def get_actions(self):
        return self.actions

    def return_agent(self):
        ind = self.ants[0]

        return ind.complete_ind, ind.food_eaten, ind.steps

