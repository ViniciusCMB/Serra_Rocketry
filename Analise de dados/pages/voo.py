import pandas as pd
import numpy as np
from fpdf import FPDF
import plotly.graph_objects as go
# import plotly.io as pio
# pio.templates.default = "plotly_dark"
from dash import html, Input, Output, callback, ctx, dcc, State
import time
import dash
import base64
import io

from sympy import half_gcdex

# Registra a página no Dash
dash.register_page(__name__, name="Análise de Voo",
                   path="/analise_voo")


# Esta função calcula a integral, preenche o dataframe de resultados e classifica o teste com base no valor da integral
def calc_duracao(x, y):
    # Cria um dataframe global com os resultados do teste
    dados_resultv = {'Info': ['MaxxA', 'MaxyA', 'VelocidadeM', 'MaxxV', 'MaxyV', 'AceleraçãoM', 'MaxxAc', 'MaxyAc', 'Pontos', 'Duração', 'Classificação', 'Nome'],
                     'Valor': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, '', '']}
    global df_resultv
    df_resultv = pd.DataFrame(dados_resultv)
    df_resultv.at[9, 'Valor'] = x.iloc[-1]-x.iloc[0]

    return None

# Esta função calcula a interpolação spline dos pontos de dados (ainda não implementada corretamente)


def spline(xi, yi):
    n = len(xi)
    a = {k: v for k, v in enumerate(yi)}
    h = {k: xi[k+1]-xi[k] for k in range(n-1)}

    A = [[1]+[0]*(n-1)]
    for i in range(1, n-1):
        linha = np.zeros(n)
        linha[i-1] = h[i-1]
        linha[i] = 2 * (h[i-1] + h[i])
        linha[i+1] = h[i]
        A.append(linha)
    A.append([0]*(n-1)+[1])

    B = [0]
    for k in range(1, n-1):
        linha = 3 * (a[k+1]-a[k])/h[k] - 3 * (a[k] - a[k-1])/h[k-1]
        B.append(linha)
    B.append(0)

    c = dict(zip(range(n), np.linalg.solve(A, B)))

    b = {}
    d = {}
    for k in range(n-1):
        b[k] = (1/h[k])*(a[k+1]-a[k])-((h[k]/3)*(2*c[k]+c[k+1]))
        d[k] = (c[k+1]-c[k])/(3*h[k])

    s = {}
    for k in range(n-1):
        eq = f'{a[k]}{b[k]:+}*(x{-xi[k]:+}){c[k]:+}*(x{-xi[k]:+})**2{d[k]:+}*(x{-xi[k]:+})**3'
        s[k] = {'eq': eq, 'dominio': [xi[k], xi[k+1]]}

    return s

# Esta função é responsável por gerar e salvar o relatório em PDF e Excel


def save(file, ndf, fig):
    fig.write_image(file+'.png')
    with pd.ExcelWriter(file+'.xlsx') as writer:
        ndf.to_excel(writer, sheet_name='Dados do teste')
        df_resultv.to_excel(writer, sheet_name='Resultados do teste')

    class PDF(FPDF):
        def header(self):
            # Logos
            self.image(
                'Analise de dados/assets/LOGO - ALTERNATIVA.png', 210-47, -5, 50)
            self.image(
                'Analise de dados/assets/logomarca-uerj-300x300.png', 2, 2, 35)

            self.set_font('Arial', 'B', 25)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(30, 25, 'Relatório de Voo', 0, 0, 'C')
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
    pdf.cell(0, 10, '{}'.format(df_resultv.at[7, 'Valor']), 0, 0, 'C', 0)
    pdf.set_xy(15, 60)
    pdf.set_font('Times', '', 18)
    pdf.multi_cell(0, 10, 'Data do teste: {}'.format(df_dadosv.at[0, 'Data']) +
                   '\nHorário do teste: {}'.format(df_dadosv.at[0, 'Hora']))

    pdf.set_xy(15, 75)
    pdf.set_font('Times', '', 14)
    pdf.multi_cell(0, 8, '\nImpulso Total (N*s) = {:.3f}'.format(df_resultv.at[0, 'Valor']) +
                   '\nAltura Médio (N) = {:.3f}'.format(df_resultv.at[3, 'Valor']) +
                   '\nAltura Máximo (N) = {:.3f}'.format(df_resultv.at[2, 'Valor']) +
                   '\nTempo aproximado de Voo (s)= {:.1f}'.format(df_resultv.at[5, 'Valor']), 0, 1)

    pdf.set_xy(105, 83)
    pdf.set_font('Times', '', 50)
    pdf.cell(0, 10, '{}'.format(df_resultv.at[6, 'Valor']))

    pdf.set_fill_color(r=43, g=18, b=76)
    pdf.set_y(120)
    pdf.cell(0, 1, ' ', 0, 1, 'C', 1)
    pdf.image(file+'.png', (210/2)-90, 130, 180, 140)
    pdf.output(file+'.pdf', 'F')

    return None


