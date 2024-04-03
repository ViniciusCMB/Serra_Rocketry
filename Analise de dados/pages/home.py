import dash
from dash import html

# Registrando a página no Dash
dash.register_page(__name__, name="Serra Rocketry", path="/")

# Definindo o layout da página home
layout = html.Div([
    html.H2('Serra Rocketry - Equipe de Foguetemodelismo do IPRJ-UERJ'), 
    html.H3('Painel de controle de testes e análises.')
], className="card", style={"text-align": "center"})
