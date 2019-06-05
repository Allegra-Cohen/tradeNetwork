import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import pandas as pd
from dendiRun import *
import ast
import matplotlib.pyplot as plt; plt.close('all')
from matplotlib.animation import FuncAnimation

def isInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def nodeColor(db, G, colorlist, colorAtt):
	colormap = []
	for index, row in db.iterrows():
		if colorAtt == "role":
			colormap.append(colorlist[roleOrder.index(row["role"])])
		else:
			if row["gender"] == "F":
				colormap.append("#ffacb0")
			else:
				colormap.append("#B5D8F6")
		pointsTo = ast.literal_eval(row["pointsTo"])
		G.add_edges_from(list(zip([row["unique_id"]]*len(pointsTo), pointsTo, [0]*len(pointsTo))))
	return(colormap, G)

# nx.draw(G, node_color = colormap, with_labels=True, font_weight='bold')
# plt.show()
def sizeAndEdgeColor(db, sizeAtt):
	sizemap = []
	edgecolormap = []
	for i in db["Step"].unique():
		dbStep = db.loc[db["Step"] == i]
		sizemap.append([(x + 0.5)*300 for x in dbStep[sizeAtt]]) # SIZE
		minimap = []
		for x in dbStep["unique_id"]:
			agent = dbStep.loc[dbStep["unique_id"] == x]
			pointsTo = ast.literal_eval(agent["pointsTo"].values[0])
			if pointsTo:
				for a in pointsTo:
					if a in ast.literal_eval(agent["soldTo"].values[0]):
						minimap.append('red')
					else:
						minimap.append('black')
		edgecolormap.append(minimap)
	return [sizemap, edgecolormap]


def animate_nodes(G, colormap2, sizemap2, edgecolormap2, pos=None):
	# define graph layout if None given
	if pos is None:
		pos = nx.circular_layout(G)

	# draw graph
	nodes = nx.draw_networkx_nodes(G, pos, node_color = colormap2)
	edges = nx.draw_networkx_edges(G, pos)
	plt.axis('off')

	def update(ii):
		plt.clf()
		nodes = nx.draw_networkx_nodes(G, pos, node_color = colormap2, node_size = np.array(sizemap2)[ii])
		edges = nx.draw_networkx_edges(G, pos, edge_color = edgecolormap2[ii])
		plt.axis('off')
		return nodes,

	fig = plt.gcf()
	animation = FuncAnimation(fig, update, interval=50, frames=len(sizemap), blit=True)
	return animation



# Assume you have a pandas database "db" written out that has ID, rice
db = pd.read_csv("dendi_test.csv", header = 0)
attributesDB = pd.read_csv(attFile, header = None)
connectionsDB = pd.read_csv(connFile, header = None)
G = nx.MultiDiGraph()
G.add_nodes_from(db["unique_id"]) # Add all the unique_ids as nodes
colorlist = ["#acffd2", "#5088ff", "#ff9a00", "#e5f27b"]
colorAtt = "role"
sizeAtt = "rice"

graph = nodeColor(db, G, colorlist, colorAtt)
colormap = graph[0]
G = graph[1]
details = sizeAndEdgeColor(db, sizeAtt)
sizemap, edgecolormap = details[0], details[1]
animation = animate_nodes(G, colormap, sizemap, edgecolormap)
animation.save('test.gif', writer='imagemagick', savefig_kwargs={'facecolor':'white'}, fps=0.7)





