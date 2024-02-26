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


dash.register_page(__name__, name="Análise de Teste Estático", path="/analise_teste_estatico")


def nd_simp(y, h):

    soma_ci_1 = 0.0
    soma_ci_2 = 0.0
    soma_ci_3 = 0.0

    for i in range(len(y)):
        if i == 0 or i == len(y)-1:
            soma_ci_1 += y.iloc[i]
        elif i % 3 == 0 and i != 0 and i != len(y)-1:
            soma_ci_2 += y.iloc[i]
        else:
            soma_ci_3 += y.iloc[i]

    return (3*h/8)*(soma_ci_1+(2*soma_ci_2)+(3*soma_ci_3))


def calc_integral(x, y):
    dados_result = {'Info': ['Integral', 'MaxxE', 'MaxyE', 'MedioE', 'Pontos', 'Duração', 'Classificação', 'Nome'],
                    'Valor': [0.0, 0.0, 0.0, 0.0, '', '', '', '']}
    global df_result
    df_result = pd.DataFrame(dados_result)
    df_result.at[4, 'Valor'] = len(x)
    df_result.at[5, 'Valor'] = x.iloc[-1]-x.iloc[0]
    df_result.at[0, 'Valor'] = nd_simp(y, ((x.iloc[-1]-x.iloc[0])/(len(x)-1)))
    df_result.at[3, 'Valor'] = (
        1/(x.iloc[-1]-x.iloc[0]))*df_result.at[0, 'Valor']
    df_result.at[6, 'Valor'] = classe(
        df_result.at[0, 'Valor'], df_result.at[3, 'Valor'], df_result.at[5, 'Valor'])

    return None


def classe(total, medio, tempo):
    if total <= 0.0625:
        designation = '1/4A'
    elif total > 0.625 and total <= 1.25:
        designation = '1/2A'
    elif total > 1.25 and total <= 2.5:
        designation = 'A'
    elif total > 2.5 and total <= 5:
        designation = 'B'
    elif total > 5 and total <= 10:
        designation = 'C'
    elif total > 10 and total <= 20:
        designation = 'D'
    elif total > 20 and total <= 40:
        designation = 'E'
    elif total > 40 and total <= 80:
        designation = 'F'
    elif total > 80 and total <= 160:
        designation = 'G'
    elif total > 160 and total <= 320:
        designation = 'H'
    elif total > 320 and total <= 640:
        designation = 'I'
    elif total > 640 and total <= 1280:
        designation = 'J'
    elif total > 1280 and total <= 2560:
        designation = 'K'
    elif total > 2560 and total <= 5120:
        designation = 'L'
    elif total > 5120 and total <= 10240:
        designation = 'M'
    else:
        designation = 'ERRO'
        return designation

    return f"{designation}{medio:.1f} - {tempo:.1f}"


def save(file, ndf, fig):
    fig.write_image(file+'.png')
    with pd.ExcelWriter(file+'.xlsx') as writer:
        ndf.to_excel(writer, sheet_name='Dados do teste')
        df_result.to_excel(writer, sheet_name='Resultados do teste')

    class PDF(FPDF):
        def header(self):
            # Logos
            self.image(
                'Analise de dados estaticos/assets/LOGO - ALTERNATIVA.png', 210-47, -5, 50)
            self.image(
                'Analise de dados estaticos/assets/logomarca-uerj-300x300.png', 2, 2, 35)

            self.set_font('Arial', 'B', 25)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(30, 25, 'Relatório de Teste Estático', 0, 0, 'C')
            # Line break
            self.ln(20)
            self.set_fill_color(r=43, g=18, b=76)
            self.set_y(45)
            self.cell(0, 1, ' ', 0, 1, 'C', 1)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) +
                      '/{nb}' + ' - Equipe Serra Rocketry', 0, 0, 'C')

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_xy(15, 50)
    pdf.set_font('Times', 'B', 20)
    pdf.cell(0, 10, '{}'.format(df_result.at[7, 'Valor']), 0, 0, 'C', 0)
    pdf.set_xy(15, 60)
    pdf.set_font('Times', '', 18)
    pdf.multi_cell(0, 10, 'Data do teste: {}'.format(df_dados.at[0, 'Data']) +
                   '\nHorário do teste: {}'.format(df_dados.at[0, 'Hora']))

    pdf.set_xy(15, 75)
    pdf.set_font('Times', '', 14)
    pdf.multi_cell(0, 8, '\nImpulso Total (N*s) = {:.3f}'.format(df_result.at[0, 'Valor']) +
                   '\nEmpuxo Médio (N) = {:.3f}'.format(df_result.at[3, 'Valor']) +
                   '\nEmpuxo Máximo (N) = {:.3f}'.format(df_result.at[2, 'Valor']) +
                   '\nTempo aproximado de queima (s)= {:.1f}'.format(df_result.at[5, 'Valor']), 0, 1)

    pdf.set_xy(105, 83)
    pdf.set_font('Times', '', 50)
    pdf.cell(0, 10, '{}'.format(df_result.at[6, 'Valor']))

    pdf.set_fill_color(r=43, g=18, b=76)
    pdf.set_y(120)
    pdf.cell(0, 1, ' ', 0, 1, 'C', 1)
    pdf.image(file+'.png', (210/2)-90, 130, 180, 140)
    pdf.output(file+'.pdf', 'F')

    return None


