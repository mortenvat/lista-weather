import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
import time
import pandas as pd
import numpy as np


username = 'mortenv'
api_key = '6aOk32PhEvHZsUmDvV16'
stream_token = 'uan67ed6r7'

py.sign_in(username, api_key)

df = pd.read_csv('testklasserom.csv')
df.head()

trace1 = go.Scatter(
                    x=df['tidspunkt'], y=df['temp1'], # Data
                    mode='lines', name='temp1' # Additional options
                   )
trace2 = go.Scatter(x=df['tidspunkt'], y=df['temp2'], mode='lines', name='temp2' )
trace3 = go.Scatter(x=df['tidspunkt'], y=df['fuktighet'], mode='lines', name='fuktighet')

layout = go.Layout(title='testklasserom',
                   plot_bgcolor='rgb(230, 230,230)')

fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)


i = 0
stream = py.Stream(stream_token)
stream.open()

while True:
        import weather
        sensor_data = weather.get_sense_data()
        stream.write({'x': i, 'y': sensor_data})
        i += 1
        time.sleep(0.25)
