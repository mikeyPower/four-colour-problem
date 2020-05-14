import os
import geopandas as gpd
import matplotlib.pyplot as plt

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


map_df['color'] = colour



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

for index, row in map_df.iterrows();

	# See if any of it's neighbours has the same colour
	for i in row[-1]:

		# Obtain the neighbours row based on the county's name
		new_row = map_df.loc[map_df['ENGLISH'] == i])

		if(new_row[-2] == row[-2]):
			



# save GeoDataFrame as a new file
#map_df.to_file("newfile.shp")


#colour=['r', 'g', 'b', 'y']

map_df.plot(color=map_df['color'])

plt.savefig('ireland.jpg')
