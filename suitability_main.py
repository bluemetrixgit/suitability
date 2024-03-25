import pandas as pd
import numpy as np
import streamlit as st
from back_suitability import Calculando_Suitability
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color
import datetime
import smtplib
import email.message
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

dia_e_hora = datetime.datetime.now().strftime("%d %m %Y")
class Interface_suitability():
    def __init__(self):
        super().__init__()
        print('Hello World')

    def questionamentos(self):

        primeira_pergunta = st.radio('Qual é o patrimônio financeiro já investido?',[
                'Até 200 mil',
                'De 200 mil a 1 milhão',
                'De 1 milhão a 10 milhões',
                'Acima de 10 milhões'],
                key='primeira')
        st.text("")
        segunda_pergunta = st.radio('Por quanto tempo você planeja manter seus investimentos?',
                                    ['Por até 1 ano',
                                    'Entre 1 e 5 anos',
                                    'Por mais de 5 anos'],key='Segunda')
        st.text("")
        terceira_pergunta = st.radio('Qual é o seu objetivo com os investimentos?',
                                    ['Preservação de patrimônio',
                                    'Aumento de capital',
                                    'Geração de renda'],
                                    key='Terceira')
        st.text("")
        quarta_pergunta = st.radio('Em uma relação de risco-retorno, qual carteira você prefere?',
                                ['Carteira sem oscilações negativas, com rendimentos previsíveis',
                                    'Carteira com oscilações moderadas, possibilidade de retornos negativos, com a capacidade de alcançar rendimentos elevados',
                                    'Carteira com alta volatilidade, com retornos negativos frequentes, mas com possibilidade de ganhos expressivos',
                                    ],key='Quarta')
        st.text("")
        quinta_pergunta = st.radio('Há quanto tempo você possui investimentos no mercado financeiro?',
                                ['Este seria o meu primeiro investimento',
                                    'Menos de 1 ano',
                                    'De 1 a 5 anos',
                                    'Acima de 5 anos'],key='Quinta')
        st.text("")
        sexta_pergunta = st.radio('Quais tipos de ativos você já investiu?',
                                ['Previdência privada ,Títulos privados (CDB, LCA, LCI)Títulos públicos (Tesouro Direto)',
                                'Fundos (imobiliários, multimercado, de ações, direitos creditórios, de renda fixa)',
                                'Derivativos, Investimentos no exterior',
                                'Não tenho familiaridade com investimentos'],key='Sexta')
        st.text("")
        setima_pergunta = st.radio('Qual característica é mais importante para você ao investir?',
                                ['Liquidez',
                                    'Segurança',
                                    'Rentabilidade'])
        st.text("")
        oitava_pergunta = st.radio("Qual é a proporção do valor a ser investido em relação ao seu patrimônio total?",
                                ['Menos de 25%',
                                    'Entre 25% e 50%',
                                    'Acima de 50%'])
        st.text("")
        nona_pergunta = st.radio('Qual das opções abaixo melhor descreve sua relação com o mercado financeiro e sua formação acadêmica?',
                                ['Não conheço ou conheço pouco as regras do mercado financeiro e preciso de toda a orientação possível',
                                'Conheço as regras do mercado financeiro e/ou tenho formação na área de finanças, mas ainda necessito de orientação profissional devido à falta de experiência prática',
                                'Tenho experiência no mercado financeiro, domino os conceitos e tomo minhas próprias decisões de investimento'],key='Nona')
        st.text("")
        decima_pergunta = st.radio('Com relação aos riscos de investimentos, como você reagiria ao verificar um retorno negativo devido à volatilidade do mercado?',
                                ['Resgataria imediatamente',
                                'Estabeleceria um limite máximo de perda antes de resgatar',
                                'Investiria mais recursos adicionais'],key='Decima')
        sexta_pergunta = sexta_pergunta if sexta_pergunta else []
        return (primeira_pergunta,segunda_pergunta,terceira_pergunta,quarta_pergunta,quinta_pergunta,sexta_pergunta,setima_pergunta,oitava_pergunta,nona_pergunta,decima_pergunta)