def classe(h):
    designation = ''
    distancia = ''
    if h <= 100:
        distancia = h - 100
        designation = 'H100'
    elif h > 100 and h <= 200:
        distancia = h - 200
        designation = 'H200'
    elif h > 200 and h <= 300:
        distancia = h - 300
        designation = 'H300'
    elif h > 300 and h <= 500:
        distancia = h - 500
        designation = 'H500'
    elif h > 500:
        distancia = h - 1000
        designation = 'H1K'
    else:
        designation = 'ERRO'
        return designation

    return f"{designation} ({distancia:.3f}m)"


# Layout da página
layout = html.Div([html.Div(dcc.Upload(id='upload-data', children=html.Button(children=html.H3('Selecione o arquivo'), className='button')), className='upload-data-div'),
                   html.Div(id='output-data-upload'),
                   ])

# Esta função é responsável por processar o arquivo de dados e exibir o gráfico e os resultados (apenas arquivos .txt são aceitos)


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
        dados = {'Data': data2, 'Hora': h2, 'Altura': yi2,
                 'Tempo Bruto': xii2, 'Tempo de Voo': ''}
        # Cria um dataframe global com os dados do arquivo, mais fácil de trabalhar com os dados
        global df_dadosv
        df_dadosv = pd.DataFrame(dados)
        # Essa lista é usada para criar os dropdowns de seleção de intervalo de amostras
        list = df_dadosv['Altura'].tolist()

    else:
        return html.H3('Ocorreu um erro ao processar este arquivo.', className='card', style={'color': '#FF0000', 'text-align': 'center'})

    current_time = time.ctime()

    # Retorna 3 cards: informações do arquivo e intervalo de amostras, gráfico e resultados
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

# Este callback atualiza o conteúdo exibido após o upload de um arquivo


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children

# Este callback atualiza o gráfico e a seção de análise com base no intervalo de dados selecionado


