import pandas as pd
import geopandas as gpd

# Import raw data as excel file
df = pd.read_excel('natsumiData.xlsx')
df = df.drop(index=0)
df.reset_index(inplace=True, drop=True)

# south initial coordinate conversion
df['dms'] = df['Coordenadas S'].str.strip()

# split deg min sec into variables
deg = df['dms'].str[:2]
min = df['dms'].str[3:5]
sec = df['dms'].str[6:10]

df['deg'] = deg
df['min'] = min
df['sec'] = sec

df['deg'] = df['deg'].astype(float)
df['min'] = df['min'].astype(float)
df['sec'] = df['sec'].astype(float)

# convert/merge the standalone values to deimal degrees and apply -1 for south
df['Coordenadas S'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

# west initial coordinate conversion
df['dms'] = df['Coordenadas W'].str.strip()

deg = df['dms'].str[:3]
min = df['dms'].str[4:6]
sec = df['dms'].str[7:11]

df['deg'] = deg
df['min'] = min
df['sec'] = sec

df['deg'] = df['deg'].astype(float)
df['min'] = df['min'].astype(float)
df['sec'] = df['sec'].astype(float)

# convert/merge the standalone values to deimal degrees and apply -1 for south
df['Coordenadas W'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

# south final coordinate conversion
df['dms'] = df['Coordenadas S.1'].str.strip()

deg = df['dms'].str[:2]
min = df['dms'].str[3:5]
sec = df['dms'].str[6:10]

df['deg'] = deg
df['min'] = min
df['sec'] = sec

df['deg'] = df['deg'].astype(float)
df['min'] = df['min'].astype(float)
df['sec'] = df['sec'].astype(float)

# convert/merge the standalone values to deimal degrees and apply -1 for south
df['Coordenadas S.1'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

# west final coordinate conversion
df['dms'] = df['Coordenadas W.1'].str.strip()

deg = df['dms'].str[:3]
min = df['dms'].str[4:6]
sec = df['dms'].str[7:11]

df['deg'] = deg
df['min'] = min
df['sec'] = sec

df['deg'] = df['deg'].astype(float)
df['min'] = df['min'].astype(float)
df['sec'] = df['sec'].astype(float)

# convert/merge the standalone values to deimal degrees and apply -1 for south
df['Coordenadas W.1'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

# remov the temp columns for deg min sec
df.pop('dms')
df.pop('deg')
df.pop('min')
df.pop('sec')

# to gdf with geometry as initial
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Coordenadas W'],df['Coordenadas S'])) 
# set crs/projection
gdf = gdf.set_crs('EPSG:4326')
gdf = gdf.to_crs('EPSG:31985')
gdf['Coordenadas Inicial'] = gdf['geometry']
# create points for final
gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(df['Coordenadas W.1'],df['Coordenadas S.1'])) 
gdf = gdf.set_crs('EPSG:4326', allow_override=True)
gdf = gdf.to_crs('EPSG:31985')
gdf['Coordenadas Final'] = gdf['geometry']
gdf.pop('geometry')

# import edge lines
edgeLine = gpd.read_file('CaaporaFragmentEdge.gpkg', layer='EdgeLine')
edgeupperLine = gpd.read_file('CaaporaFragmentEdge.gpkg', layer='EdgeUpper')
edgelowerLine = gpd.read_file('CaaporaFragmentEdge.gpkg', layer='EdgeLower')

edge = edgeLine.unary_union
edgeupper = edgeupperLine.unary_union
edgelower = edgelowerLine.unary_union

# Dist for initial geometry
gdf.loc[:,'iniDistEdge'] = gdf['Coordenadas Inicial'].distance(edge)
gdf.loc[:,'iniDistUpEdge'] = gdf['Coordenadas Inicial'].distance(edgeupper)
gdf.loc[:,'iniDistLowEdge'] = gdf['Coordenadas Inicial'].distance(edgelower)

# Dist for final geometry
gdf.loc[:,'finDistEdge'] = gdf['Coordenadas Final'].distance(edge)
gdf.loc[:,'finDistUpEdge'] = gdf['Coordenadas Final'].distance(edgeupper)
gdf.loc[:,'finDistLowEdge'] = gdf['Coordenadas Final'].distance(edgelower)

ini50 = gdf['iniDistEdge']
fin50 = gdf['finDistEdge']

iniStat = []
for i in ini50:
    if i <= 50:
        stat='border'
        iniStat.append(stat)
    else:
        stat='interior'
        iniStat.append(stat)

finStat = []
for i in fin50:
    if i <= 50:
        stat='border'
        finStat.append(stat)
    else:
        stat='interior'
        finStat.append(stat)
        
gdf.insert(loc=13, column='initial status', value=iniStat)
gdf.insert(loc=14, column='final status', value=finStat)

gdf.to_csv('natsumiData.csv')

print('DONE')