layout = html.Div([html.Div(dcc.Upload(id='upload-data', children=html.Button(children=html.H3('Selecione o arquivo'), className='button')), className='upload-data-div'),
                   html.Div(id='output-data-upload'),
                   ])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if 'txt' in filename:
        df2 = pd.read_csv(io.StringIO(
            decoded.decode('utf-8')), sep='\t', header=None)
        df3 = df2.iloc[:, 0].str.split(';', expand=True)
        yi2 = []
        xii2 = []
        data2 = df3[0].tolist()
        h2 = df3[1].tolist()
        for i in range(len(df3[2])):
            yi2.append((float(df3[2].iloc[i])) * 9.81)
            xii2.append(float(df3[3].iloc[i]) / 1000)
        dados = {'Data': data2, 'Hora': h2, 'Força': yi2,
                 'Tempo Bruto': xii2, 'Tempo de Queima': ''}
        global df_dados
        df_dados = pd.DataFrame(dados)
        list = df_dados['Força'].tolist()

    else:
        return html.H3('Ocorreu um erro ao processar este arquivo.', className='card', style={'color': '#FF0000', 'text-align': 'center'})

    current_time = time.ctime()
    return html.Div([html.Div([html.Div([html.H5(filename),
                                         html.H5(current_time)], id='doc-info', className='card'),
                               html.Div([html.H4('Intervalo de amostras:', style={'margin-bottom': '10px'}),
                                         html.Div([html.Div([html.H5('Selecione o início do intervalo:', style={'margin-left': '10px'}),
                                                             html.Div(dcc.Dropdown(id='start', style={'width': '50%', 'position': 'absolute', 'right': '30px', 'font-size': 'medium', 'background-color': '#cbcbe2'}, options=[
                                                                 {'label': list[i], 'value': i} for i in range(len(list))], value=0, clearable=False), style={'color': 'black'})
                                                             ], style={'display': 'flex', 'margin-bottom': '20px'}),
                                                   html.Div([html.H5('Selecione o fim do intervalo:', style={'margin-left': '10px'}),
                                                             html.Div(dcc.Dropdown(id='end', style={'width': '50%', 'position': 'absolute', 'right': '30px', 'font-size': 'medium', 'background-color': '#cbcbe2'}, options=[
                                                                 {'label': list[i], 'value': i} for i in range(len(list))], value=len(list)-1, clearable=False), style={'color': 'black'})
                                                             ], style={'display': 'flex', 'margin-bottom': '20px'})
                                                   ])
                                         ], id='intervalo', className='card'),
                               ], id='info-intervalo'),
                     html.Div([html.Div([dcc.Graph(id='graph', responsive=True),
                                         ], className='card'),
                               html.Div([html.Div(id='analysis'),
                                         dcc.Input(
                                   id='name', type='text', placeholder='Nome do teste'),
                                   html.Div(id='notpass'),
                                   html.Button(children=html.H3(
                                       'Salvar análise'), id='save', n_clicks=0, className='button'),
                                   html.Div(id='analysis-save'),
                                   dcc.Input(
                                   id='pass', type='hidden'),
                               ], id='result', className='card')
                               ], id='graph-analysis')
                     ])


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children


