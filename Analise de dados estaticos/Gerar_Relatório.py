from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # Logo
        self.image(
            '/home/vinicius/Área de Trabalho/Serra_Rocketry/Analise de dados estaticos/LOGO - ALTERNATIVA.png', 210-47, -5, 50)
        self.image(
            '/home/vinicius/Área de Trabalho/Serra_Rocketry/Analise de dados estaticos/logomarca-uerj-300x300.png', 2, 2, 35)
        # Arial bold 15
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
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}' + ' - Equipe Serra Rocketry', 0, 0, 'C')


list_result = {'integral': 0.0, 'maxxE': 0.0, 'maxyE': 0.0, 'medioE': 0.0,
               'pontos': 0.0, 'duracao': 0.0, 'inicio': 0.0, 'data': 0.0}
# Instantiation of inherited class
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_xy(15, 50)
pdf.set_font('Times', '', 18)
pdf.multi_cell(0, 10, 'Data do teste: ' +
               str(list_result['data'])+'\nHora do teste: '+str(list_result['inicio']))

pdf.set_xy(15, 65)
pdf.set_font('Times', '', 14)
pdf.multi_cell(0, 8, '\nImpulso Total (N*s) = '+str(list_result['integral']) +
                     '\nEmpuxo Médio (N) = '+str(list_result['medioE']) +
                     '\nEmpuxo Máximo (N) = '+str(list_result['maxyE']) +
                     '\nTempo aproximado de queima = '+str(list_result['duracao']), 0, 1)

pdf.set_fill_color(r=43, g=18, b=76)
pdf.set_y(110)
pdf.cell(0, 1, ' ', 0, 1, 'C', 1)
pdf.image("Motor_Comercial.png", (210/2)-90, 120, 180, 140)


pdf.output('Análise.pdf', 'F')
