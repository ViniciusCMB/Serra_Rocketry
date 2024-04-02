from ast import In
import dash
from dash import Dash, dcc, html, Input, Output, callback
import requests

dash.register_page(__name__, name="Ignitor", path="/ignitor")

layout = html.Div([
    html.H1('Controle do Ignitor'),
    html.Div([html.Div(id='led-status'),
              html.Button('Iniciar', id='led-control', value='on', className='button'),
              html.Button('Cancelar', id='led-control', value='off', className='button'),
    ])
], className='card')


@callback(
    Output('led-status', 'children'),
    [Input('led-control', 'value')]
)
def update_led_status(estado):
    if estado == 'on':
        return html.Div([html.H2(id='contagem'),
                         dcc.Interval(
                                id='interval-component',
                                interval=1*1000,  # in milliseconds
                                n_intervals=10)])
    elif estado == 'off':
        requests.post('http://192.168.0.57/off')
        return False

@callback(Output('contagem', 'children'),Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    if n == 10:
        requests.post('http://192.168.0.57/on')
        return 'Ignitor ligado!'
    return f'Contagem regressiva: {10-n}'
