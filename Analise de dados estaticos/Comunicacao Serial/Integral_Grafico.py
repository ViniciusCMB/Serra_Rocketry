import numpy as npy
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import easygui
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


def calc_integral():

    list_result['integral'] = nd_simp(
        yi, calc_h(xi[len(xi)-1], xi[0], len(xi)-1))

    # print('Integral método 2ª Regra de Simpson composta = {:.4f}'.format(list_result['integral'])+'N*s')

    list_result['medioE'] = (1/(xi[len(xi)-1]-xi[0]))*list_result['integral']
    # print('\nEmpuxo médio: {:.4f}'.format(list_result['medioE'])+'N')
    return None


def graph():

    def save(file):
        f = open(file+'_'+list_result['inicio'], "a")
        f.write('Impulso Total (N*s) ≈ {:.4f}'.format(list_result['integral']) +
                '\nEmpuxo médio (N) ≈ {:.4f}'.format(list_result['medioE']) +
                '\nEmpuxo máximo (N) ≈ {:.4f}'.format(list_result['maxyE'])+', em t={:.4f}'.format(list_result['maxxE']) +
                '\nQuantidade de pontos: '+list_result['pontos'] +
                '\nTempo de queima (s) ≈ {:.3f}'.format(list_result['duracao']) +
                '\nHorário do teste: '+list_result['inicio'])
        f.close()
        plt.savefig(file+'_'+list_result['inicio']+'.png')
        return None
    
    def open_matplot():

        return plt.show()
    
    def save_path():

        return easygui.filesavebox()

    sn = spline(xi, yi)

    plt.rcParams["figure.figsize"] = (8, 6)
    fig, ax1 = plt.subplots()

    ax1.set_title('Gráfico Empuxo vs Tempo ' +
                  list_result['inicio'], fontsize=15)
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

    # print('Empuxo máximo: {:.4f}'.format(list_result['maxyE'])+'N, em t={:.4f}'.format(list_result['maxxE']))
    ax1.scatter(max_x, max_y, c='purple', label='Máximo')
    ym = [(list_result['medioE'])]*(len(xi))
    ax1.plot(xi, ym, c='green', label='Empuxo médio')

    # r = input('\nDeseja buscar um valor específico no tempo?\n"S" para sim e "N" para não\nResposta: ')
    # if r == 'S' or r == 's':
    #     a = float(input(f'Informe o instante desejado no intervalo [{min(xi)},{max(xi)}]: '))
    #     for key, value in sn.items():
    #         def p(x):
    #             return eval(value['eq'])
    #         t = npy.linspace(*value['dominio'],100)
    #         for i in range(len(t)-1):
    #             if a > t[i] and a < t[i+1]:
    #                 tx = p(a)
    #                 print(f'O Empuxo estimado é {tx:.4f}N no instante t={a}')
    #                 plt.scatter(a, tx, c='blue', label='Interesse')
    #                 break

    # ax1.plot(xi, yi, c='blue', label=None)
    ax1.scatter(xi, yi, c='black', label='Pontos')

    ax1.set_ylabel('Empuxo (N)', fontsize=12)
    # ax1.set_xticks(xi, h, rotation=45)
    ax1.set_xlabel('Tempo (s)', fontsize=12)
    # ax1.text(max(xi), max(yi), r'Impulso Total (N*s) ≈ {:.4f}'.format(list_result['integral'])+'\nEmpuxo médio (N) ≈ {:.4f}'.format(list_result['medioE'])+'\nEmpuxo máximo (N) ≈ {:.4f}'.format(list_result['maxyE']), horizontalalignment='right', verticalalignment='top', fontsize=10)
    ax1.yaxis.set_minor_formatter('{x:.3f}')
    ax1.yaxis.set_major_formatter('{x:.2f}')
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.tick_params(which='both', width=2)
    ax1.tick_params(which='major', length=7)
    ax1.tick_params(which='minor', length=4, color='gray')
    ax1.legend()

    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Painel de Análise")
    root.maxsize(1400,  900)

    Frame = ctk.CTkFrame(master=root,  width=1200,  height=800,
                         fg_color='#8989b8', corner_radius=0)
    Frame.pack(fill='both',  padx=5,  pady=5,  expand=True)

    plotframe = ctk.CTkFrame(master=Frame, width=800,
                             height=600, fg_color='#656693', corner_radius=5)
    plotframe.pack(padx=5, pady=15, side='left')
    canvas = FigureCanvasTkAgg(fig, master=plotframe)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0, rely=0)

    infos = ctk.CTkLabel(master=Frame, text='Impulso Total (N*s) ≈ {:.4f}'.format(list_result['integral']) +
                         '\nEmpuxo médio (N) ≈ {:.4f}'.format(list_result['medioE']) +
                         '\nEmpuxo máximo (N) ≈ {:.4f}'.format(list_result['maxyE']) +
                         '\nQuantidade de pontos: '+list_result['pontos'] +
                         '\nTempo de queima (s) ≈ {:.3f}'.format(list_result['duracao']) +
                         '\nHorário do teste: '+list_result['inicio'],
                         fg_color='#656693',
                         text_color='white',
                         corner_radius=5,
                         height=200,
                         width=400,
                         font=('Roboto', 20, 'bold'))
    infos.pack(padx=5, pady=10, side='top')

    save_btn = ctk.CTkButton(master=Frame, corner_radius=10, height=50, width=150, font=('Roboto', 15), fg_color='#7777a6',
                             hover_color='#acabdd', border_color='black', border_width=2, text='Salvar análise', command=lambda: [save(save_path())])
    save_btn.pack(padx=5, pady=10, side='top')

    matplot_btn = ctk.CTkButton(master=Frame, corner_radius=10, height=50, width=150, font=('Roboto', 15), fg_color='#7777a6',
                             hover_color='#acabdd', border_color='black', border_width=2, text='Abrir Matplotlib', command=lambda: [open_matplot()])
    matplot_btn.pack(padx=5, pady=10, side='top')

    your_image = ctk.CTkImage(light_image=Image.open('Analise de dados estaticos/Comunicacao Serial/LOGO - ALTERNATIVA.png'), size=(250, 250))
    label = ctk.CTkLabel(master=Frame, image=your_image, text='')
    label.pack(padx=5, pady=5, side='bottom')


    root.update()

    return root.mainloop()


def select():

    return easygui.fileopenbox()

yi = []
xii = []
h = []
arq = open(select(), 'r').read()
lines = arq.split('\n')
for line in lines:
    if len(line) > 1:
        z, x, y = line.split(';')
        h.append(z)
        yi.append(float(x)*9.81)
        xii.append(float(y)/1000)

xi = [xii[i]-xii[0] for i in range(len(xii))]

list_result = {'integral': 0.0, 'maxxE': 0.0, 'maxyE': 0.0, 'medioE': 0.0,
               'pontos': str(len(yi)), 'duracao': xi[len(xi)-1]-xi[0], 'inicio': h[0]}

calc_integral()
graph()
