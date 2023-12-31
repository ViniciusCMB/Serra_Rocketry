import numpy as npy
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import easygui
from fpdf import FPDF
from PIL import Image


def calc_h(f, i, n):
    return (f-i)/n


def nd_simp(y, h):

    soma_ci_1 = 0.0
    soma_ci_2 = 0.0
    soma_ci_3 = 0.0

    for i in range(len(y)):
        if i == 0 or i == len(y)-1:
            soma_ci_1 += y[i]
        elif i % 3 == 0 and i != 0 and i != len(y)-1:
            soma_ci_2 += y[i]
        else:
            soma_ci_3 += y[i]

    return (3*h/8)*(soma_ci_1+(2*soma_ci_2)+(3*soma_ci_3))


def spline(xi, yi):
    n = len(xi)
    a = {k: v for k, v in enumerate(yi)}
    h = {k: xi[k+1]-xi[k] for k in range(n-1)}

    A = [[1]+[0]*(n-1)]
    for i in range(1, n-1):
        linha = npy.zeros(n)
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

    c = dict(zip(range(n), npy.linalg.solve(A, B)))

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


def mmq(xi, yi):
    n = len(xi)
    sum_x = sum(xi)
    sum_x2 = sum([i**2 for i in xi])
    sum_y = sum(yi)
    sum_xy = sum([xi[i]*yi[i] for i in range(n)])
    A = [[n, sum_x], [sum_x, sum_x2]]
    B = [sum_y, sum_xy]

    return npy.linalg.solve(A, B)


def calc_mmq(x, c1, c0):
    return (c1*x)+c0


def calc_integral():

    list_result['integral'] = nd_simp(
        yi, calc_h(xi[len(xi)-1], xi[0], len(xi)-1))

    list_result['medioE'] = (1/(xi[len(xi)-1]-xi[0]))*list_result['integral']

    list_result['classificacao'] = classe(
        list_result['integral'], list_result['medioE'], list_result['duracao'])

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


def save(file):
    plt.savefig(file+'.png')

    class PDF(FPDF):
        def header(self):
            # Logos
            self.image(
                '/home/viniciusmonnerat/Documentos/Serra_Rocketry/Analise de dados estaticos/LOGO - ALTERNATIVA.png', 210-47, -5, 50)
            self.image(
                '/home/viniciusmonnerat/Documentos/Serra_Rocketry/Analise de dados estaticos/logomarca-uerj-300x300.png', 2, 2, 35)

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
    pdf.cell(0, 10, list_result['nome'], 0, 0, 'C', 0)
    pdf.set_xy(15, 60)
    pdf.set_font('Times', '', 18)
    pdf.multi_cell(0, 10, 'Data do teste: ' +
                   str(list_result['data'])+'\nHora do teste: '+str(list_result['inicio']))

    pdf.set_xy(15, 75)
    pdf.set_font('Times', '', 14)
    pdf.multi_cell(0, 8, '\nImpulso Total (N*s) = {:.3f}'.format(list_result['integral']) +
                   '\nEmpuxo Médio (N) = {:.3f}'.format(list_result['medioE']) +
                   '\nEmpuxo Máximo (N) = {:.3f}'.format(list_result['maxyE']) +
                   '\nTempo aproximado de queima (s)= {:.1f}'.format(list_result['duracao']), 0, 1)

    pdf.set_xy(105, 83)
    pdf.set_font('Times', '', 50)
    pdf.cell(0, 10, '{}'.format(list_result['classificacao']))

    pdf.set_fill_color(r=43, g=18, b=76)
    pdf.set_y(120)
    pdf.cell(0, 1, ' ', 0, 1, 'C', 1)
    pdf.image(file+'.png', (210/2)-90, 130, 180, 140)
    pdf.output(file+'.pdf', 'F')

    return None


def select():

    return easygui.fileopenbox()


def save_path():

    return easygui.filesavebox()


def QU(y2, y1, x2, x1):
    m = (y2 - y1) / (x2 - x1)
    if m > 10 or m < -10:
        if m < -10:
            return None, None, 0
        else:
            return None, None, 1
    else:
        return y1, x1, 1


