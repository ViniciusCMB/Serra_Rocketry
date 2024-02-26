from dash import html


def create_navbar():
    navbar = html.Header([html.Img(src='assets/LOGO - SEM TEXTO.png', style={'width': '100px', 'height': '100px', 'flex': 'none', 'margin-left': '10px'}),
                          html.H1('Serra Rocketry', style={
                                  'flex': 'auto', 'margin-left': '10px'}),
                          html.Nav([html.A('Home', href='/'),
                                    html.A('Real time', href='/real_time'),
                                    html.A('Analise de teste estático', href='/analise_teste_estatico'),
                                    html.A('Analise de voo', href='/analise_voo')], style={'display': 'flex', 'margin-right': '15px'})
                             

                          ], className='card', style={'border-radius': '0px', 'margin': '0px', 'margin-bottom': '10px', 'border': '0px', 'border-bottom': '2px solid #232333', }
    )

    return navbar
