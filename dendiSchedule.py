from collections import defaultdict
from mesa.time import BaseScheduler
import numpy as np


class Activation(BaseScheduler):

	def __init__(self, model, roleOrder):
		super().__init__(model)
		self.agents_by_type = defaultdict(dict)
		self.roleOrder = roleOrder
		self.roleIndex = 0

	def add(self, agent):

		self._agents[agent.unique_id] = agent
		agent_class = agent.role
		self.agents_by_type[agent_class][agent.unique_id] = agent

	def remove(self, agent):

		del self._agents[agent.unique_id]

		agent_class = agent.role
		del self.agents_by_type[agent_class][agent.unique_id]

	def step(self):
		role = self.roleOrder[self.roleIndex]
		agentKeys = list(self.agents_by_type[role].keys())
		for agentKey in agentKeys:
			agent = self.agents_by_type[role][agentKey]
			agent.step()
		self.steps += 1
		self.time += 1
		self.roleIndex = (self.roleIndex + 1)%4
		# super().step()