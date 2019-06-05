# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.time import StagedActivation
import numpy as np
import pandas as pd
import random
import operator
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from dendiSchedule import *
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx


class Model(Model):
	def __init__(self, attributesFile, connectionsFile, xmax, ymax, roleOrder): # coords of map edge
		attributesDB = pd.read_csv(attributesFile, header = None)
		connectionsDB = pd.read_csv(connectionsFile, header = None)
		self.running=True
		self.grid = MultiGrid(xmax, ymax, True) # bool = toroidal
		self.schedule = Activation(self, roleOrder)

		self.agents = []

		# WALTHER DATA
		# Create agents
		for index, row in attributesDB.iterrows():
			# From attributesDB: agent id, role, gender, current $, current rice, x coord and y coord
			newAgent = Agent(row[0], self, row[1], row[2], row[3], row[4]) # Gotta assume the IDs correspond to the row number because the OECD book says it's matrix-based
			self.schedule.add(newAgent)
			self.grid.place_agent(newAgent, (row[5], row[6]))
			self.agents.append(newAgent)

		# Add links
		for index, row in connectionsDB.iterrows():
			agent = next((x for x in self.agents if x.unique_id == row[0]), None) # I'm gonna say for now you can't assume this list is ordered the way the agents are added even though that's pretty paranoid
			print(agent)
			for i in range(1, len(row)): # for column index aka other agent id
				if row[i] == 1:
					agent.pointsTo.append(next((x for x in self.agents if x.unique_id == (i - 1)), None))
					agent.pointsToIDs.append(i - 1)

		self.datacollector = DataCollector(
				agent_reporters={"unique_id": "unique_id", "gender": "gender", "role": "role", "rice": "rice", "capital": "capital", "pointsTo": "pointsToIDs", "soldTo": "soldTo"})

	def step(self):
		self.datacollector.collect(self)
		for a in self.agents:
			a.soldTo = []
			if a.role == "producer" and self.schedule.time % 4 == 0:
				a.rice = 2 # Have the producers produce every full timestep, assume they've sold everything
			if a.role == "consumer" and self.schedule.time % 4 == 3:
				a.capital += 1 # Have the consumers have an income
				a.rice = 0 # Consumers eat rice

		self.schedule.step()



class Agent(Agent):
	def __init__(self, unique_id, model, role, gender, capital, rice):
		super().__init__(unique_id, model)
		self.role = role
		self.gender = gender
		self.capital = capital
		self.rice = rice
		self.pointsTo = []
		self.pointsToIDs = []
		self.soldTo = []

	# def buy(self):

	def sell(self, agent):
		home = self.pos
		self.model.grid.move_agent(self, agent.pos)
		if self.rice > 0:
			if agent.capital > 0:
				agent.rice += 1
				agent.capital = agent.capital - 1
				self.rice = self.rice - 1
				self.capital += 1
				print(self.unique_id, " sells to ", agent.unique_id)
		self.model.grid.move_agent(self, home)

	# def addValue(self):

	# For now the only thing an agent can do is sell rice to another agent.
	def step(self):
		for agent in self.pointsTo:
			if agent != None:
				self.sell(agent)
				self.soldTo.append(agent.unique_id)






















