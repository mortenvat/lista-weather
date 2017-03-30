import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
import time


username = 'mortenv'
api_key = '6aOk32PhEvHZsUmDvV16'
stream_token = 'uan67ed6r7'

py.sign_in(username, api_key)

trace1 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token,
        maxpoints=200
    )
)

layout = Layout(
    title='Raspberry Pi Streaming Sensor Data'
)

fig = Figure(data=[trace1], layout=layout)

py.plot(fig, filename='Raspberry Pi Streaming Example Values')


i = 0
stream = py.Stream(stream_token)
stream.open()

while True:
        import weather
        sensor_data = weather.get_sense_data()
        stream.write({'x': i, 'y': sensor_data})
        i += 1
        time.sleep(0.25)
