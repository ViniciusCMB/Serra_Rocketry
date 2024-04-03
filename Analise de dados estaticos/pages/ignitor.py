import dash
from dash import Dash, Input, Output, html, dcc, State, callback
import requests

dash.register_page(__name__, name="Ignitor",
                   path="/ignitor")

