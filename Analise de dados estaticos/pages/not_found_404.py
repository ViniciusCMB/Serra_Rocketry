from dash import html
import dash

dash.register_page(__name__, path="/404")

layout = html.Div(
    html.H2('Página não encontrada - 404 Not Found'), className="card", style={"text-align": "center"})
