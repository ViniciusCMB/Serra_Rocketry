import pandas as pd
from fpdf import FPDF
import plotly.graph_objects as go
# import plotly.io as pio
# pio.templates.default = "plotly_dark"
from dash import html, Input, Output, callback, ctx, dcc, State
import time
import dash
import base64
import io


dash.register_page(__name__, name="Voo", path="/analise_voo")


layout = html.Div([html.Div(dcc.Upload(id='upload-data', children=html.Button(children=html.H3('Selecione o arquivo'), className='button')), className='upload-data-div'),
                   html.Div(id='output-data-upload'),
                   ])
