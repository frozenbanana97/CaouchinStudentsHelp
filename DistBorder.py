import pandas as pd
import geopandas as gpd

# Import border line file
borderLine = gpd.read_file('CaaporaFragmentEdge.gpkg', layer='EdgeLine')
border = borderLine.unary_union

# Import data, should be lat long decimal ex: -7.35, -34.51
df = pd.read_excel('data.xlsx')
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
gdf = gdf.set_crs('EPSG:4326')
gdf = gdf.to_crs('EPSG:31985')

# Calculate distance of each point in the group to the centroid and border
# Calcular a distância de cada ponto no grupo para o centroide e fronteira
for row in gdf['geometry']:
    # Apply to the scan geodataframe / Aplicar ao geodataframe de varredura
    # gdf.loc[:,'distCentr'] = gdf.distance(centroid[0])
    gdf.loc[:,'distBorder'] = gdf.distance(border)

# cenList = gdf['distCentr'].tolist()
borList = gdf['distBorder'].tolist()
gdf.to_file('DistBorder.gpkg', driver='GPKG', layer='points')
gdf.to_csv('DistBorder.csv', index=False)
gdf.head()