@callback(
    [Output(component_id='graph', component_property='figure'),
        Output(component_id='analysis', component_property='children')],
    [Input(component_id='start', component_property='value'),
        Input(component_id='end', component_property='value'), ]
)
def update_graph(input_data, input_data2):
    # Cria um novo dataframe com os dados do intervalo selecionado
    ndf2v = df_dadosv[input_data:input_data2]
    ndf2v['Tempo de Voo'] = ndf2v['Tempo Bruto'] - \
        ndf2v.at[input_data, 'Tempo Bruto']

    # Calcula o Tempo de Voo
    ndfv = ndf2v.reset_index(drop=True)
    calc_duracao(ndfv['Tempo de Voo'], ndfv['Altura'])

    # Interpolação spline
    sn = spline(ndfv['Tempo de Voo'], ndfv['Altura'])
    t = []
    pt = []
    for key, value in sn.items():
        def p(x):
            return eval(value['eq'])
        tx = np.linspace(*value['dominio'], 100)
        t.extend(tx)
        ptx = [p(x) for x in tx]
        pt.extend(ptx)

    def coef(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_x2 = sum([i**2 for i in x])
        sum_y = sum(y)
        sum_xy = sum([x.iloc[i]*y.iloc[i] for i in range(n)])
        A = [[n, sum_x], [sum_x, sum_x2]]
        B = [sum_y, sum_xy]

        return np.linalg.solve(A, B)

    def velocidade(x, a, b):
        return (a*x)+b

    acel = []
    vel = []
    for i in range(len(df_resultv)-1):
        atemp, btemp = coef(
            ndfv.loc[i:i+2, 'Tempo de Voo'], ndfv.loc[i:i+2, 'Altura'])
        acel.append(atemp)
        vel.append(velocidade(ndfv.at[i, 'Tempo de Voo'], atemp, btemp))

    df_resultv.at[2, 'Valor'] = np.mean(vel)
    df_resultv.at[4, 'Valor'] = max(vel)
    df_resultv.at[3, 'Valor'] = t[vel.index(max(vel))]
    df_resultv.at[5, 'Valor'] = np.mean(acel)
    df_resultv.at[7, 'Valor'] = max(acel)
    df_resultv.at[6, 'Valor'] = t[acel.index(max(acel))]
    df_resultv.at[1, 'Valor'] = max(pt)
    df_resultv.at[0, 'Valor'] = t[pt.index(max(pt))]
    df_resultv.at[10, 'Valor'] = classe(df_resultv.at[1, 'Valor'])

    # Criando o gráfico com os dados de Tempo de Voo e Altura
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=pt, mode='lines',
                  name='Interpolação', line=dict(color='black', width=2)))
    fig.add_trace(go.Scatter(x=ndfv['Tempo de Voo'], y=ndfv['Altura'], mode='markers', name='Altura',
                             marker=dict(size=16, cmin=0, color=ndfv['Altura'], colorscale='turbo', colorbar=dict(title='Altura (m)')), line=dict(color='black', width=2)))

    fig['layout'].update(height=600, width=800,
                         xaxis_title='Tempo de Voo (s)', yaxis_title='Altura (m)', xaxis=dict(tickformat='.2f', dtick=0.5), legend=dict(
                             orientation="h",
                             yanchor="bottom",
                             y=1.02,
                             xanchor="right",
                             x=1))

    # Criando a seção de análise com os resultados
    result = html.Div([html.Div([html.H3('Resultados:'),
                                 html.H4(children='Data do Voo: {}'.format(
                                     df_dadosv.at[0, 'Data'])),
                                 html.H4(children='Horário do Voo: {}'.format(
                                     df_dadosv.at[0, 'Hora'])),
                                 html.H4(
        children='Altura Máxima (m) ≈ {:.3f}'.format(df_resultv.at[1, 'Valor'])),
        html.H4(children='Velocidade média (m/s) ≈ {:.3f}'.format(
            df_resultv.at[2, 'Valor'])),
        html.H4(children='Velocidade máxima (m/s) ≈ {:.3f}'.format(
            df_resultv.at[4, 'Valor'])),
        html.H4(children='Aceleração média (m/s²) ≈ {:.3f}'.format(
            df_resultv.at[5, 'Valor'])),
        html.H4(children='Aceleração máxima (m/s²) ≈ {:.3f}'.format(
            df_resultv.at[7, 'Valor'])),
        html.H4(children='Tempo aproximado de Voo (s) ≈ {:.1f}'.format(
            df_resultv.at[9, 'Valor'])),
        html.H3(children='Classe: {}'.format(
            df_resultv.at[10, 'Valor'])),
    ])
    ])

    return fig, result

# Este callback lida com o salvamento da análise e exibe um alerta se nenhum nome for fornecido


