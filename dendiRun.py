from dendiModel import *
import matplotlib.pyplot as plt
import pandas as pd

from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

attFile = 'dendiAtt.csv'
connFile = 'dendiConn.csv'
# FOR MESA:

# def agent_portrayal(agent):
# 	portrayal = {"Shape": "circle",
#                  "Filled": "true",
#                  "Color": "red",
#                  "Layer": 0}
# 	portrayal["r"] = agent.rice/2
# 	if agent.role == "producer":
# 		portrayal["Color"] = "green"
# 	elif agent.role == "assembler":
# 		portrayal["Color"] = "blue"
# 	elif agent.role == "retailer":
# 		portrayal["Color"] = "orange"
# 	else:
# 		portrayal["Color"] = "red"

# 	return portrayal

# grid = CanvasGrid(agent_portrayal, len(pd.read_csv(attFile, header = None))//2, len(pd.read_csv(attFile, header = None))//2, 500, 500)
# server = ModularServer(Model,
# 					   [grid],
# 					   "Dendi Model", {"attributesFile": attFile, "connectionsFile": connFile, "xmax": 2, "ymax":2, "roleOrder": ["producer", "assembler", 
# 					   "retailer", "consumer"]})
# server.port = 8521 # The default
# server.launch()

# FOR ANIMATED NETWORK GRAPH:
roleOrder = ["producer", "assembler", "retailer", "consumer"]
model = Model(attFile, connFile, len(pd.read_csv(attFile, header = None))//2, len(pd.read_csv(attFile, header = None))//2, roleOrder)

for i in range(4):
    model.step()

agent_db = model.datacollector.get_agent_vars_dataframe()
agent_db.to_csv('dendi_test.csv', ',')





