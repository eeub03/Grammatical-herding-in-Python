import numpy as np
import matplotlib.pyplot as plt
import santa_fe.ant_model as am
import pandas as pd
model = am.Ant_Model(500)

for i in range(10):
    model.step()

food_eaten = model.data_collector.get_model_vars_dataframe()
print(food_eaten)