def graph():

    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Painel de Análise")
    root.maxsize(1400,  900)
    dialog = ctk.CTkInputDialog(text="Qual o nome do motor?", title="Nome")
    list_result['nome'] = dialog.get_input()

    sn = spline(xi, yi)

    plt.rcParams["figure.figsize"] = (8, 6)
    fig, ax1 = plt.subplots()

    ax1.set_title(list_result['nome']+'\n', fontsize=15)
    ax1.grid()
    max_x = 0.0
    max_y = 0.0
    for key, value in sn.items():
        def p(x):
            return eval(value['eq'])
        t = npy.linspace(*value['dominio'], 100)
        for i in range(len(t)-1):
            temp = p(t[i])
            if max_y < temp:
                max_x = t[i]
                list_result['maxxE'] = max_x
                max_y = p(t[i])
                list_result['maxyE'] = max_y
        linha, = ax1.plot(t, p(t), c='red')

    linha.set_label('Interpolação')
    ax1.scatter(max_x, max_y, c='purple', label='Máximo')
    x2 = []
    y2 = []
    for i in range(len(yi)-1):
        ytemp, xtemp, cond = QU(yi[i+1], yi[i], xi[i+1], xi[i])

        if ytemp == None and cond == 0:
            x2.append(xi[i])
            y2.append(yi[i])
            break
        elif ytemp == None:
            continue
        else:
            x2.append(xtemp)
            y2.append(ytemp)

    c0, c1 = mmq(x2, y2)
    mmqy = [calc_mmq(ti, c1, c0) for ti in x2]
    ax1.plot(x2, mmqy, c='blue', label=f'MMQ (A={c1:.4f}, B={c0:.4f})')

    ax1.scatter(xi, yi, c='black', label='Pontos')
    ax1.set_ylabel('Empuxo (N)', fontsize=12)
    ax1.set_xlabel('Tempo (s)', fontsize=12)
    ax1.yaxis.set_minor_formatter('{x:.2f}')
    ax1.yaxis.set_major_formatter('{x:.2f}')
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.tick_params(which='both', width=2)
    ax1.tick_params(which='major', length=7)
    ax1.tick_params(which='minor', length=4, color='gray')
    ax1.legend()

    Frame = ctk.CTkFrame(master=root,  width=1200,  height=900,
                         fg_color='#473E66', corner_radius=0)
    Frame.pack(fill='both',  padx=5,  pady=5,  expand=True)

    plotframe = ctk.CTkFrame(master=Frame, width=800,
                             height=600, fg_color='#F5D7DB', corner_radius=5)
    plotframe.pack(padx=5, pady=15, side='left')
    canvas = FigureCanvasTkAgg(fig, master=plotframe)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0, rely=0)
    infos = ctk.CTkLabel(master=Frame, text='Data do teste: '+list_result['data'] +
                         '\nHorário do teste: '+list_result['inicio'] +
                         '\nImpulso Total (N*s) ≈ {:.3f}'.format(list_result['integral']) +
                         '\nEmpuxo médio (N) ≈ {:.3f}'.format(list_result['medioE']) +
                         '\nEmpuxo máximo (N) ≈ {:.3f}'.format(list_result['maxyE']) +
                         '\nQuantidade de pontos: '+list_result['pontos'] +
                         '\nTempo de queima (s) ≈ {:.1f}'.format(list_result['duracao']) +
                         '\nClasse: {}'.format(list_result['classificacao']),
                         fg_color='#522B5B',
                         text_color='white',
                         corner_radius=5,
                         height=200,
                         width=400,
                         font=('Roboto', 18, 'bold'))
    infos.pack(padx=5, pady=14, side='top')

    save_btn = ctk.CTkButton(master=Frame, corner_radius=10, height=50, width=150, font=('Roboto', 15), fg_color='#522B5B',
                             hover_color='#2B124C', border_color='black', border_width=2, text='Gerar Relatório', command=lambda: [save(save_path())])
    save_btn.pack(padx=5, pady=10, side='top')

    your_image = ctk.CTkImage(light_image=Image.open(
        '/home/viniciusmonnerat/Documentos/Serra_Rocketry/Analise de dados estaticos/LOGO - ALTERNATIVA.png'), size=(250, 250))
    label = ctk.CTkLabel(master=Frame, image=your_image, text='')
    label.pack(padx=5, pady=5, side='bottom')

    root.update()

    return root.mainloop()


yi = []
xii = []
h = []
data = []
arq = open(select(), 'r').read()
lines = arq.split('\n')
for line in lines:
    if len(line) > 1:
        d, z, y, x = line.split(';')
        data.append(d)
        h.append(z)
        yi.append((float(y)+0.013) * 9.81)
        xii.append(float(x) / 1000)

xi = [xii[i]-xii[0] for i in range(len(xii))]

list_result = {'integral': 0.0, 'maxxE': 0.0, 'maxyE': 0.0, 'medioE': 0.0,
               'pontos': str(len(yi)), 'duracao': xi[len(xi)-1]-xi[0], 'inicio': h[0], 'data': data[0], 'classificacao': '', 'nome': ''}

calc_integral()
graph()
