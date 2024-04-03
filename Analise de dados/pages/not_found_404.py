from dash import html
import dash


# Registre a página com o caminho "/404"
dash.register_page(__name__, path="/404")

# Defina o layout da página 404
layout = html.Div(
    html.H2('Página não encontrada - 404 Not Found'), className="card", style={"text-align": "center"})