@callback(
    [Output(component_id='notpass', component_property='children'),
        Output(component_id='pass', component_property='value')],
    [Input(component_id='name', component_property='value'),
        Input(component_id='save', component_property='n_clicks')],
    prevent_initial_call=True
)
def update_name(name, n_clicks):
    if 'save' == ctx.triggered_id:
        # Verifica se um nome foi fornecido
        if name is not None:
            df_resultv.at[11, 'Valor'] = name
            return None, 1
        else:
            alerta = html.H5('Informe um nome para o Voo!!')
            return alerta, None
    else:
        return None, None

# Este callback aciona o processo de salvamento do arquivo quando o botão "Salvar análise" é clicado e um nome é fornecido


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
            # Refaz o processo de análise e gráfico para poder executar a função de salvar
            # Cria um novo dataframe com os dados do intervalo selecionado
            ndf2v = df_dadosv[input_data:input_data2]
            ndf2v['Tempo de Voo'] = ndf2v['Tempo Bruto'] - \
                ndf2v.at[input_data, 'Tempo Bruto']

            # Calcula o Tempo de Voo e a integral numérica
            ndfv = ndf2v.reset_index(drop=True)
            calc_duracao(ndfv['Tempo de Voo'], ndfv['Altura'])

            # Interpolação spline (ainda não implementada corretamente, não atualiza a interpolação com o intervalo selecionado)
            sn = spline(ndfv['Tempo de Voo'], ndfv['Altura'])
            t = []
            pt = []
            for key, value in sn.items():
                def p(x):
                    return eval(value['eq'])
                tx = np.linspace(*value['dominio'], 100)
                t.extend(tx)
                ptx = [p(x) for x in tx]
                pt.extend(ptx)

            def coef(x, y):
                n = len(x)
                sum_x = sum(x)
                sum_x2 = sum([i**2 for i in x])
                sum_y = sum(y)
                sum_xy = sum([x.iloc[i]*y.iloc[i] for i in range(n)])
                A = [[n, sum_x], [sum_x, sum_x2]]
                B = [sum_y, sum_xy]

                return np.linalg.solve(A, B)

            def velocidade(x, a, b):
                return (a*x)+b

            acel = []
            vel = []
            for i in range(len(df_resultv)-1):
                atemp, btemp = coef(
                    ndfv.loc[i:i+2, 'Tempo de Voo'], ndfv.loc[i:i+2, 'Altura'])
                acel.append(atemp)
                vel.append(velocidade(
                    ndfv.at[i, 'Tempo de Voo'], atemp, btemp))

            df_resultv.at[2, 'Valor'] = np.mean(vel)
            df_resultv.at[4, 'Valor'] = max(vel)
            df_resultv.at[3, 'Valor'] = t[vel.index(max(vel))]
            df_resultv.at[5, 'Valor'] = np.mean(acel)
            df_resultv.at[7, 'Valor'] = max(acel)
            df_resultv.at[6, 'Valor'] = t[acel.index(max(acel))]
            df_resultv.at[1, 'Valor'] = max(pt)
            df_resultv.at[0, 'Valor'] = t[pt.index(max(pt))]
            df_resultv.at[10, 'Valor'] = classe(df_resultv.at[1, 'Valor'])

            # Criando o gráfico com os dados de Tempo de Voo e Altura
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=pt, mode='lines',
                          name='Interpolação', line=dict(color='black', width=2)))
            fig.add_trace(go.Scatter(x=ndfv['Tempo de Voo'], y=ndfv['Altura'], mode='markers', name='Altura',
                                     marker=dict(size=16, cmin=0, color=ndfv['Altura'], colorscale='turbo', colorbar=dict(title='Altura (m)')), line=dict(color='black', width=2)))

            fig['layout'].update(height=600, width=800,
                                 xaxis_title='Tempo de Voo (s)', yaxis_title='Altura (m)', xaxis=dict(tickformat='.2f', dtick=0.5), legend=dict(
                                     orientation="h",
                                     yanchor="bottom",
                                     y=1.02,
                                     xanchor="right",
                                     x=1))

            save(nome, ndfv, fig)
            return None
        else:
            return None
    else:
        return None