@callback(
    [Output(component_id='graph', component_property='figure'),
        Output(component_id='analysis', component_property='children')],
    [Input(component_id='start', component_property='value'),
        Input(component_id='end', component_property='value'), ]
)
def update_graph(input_data, input_data2):
    ndf = df_dados[input_data:input_data2]
    ndf['Tempo de Queima'] = ndf['Tempo Bruto'] - \
        ndf.at[input_data, 'Tempo Bruto']
    calc_integral(ndf['Tempo de Queima'], ndf['Força'])
    max_x = 0.0
    max_y = 0.0
    for i in range(len(ndf)):
        temp = ndf.at[i+input_data, 'Força']
        if max_y < temp:
            max_x = ndf.at[i+input_data, 'Tempo de Queima']
            df_result.at[1, 'Valor'] = max_x
            max_y = temp
            df_result.at[2, 'Valor'] = max_y

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ndf['Tempo de Queima'], y=ndf['Força'], mode='markers+lines', name='Empuxo',
                             marker=dict(size=16, cmin=0, color=ndf['Força'], colorscale='turbo', colorbar=dict(title='Empuxo (N)')), line=dict(color='black', width=2)))
    fig['layout'].update(height=600, width=800,
                         xaxis_title='Tempo de Queima (s)', yaxis_title='Empuxo (N)', xaxis=dict(tickformat='.2f', dtick=0.5))

    result = html.Div([html.Div([html.H3('Resultados:'),
                                 html.H4(children='Data do teste: {}'.format(
                                     df_dados.at[0, 'Data'])),
                                 html.H4(children='Horário do teste: {}'.format(
                                     df_dados.at[0, 'Hora'])),
                                 html.H4(
        children='Impulso Total (N*s) ≈ {:.3f}'.format(df_result.at[0, 'Valor'])),
        html.H4(children='Empuxo médio (N) ≈ {:.3f}'.format(
            df_result.at[3, 'Valor'])),
        html.H4(children='Empuxo máximo (N) ≈ {:.3f}'.format(
            df_result.at[2, 'Valor'])),
        html.H4(children='Tempo aproximado de queima (s) ≈ {:.1f}'.format(
            df_result.at[5, 'Valor'])),
        html.H3(children='Classe: {}'.format(
            df_result.at[6, 'Valor'])),
    ])
    ])

    return fig, result


@callback(
    [Output(component_id='notpass', component_property='children'),
        Output(component_id='pass', component_property='value')],
    [Input(component_id='name', component_property='value'),
        Input(component_id='save', component_property='n_clicks')],
    prevent_initial_call=True
)
def update_name(name, n_clicks):
    if 'save' == ctx.triggered_id:
        if name is not None:
            df_result.at[7, 'Valor'] = name
            return None, 1
        else:
            alerta = html.H5('Informe um nome para o teste!!')
            return alerta, None
    else:
        return None, None


@callback(
    Output(component_id='analysis-save', component_property='children'),
    [Input(component_id='start', component_property='value'),
        Input(component_id='end', component_property='value'),
        Input(component_id='save', component_property='n_clicks'),
        Input(component_id='pass', component_property='value'),
        Input(component_id='name', component_property='value')],
    prevent_initial_call=True
)
def download(input_data, input_data2, n_clicks, passw, nome):
    if passw == 1:
        if 'save' == ctx.triggered_id:
            ndf = df_dados[input_data:input_data2]
            ndf['Tempo de Queima'] = ndf['Tempo Bruto'] - \
                ndf.at[input_data, 'Tempo Bruto']
            calc_integral(ndf['Tempo de Queima'], ndf['Força'])

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=ndf['Tempo de Queima'], y=ndf['Força'], mode='markers+lines', name='Empuxo',
                                      marker=dict(size=16, cmin=0, color=ndf['Força'], colorscale='turbo', colorbar=dict(title='Empuxo (N)')), line=dict(color='black', width=2)))
            fig2['layout'].update(height=600, width=800, title='Empuxo x Tempo de Queima',
                                  xaxis_title='Tempo de Queima (s)', yaxis_title='Empuxo (N)', xaxis=dict(tickformat='.2f', dtick=0.5))
            save(nome, ndf, fig2)
            return None
        else:
            return None
    else:
        return None
