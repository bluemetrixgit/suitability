from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from suitability_main import Interface_suitability
from reportlab.lib import utils



perguntas = {'Qual é o patrimônio financeiro já investido?':[
                'Até 200 mil',
                'De 200 mil a 1 milhão',
                'De 1 milhão a 10 milhões',
                'Acima de 10 milhões'],            
        
        'Por quanto tempo você planeja manter seus investimentos?':
                                    ['Por até 1 ano',
                                    'Entre 1 e 5 anos',
                                    'Por mais de 5 anos'],
        

        'Qual é o seu objetivo com os investimentos?':
                                    ['Preservação de patrimônio',
                                    'Aumento de capital',
                                    'Geração de renda'],

        'Em uma relação de risco-retorno, qual carteira você prefere?':
                                ['Carteira sem oscilações negativas, com rendimentos previsíveis',
                                    'Carteira com oscilações moderadas, possibilidade de retornos negativos, com a capacidade de alcançar rendimentos elevados',
                                    'Carteira com alta volatilidade, com retornos negativos frequentes, mas com possibilidade de ganhos expressivos',
                                    ],
        

        'Há quanto tempo você possui investimentos no mercado financeiro?':
                                ['Este seria o meu primeiro investimento',
                                    'Menos de 1 ano',
                                    'De 1 a 5 anos',
                                    'Acima de 5 anos'],


        "Qual é a sua experiência e conhecimento sobre os produtos e serviços oferecidos no mercado financeiro?":
                                ['Nenhuma: Não possuo experiência prévia e nunca realizei investimentos no mercado financeiro.',
                                'Limitada: Tenho conhecimento muito básico e comecei a investir recentemente.',
                                'Moderada: Acompanho esporadicamente e possuo um entendimento básico sobre o mercado financeiro.',
                                'Suficiente: Tenho um conhecimento abrangente sobre os produtos e ativos disponíveis, incluindo fundos, derivativos e títulos.'],
   
   
        'Qual característica é mais importante para você ao investir?':
                                ['Liquidez',
                                    'Segurança',
                                    'Rentabilidade'],
        

       "Qual é a proporção do valor a ser investido em relação ao seu patrimônio total?":
                                ['Menos de 25%',
                                    'Entre 25% e 50%',
                                    'Acima de 50%'],

        'Qual das opções abaixo melhor descreve sua relação com o mercado financeiro e sua formação acadêmica?':
                                ['Não conheço ou conheço pouco as regras do mercado financeiro e preciso de toda a orientação possível',
                                'Conheço as regras do mercado financeiro e/ou tenho formação na área de finanças, mas ainda necessito de orientação profissional devido à falta de experiência prática',
                                'Tenho experiência no mercado financeiro, domino os conceitos e tomo minhas próprias decisões de investimento'],


        'Com relação aos riscos de investimentos, como você reagiria ao verificar um retorno negativo devido à volatilidade do mercado?':
                                ['Resgataria imediatamente',
                                'Estabeleceria um limite máximo de perda antes de resgatar',
                                'Investiria mais recursos adicionais'],

        '"Qual é o seu perfil de investidor: Profissional, Qualificado ou Não Qualificado?"':
                                            ['Investidor Profissional: Investidor profissional é uma pessoa jurídica ou física que atua no mercado financeiro'
                                              'diretamente ou por meio de terceiros, e que possui investimentos financeiros em valor superior a R$ 10 milhões e atestou por escrito(Assinou o termo de Investidor Profissional). ',
                                                'Investidor Qualificado: Pessoa física ou jurídica que possui investimentos financeiros em valor superior a R$ 1 milhão e atestou por escrito(Assinou o termo de Investidor Qualificado).',
                                                'Investidor Não Qualificado: Um Não qualificado é aquele que não se enquadra nas definições de investidor profissional ou qualificado. Geralmente, são indivíduos sem certificações específicas para o mercado financeiro.'],
                                                        }


class GeradorPDF:
    def __init__(self):
        print('PDF questionario suitability')

    def gerar_pdf(self):
        c = canvas.Canvas("Quest PDF.pdf", pagesize=letter)

        img1 = ImageReader("LOGO_BLUEMETRIX_VERTICAL jpg.jpg")
        c.drawImage(img1, 150, 750, width=250, height=200, mask='auto')

        c.setFont('Helvetica', 10)
        c.setFillColor('black')

        y_position = 600 # Posição inicial Y das perguntas

        # Iterando sobre todas as perguntas e opções e adicionando-as ao PDF
        for indice, pergunta in enumerate(perguntas, start=1):
            c.setFont('Helvetica-Bold', 10)
            c.stringWidth(f"{indice}. {pergunta}")
            #utils.stringWidth(f"{indice}. {pergunta}", 'Helvetica-Bold', 12)
            c.drawString(10, y_position, f"{indice}. {pergunta}")
            y_position -= 20  # Ajuste a posição Y para as opções

            # Ajustando opções para uma pergunta
            opcoes = perguntas[pergunta]

            # Iterando sobre as opções da pergunta
            for opcao in opcoes:
                y_position -= 15  # Ajuste a posição Y para a próxima opção
                c.setFont('Helvetica', 10)
                c.drawString(20, y_position, f"- {opcao}")

            y_position -= 30  # Espaço entre as perguntas

            # Verificar se há espaço para outra pergunta na página atual
            if y_position < 50:
                c.showPage()  # Adicionar uma nova página
                c.drawImage(img1, 150, 750, width=250, height=200, mask='auto')
                y_position = 750  # Reiniciar a posição Y para a próxima página

        # Salvando o arquivo PDF
        c.save()
        print("PDF gerado com sucesso.")


if __name__ == "__main__":
    quest = Interface_suitability()
    pdf = GeradorPDF()
    pdf.gerar_pdf()

