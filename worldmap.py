import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd


df= pd.read_csv("coordinates.csv",delimiter=",")

df2 = df[pd.to_numeric(df['longitude'],errors='coerce').notna()]

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lon = df2.longitude,
    lat = df2.latitude,
    name="Boat"
))

fig.update_layout(
        title = 'Current position of the boat',
        geo_scope='world',
    )
fig.show()