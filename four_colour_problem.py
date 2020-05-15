import os
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from osgeo import gdal, ogr

# set the filepath and load in a shapefile
fp = '9333c7bd-3d68-4a0f-8e3f-e2d2f9fe692e2020329-1-y5g7b3.h6mmo.shp'

map_df = gpd.read_file(fp)
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

for index, county in map_df.iterrows():   
    # get 'not disjoint' countries
    neighbors = map_df[~map_df.geometry.disjoint(county.geometry)].ENGLISH.tolist()
    # remove own name from the list
    neighbors = [ name for name in neighbors if county.ENGLISH != name ]
    # add names of neighbors as NEIGHBORS value
    map_df.at[index, "NEIGHBORS"] = ", ".join(neighbors)

for field in map_df:
	print(field)

print(map_df)
#print(map_df.loc[map_df['ENGLISH'] == 'CORK'])

#for index, row in map_df.iterrows();


	# See if any of it's neighbours has the same colour
#	for i in row[-1]:

		# Obtain the neighbours row based on the county's name
#		new_row = map_df.loc[map_df['ENGLISH'] == i])
		# see if colour of neighbour is the same

#		if(new_row[-2] == row[-2]):
			# if the same change colour of row[-2]
#		else:
			# check next neighbouring county
#			continue


# save GeoDataFrame as a new file
#map_df.to_file("newfile.shp")


#colour=['r', 'g', 'b', 'y']


# Converting shapefile to graph
G=nx.read_shp(fp) 
pos = {k: v for k,v in enumerate(G.nodes())}
X=nx.Graph() #Empty graph
X.add_nodes_from(pos.keys()) #Add nodes preserving coordinates
l=[set(x) for x in G.edges()] #To speed things up in case of large objects
edg=[tuple(k for k,v in pos.items() if v in sl) for sl in l] #Map the G.edges start and endpoints onto pos
nx.draw_networkx_nodes(X,pos,node_size=100,node_color='r')
X.add_edges_from(edg)
nx.draw_networkx_edges(X,pos)
plt.xlim(450000, 470000) #This changes and is problem specific
plt.ylim(430000, 450000) #This changes and is problem specific
plt.xlabel('X [m]')
plt.ylabel('Y [m]')
plt.title('From shapefiles to NetworkX')
print(X)

# Print map with alternate 4 colours
map_df.plot(color=map_df['color'])

# Save plot output to jpg file
plt.savefig('ireland.jpg')
