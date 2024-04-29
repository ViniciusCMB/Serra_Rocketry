import dash
import time
from dash import Dash, Input, Output, html, ctx, State, callback, dcc
import dash_daq as daq
import requests


dash.register_page(__name__, name="Ignitor",
                   path="/ignitor")

layout = html.Center([
    html.H1('Controle de ignitor', style={'margin-bottom':'10px'}),
    daq.LEDDisplay(id="contagem", value=10, color="#FF5E5E", size=64, backgroundColor="#323249"),
    dcc.Interval(
        id="trigger-while-button-on", interval=1000, n_intervals=0
    ),
    html.Div(daq.PowerButton(
        id="start", on=False, size=100, color='#696cff'
    ), style={'margin-top':'10px'}),
    html.H3(id='on_off', style={'margin-top':'10px'}),
], className='card'
)


@callback(
    Output("contagem", "value"),
    Input("trigger-while-button-on", "n_intervals"),
    Input("start", "on"),
    Input("contagem", "value"),
)
def update_output(n, start_watch, led_value):
    input_value = 10
    if input_value != None and start_watch == False:
        return int(input_value)
    if n >= 0 and start_watch == True:
        if led_value > 0:
            led_value -= 1
            return led_value
        if led_value == 0:
            return led_value
    return led_value

@callback(
        Output("on_off", "children"),
        Input("contagem", "value")
)
def on_off(value):
    if value == 0:
        requests.get('http://192.168.4.1/on')
        return 'Ativado'
    else:
        requests.get('http://192.168.4.1/off')
    return 'Desativado'
