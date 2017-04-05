import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import weather
# Import data from csv
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

# Plot data in the notebook
py.iplot(fig, filename='simple-plot-from-csv')