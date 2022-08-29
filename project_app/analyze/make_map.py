import pandas as pd
import json
import requests
import branca
import folium

url = 'https://raw.githubusercontent.com/suanlab/dataset/master'
skorea_municipalities_geo = f'{url}/skorea-municipalities-2018-geo.json'
skorea_municipalities_population = f'{url}/skorea_municipalities_population.csv'
skorea_municipalities_df = pd.read_csv(skorea_municipalities_population, encoding = 'utf-8')

m = folium.Map(
location = [36.4136816, 127.8203656],
zoom_start=7
)

folium.GeoJson(
    skorea_municipalities_geo,
    name = 'skorea-municipalities'
).add_to(m)

m.save('map.html')