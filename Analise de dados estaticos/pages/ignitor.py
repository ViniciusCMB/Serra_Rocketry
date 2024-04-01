import dash
from dash import Dash, dcc, html, Input, Output, callback
import requests

dash.register_page(__name__, name="Ignitor", path="/ignitor")

layout = html.Div([
    dcc.Dropdown(
        id='led-control',
        options=[
            {'label': 'Ligado', 'value': 'on'},
            {'label': 'Desligado', 'value': 'off'},
        ],
        value='off',
        clearable=False
    ),
    html.H1(id='led-status')
], className='card')


@callback(
    Output('led-status', 'children'),
    [Input('led-control', 'value')]
)
def update_led_status(estado):
    # Simulação de controle do LED
    if estado == 'on':
        # Envie sinal para ligar o LED
        requests.post('http://192.168.1.160/on')
        return 'LED aceso!'
    elif estado == 'off':
        # Envie sinal para desligar o LED
        requests.post('http://192.168.1.160/off')
        return 'LED apagado!'
