import os
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from osgeo import gdal, ogr
import momepy
import pysal as ps
import numpy as np
from pylab import figure, scatter, show


# set the filepath and load in a shapefile
fp = r'9333c7bd-3d68-4a0f-8e3f-e2d2f9fe692e2020329-1-y5g7b3.h6mmo.shp'

map_df = gpd.read_file(fp)

# Construct queen weights from the dataframe
Q_w = ps.lib.weights.Queen.from_dataframe(map_df)

# Dense matrix describing all of the pairwise relationships

Wmatrix, ids = Q_w.full()

print(Wmatrix)
#nx.draw_networkx_edge_labels(G, pos=layout)


# check data type so we can see that this is not a normal dataframe, but a GEOdataframe
print(map_df.head())
# create an array of colours
colours = ['r','g','b','y']
colour= []
size = 26
for i in range(size):
	colour.append(colours[i%len(colours)])


print(colour)


map_df['colour'] = None # add color coloumn



map_df["NEIGHBORS"] = None  # add NEIGHBORS column
nodes_edges=[]
#neighbours_dict={}
for index, county in map_df.iterrows():   
    neighbours_dict={}
    # get 'not disjoint' countries
    neighbors = map_df[~map_df.geometry.disjoint(county.geometry)].OBJECTID.tolist()
    # remove own name from the list
    neighbors = [ name for name in neighbors if county.OBJECTID != name ]
    # add names of neighbors as NEIGHBORS value
    #map_df.at[index, "NEIGHBORS"] = ", ".join(neighbors)
    # add weight of 1 to all members of neighbours
    for i in neighbors:
        neighbours_dict[i]=1
    nodes_edges.append((county.OBJECTID,neighbours_dict))


for i in nodes_edges:
	print(i)

# create a 26 * 26 matrix [26][26] having each neighbour with 1.0 and the rest as 0.0
matrix = [[0.0 for x in range(26)] for y in range(26)] 
for i in nodes_edges:
	dict = i[1]
	for j in dict:
		matrix[i[0]-1][j-1] = 1.0

print(matrix)
G = nx.from_numpy_matrix(np.matrix(Wmatrix), create_using=nx.DiGraph)
layout = nx.spring_layout(G)
nx.draw(G,layout)
plt.show()





#print(map_df)
#print(map_df.loc[map_df['ENGLISH'] == 'CORK'])


# Print map with alternate 4 colours
map_df.plot(color=map_df['color'])

# Save plot output to jpg file
plt.savefig('ireland.jpg')
