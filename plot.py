# Get this figure: fig = py.get_figure("https://plot.ly/~mortenv/0/")
# Get this figure's data: data = py.get_figure("https://plot.ly/~mortenv/0/").get_data()
# Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="Raspberry Pi Streaming Example Values", fileopt="extend")
# Get y data of first trace: y1 = py.get_figure("https://plot.ly/~mortenv/0/").get_data()[0]["y"]

# Get figure documentation: https://plot.ly/python/get-requests/
# Add data documentation: https://plot.ly/python/file-options/

# If you're using unicode in your file, you may need to specify the encoding.
# You can reproduce this figure in Python with the following code!

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
from plotly.graph_objs import *
username = mortenvat
api_key = 6aOk32PhEvHZsUmDvV16
py.sign_in('username', 'api_key')
trace1 = {
  "x": ["2017-03-30 12:42", "2017-03-30 12:42", "2017-03-30 12:43", "2017-03-30 12:43", "2017-03-30 12:44", "2017-03-30 12:44", "2017-03-30 12:45", "2017-03-30 12:45", "2017-03-30 12:46", "2017-03-30 12:46", "2017-03-30 12:47", "2017-03-30 12:47", "2017-03-30 12:48", "2017-03-30 12:48", "2017-03-30 12:49"], 
  "y": ["20.8", "21.2", "21.2", "21.3", "21.6", "21.4", "21.5", "21.4", "21.4", "21.5", "21.4", "21.5", "21.5", "21.2", "21.3"], 
  "mode": "lines", 
  "name": "temp1", 
  "type": "scatter", 
  "uid": "08dc4e", 
  "xsrc": "mortenv:6:864243", 
  "ysrc": "mortenv:6:779221"
}
trace2 = {
  "x": ["2017-03-30 12:42", "2017-03-30 12:42", "2017-03-30 12:43", "2017-03-30 12:43", "2017-03-30 12:44", "2017-03-30 12:44", "2017-03-30 12:45", "2017-03-30 12:45", "2017-03-30 12:46", "2017-03-30 12:46", "2017-03-30 12:47", "2017-03-30 12:47", "2017-03-30 12:48", "2017-03-30 12:48", "2017-03-30 12:49"], 
  "y": ["20.7", "21.0", "21.1", "21.1", "21.3", "21.3", "21.3", "21.3", "21.3", "21.3", "21.3", "21.4", "21.3", "21.1", "21.2"], 
  "mode": "lines", 
  "name": "temp2", 
  "type": "scatter", 
  "uid": "c81950", 
  "xsrc": "mortenv:6:864243", 
  "ysrc": "mortenv:6:3ad1a1"
}
trace3 = {
  "x": ["2017-03-30 12:42", "2017-03-30 12:42", "2017-03-30 12:43", "2017-03-30 12:43", "2017-03-30 12:44", "2017-03-30 12:44", "2017-03-30 12:45", "2017-03-30 12:45", "2017-03-30 12:46", "2017-03-30 12:46", "2017-03-30 12:47", "2017-03-30 12:47", "2017-03-30 12:48", "2017-03-30 12:48", "2017-03-30 12:49"], 
  "y": ["26.0", "25.6", "26.0", "26.1", "26.3", "25.5", "26.6", "25.7", "26.1", "25.8", "25.5", "26.4", "26.3", "25.9", "25.8"], 
  "mode": "lines", 
  "name": "fuktighet", 
  "type": "scatter", 
  "uid": "e4f9fa", 
  "xsrc": "mortenv:6:864243", 
  "ysrc": "mortenv:6:0ec6e2"
}
data = Data([trace1, trace2, trace3])
layout = {
  "hovermode": "closest", 
  "showlegend": True, 
  "title": "", 
  "xaxis": {
    "autorange": True, 
    "range": ["2017-03-30 12:42", "2017-03-30 12:49"], 
    "title": " ", 
    "type": "date"
  }, 
  "yaxis": {
    "autorange": True, 
    "range": [20.3722222222, 26.9277777778], 
    "title": "Click to enter Y axis title", 
    "type": "linear"
  }
}
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)