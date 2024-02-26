import serial
import time
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly
import plotly.graph_objs as go


dash.register_page(__name__, name="Real Time", path="/real_time")


try:  # Tenta se conectar, se conseguir, o loop se encerra
    arduino = serial.Serial('/COM5', 9600)
    print('Arduino conectado')
except:
    layout = html.Div(
        html.H2('Não foi possível conectar.'), className="card", style={"text-align": "center"})

layout = html.Div(
    html.Div([
        dcc.Graph(id='graph-live-update'),
        dcc.Interval(
            id='interval-component',
            interval=1*100,  # in milliseconds
            n_intervals=0
        )
    ], className='card')
)

fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
fig['layout']['margin'] = {
    'l': 30, 'r': 10, 'b': 30, 't': 10
}

data = {
    'Time': [],
    'Temperature': [],
    'Humidity': []
}


@callback(Output('graph-live-update', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    # arduino.write('a'.encode())
    msg = str(arduino.readline())  # Lê os dados em formato de string
    msg = msg[2:-5]  # Fatia a string

    print(msg)
    z, x = msg.split(';')
    d = time.ctime()
    data['Time'].append(d)
    data['Temperature'].append(z)
    data['Humidity'].append(x)

    fig.append_trace(go.Scatter(x=data['Time'], y=data['Temperature'], mode='markers+lines', showlegend=False, name='Temperatura (°C)',
                                marker=dict(size=16, cmin=0), line=dict(color='black', width=2)), 1, 1)
    fig.append_trace(go.Scatter(x=data['Time'], y=data['Humidity'], mode='markers+lines', showlegend=False, name='Umidade (%)',
                                marker=dict(size=16, cmin=0), line=dict(color='black', width=2)), 2, 1)

    arduino.flush()

    return fig
