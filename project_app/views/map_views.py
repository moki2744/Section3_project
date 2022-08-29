from flask import Blueprint, render_template, request
import pandas as pd
from datetime import datetime
import plotly
import plotly.express as px
import json
import folium

map_bp = Blueprint('map', __name__, url_prefix='/map')

@map_bp.route('/')
def show_map():
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
    return m._repr_html_()