class GeradorPDF:
    def __init__(self, filename):
        self.filename = filename
    
    def gerar_pdf(self, suitability_result,nome_cliente,cpf):

        c = canvas.Canvas(self.filename, pagesize=letter)
        img1 = ImageReader("imagem bmrtx.jpg")
        c.drawImage(img1, 150, 600, width=250, height=200,mask='auto')

        # Configurações de fonte
        c.setFont('Helvetica-Bold', 20)  # Fonte em negrito, tamanho 16
        c.setFillColor('black')
        c.drawString(190, 600, f'{nome_cliente}')

        c.setFont('Times-Roman', 15)  # Fonte em negrito, tamanho 16
        c.setFillColor('black')
        c.drawString(190, 550, f'CPF   {cpf}')


        c.setFont('Times-Roman', 15)  # Fonte em negrito, tamanho 16
        c.setFillColor('black')
        c.drawString(230, 450, "Resultado do Suitability:")

        c.setFont('Helvetica-Bold', 30)  # Fonte em negrito, tamanho 16
        c.setFillColor('black')
        c.drawString(230, 400, f"{suitability_result}")

        # Adiciona data
        c.setFont('Helvetica-Bold', 10)  # Altera a fonte para não negrito
        c.drawString(100, 350, f"Data: {dia_e_hora}")
        c.setLineWidth(0.5)  # Define a espessura da linha
        c.line(100, 340, 180, 340)  


        img = ImageReader("imagem bmrtx.jpg")
        c.drawImage(img, 150, 10, width=250, height=200,mask='auto')


        c.save()
        print(f"PDF gerado com sucesso: {self.filename}")

def enviar_email(nome_cliente,nome_do_arquivo_pdf):
    corpo_do_email = """
    suitability
    """
    msg = MIMEMultipart()
    msg['Subject'] = f'Suitability {nome_cliente}'
    msg['From'] = 'lauro.bluemetrix@gmail.com'
    msg['To'] = 'lauro.bluemetrix@gmail.com'
    password = 'dlthvrayjsecacbt'
    msg.add_header('Content-Type', 'text/html')

    msg.attach(MIMEText(corpo_do_email, 'plain'))

    with open(nome_do_arquivo_pdf, 'rb') as f:
        arquivo_pdf = f.read()
        arquivo_anexado = MIMEApplication(arquivo_pdf, _subtype="pdf")
        arquivo_anexado.add_header('content-disposition', 'attachment', filename=nome_arquivo_pdf)
        msg.attach(arquivo_anexado)

    s=smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string().encode('utf-8'))
    print('email enviado')





if __name__=='__main__':

    
    st.header('Questionário Suitability - Bluemetrix')
    st.write('Preencha os campos abaixo para realizar o cadastro do Suitability')
    st.text("")
    st.text("")
    st.text("")

    nome_cliente = st.text_input('Nome completo :','')
    cpf = st.text_input('CPF')
    

    interface = Interface_suitability()
    respostas = tuple(interface.questionamentos())
    calculando = Calculando_Suitability()
    st.text("")
    st.text("")
    st.text("")
    if st.button('Enviar',type='primary'):
        suitability_final = calculando.definindo_suitability(*respostas)
        st.warning(suitability_final)
        # Use o nome do arquivo que você deseja para o PDF
        
        nome_arquivo_pdf = f"Suitability  {nome_cliente}  {dia_e_hora}  {cpf}_.pdf"

    # Calcule o resultado do suitability
        resultado_suitability = suitability_final  # Substitua isso pelo resultado real do seu cálculo
        gerador_pdf = GeradorPDF(nome_arquivo_pdf)
        gerador_pdf.gerar_pdf(resultado_suitability,nome_cliente,cpf)
        enviar_email(nome_cliente,nome_arquivo_pdf)
        st.success('Suitability enviado, Obrigado')    

