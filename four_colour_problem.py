import geopandas as gpd
import matplotlib.pyplot as plt

# Create an array of colours
# Parameters: the colouring order
# Returns: a list of colours in the assgined order of the parameter
def colouring(colour_order):
    colours = ['r','g','b','y']
    colour = []
    for i in colour_order:
        colour.append(colours[i-1])
    return colour

# Finds all the neighbours of each county adding each county the first index of the tuples with it's neighbours to the second index of tuples as a dictionary with a key being the neighbour and the value weight of 1
# Parameters: shapefile as a Dataframe
# Returns: A list of tuples
def find_neighbours(map_df):
    nodes_edges=[]
    for index, county in map_df.iterrows():
        neighbours_dict={}
        # get 'not (tilda operator) disjoint' of counties by returning all the OBJECTID where its boundary and interior does intersect
        neighbours = map_df[~map_df.geometry.disjoint(county.geometry)].OBJECTID.tolist()
        # remove own name from the list as this would be part of the not disjoint list
        neighbours = [ name for name in neighbours if county.OBJECTID != name ]
        # add weight of 1 to all members of neighbours
        for i in neighbours:
            neighbours_dict[i]=1
        nodes_edges.append((county.OBJECTID,neighbours_dict))
    return nodes_edges

# create a matrix [length of array][length of array] having each neighbour with 1.0 and the rest as 0.0
# Parameters: Takes a list of tuples
# Returns: a 2-d array
def create_matrix(nodes_edges):
    matrix = [[0.0 for x in range(len(nodes_edges))] for y in range(len(nodes_edges))]
    for i in nodes_edges:
        dict = i[1]
        for j in dict:
            matrix[i[0]-1][j-1] = 1.0

    return matrix

# Draw graph from nodes and edges
#G = nx.from_numpy_matrix(np.matrix(Wmatrix), create_using=nx.DiGraph)
#layout = nx.spring_layout(G)
#nx.draw(G,layout)
#plt.show()


# A utility function to check if the current color assignment
# is safe for vertex v
# Parameter: graph(2-d array),v (current row), colour(a 1-d array), c (current colour int)
# Return: True if no other neighbour has the same colour (this is done by checking all 1's on the same row) is the same else False
def is_safe(graph, v, colour, c):
    for i in range(len(graph)):
        if (graph[v][i] == 1 and colour[i] == c):
            return False
    return True

# A recursive utility function to solve m
# coloring  problem
# Parameter: graph(2-d array, type:list),v (current row, type:int), colour(a 1-d array, type:list), c (current colour, type:int)
# Return: True when we reach the end of the graph else None by keep recursively looping through until we is_safe returns false for all colour options i.e. can't solve problem
def graph_colour_util(graph, m, colour, v):
    if(v == len(graph)):
        return True

    for c in range(1, m+1):
        if(is_safe(graph,v, colour, c) == True):
            colour[v] = c
            if(graph_colour_util(graph,m, colour, v+1) == True):
                return True
            colour[v] = 0

def graph_colouring(graph, m):
    colour = [0.0] * len(graph)
    if(graph_colour_util(graph,m, colour, 0) == None):
        return False
    return (colouring(colour))


# set the filepath and load in a shapefile
fp = r'data/9333c7bd-3d68-4a0f-8e3f-e2d2f9fe692e2020329-1-y5g7b3.h6mmo.shp'

# Create a dataframe of the data file using geopandas
map_df = gpd.read_file(fp)

# check data type so we can see that this is not a normal dataframe, but a GEOdataframe
#print(map_df.head())

# Create a list of tuples nothing all the neighbours of each county
nodes_edges = find_neighbours(map_df)

# From the list of tuples containning nodes and edges convert this into an adjacency matrix
matrix = create_matrix(nodes_edges)

# Number of colours
n = 4

# Get list of colours each node is assigned
colours = graph_colouring(matrix,n)

if(colours != False):
    # Print the solution
    print("Solution found")
    # Print map with alternate 4 colours
    map_df.plot(color=colours)

    # Save plot output to jpg file
    plt.savefig('ireland.jpg')
else:
    print("Solution cannot be found")

