import pandas as pd
import geopandas as gpd
import numpy as np

df = pd.read_excel('natsumiData.xlsx')
df = df.drop(index=0) # Locus adds an empty row here, remove this line if not needed
df.reset_index(inplace=True, drop=True)

# south intial
df['dms'] = df['Coordenadas S'].str.strip()

deg = df['dms'].str[:2]
min = df['dms'].str[3:5]
sec = df['dms'].str[6:10]

df['deg'] = deg
df['min'] = min
df['sec'] = sec

df['deg'] = df['deg'].astype(float)
df['min'] = df['min'].astype(float)
df['sec'] = df['sec'].astype(float)

df['Coordenadas S'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

# west initial
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

df['Coordenadas W'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

# south final
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

df['Coordenadas S.1'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

# west final
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

df['Coordenadas W.1'] = (df['deg'] + (df['min']/60) + (df['sec']/3600)) * -1

df.pop('dms')
df.pop('deg')
df.pop('min')
df.pop('sec')

# to gdf
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Coordenadas W'],df['Coordenadas S'])) 
gdf = gdf.set_crs('EPSG:4326')
gdf = gdf.to_crs('EPSG:31985')
gdf['Coordenadas Inicial'] = gdf['geometry']
gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(df['Coordenadas W.1'],df['Coordenadas S.1'])) 
gdf = gdf.set_crs('EPSG:4326', allow_override=True)
gdf = gdf.to_crs('EPSG:31985')
gdf['Coordenadas Final'] = gdf['geometry']
gdf.pop('geometry')

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

gdf.to_csv('natsumiData.csv')