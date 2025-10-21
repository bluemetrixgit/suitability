import numpy as np
import pandas as pd
import streamlit as st

mapeamento_respostas = {
    'Até 200 mil': 1,
    'De 200 mil a 1 milhão': 2,
    'De 1 milhão a 10 milhões': 3,
    'Acima de 10 milhões': 4,
    'Por até 1 ano': 1,
    'Entre 1 e 5 anos': 2,
    'Por mais de 5 anos': 3,
    'Preservação de patrimônio': 1,
    'Aumento de capital': 2,
    'Geração de renda': 2,
    'Carteira sem oscilações negativas, com rendimentos previsíveis': 1,
    'Carteira com oscilações moderadas, possibilidade de retornos negativos, com a capacidade de alcançar rendimentos elevados': 2,
    'Carteira com alta volatilidade, com retornos negativos frequentes, mas com possibilidade de ganhos expressivos': 3,
    'Este seria o meu primeiro investimento': 1,
    'Menos de 1 ano': 1,
    'De 1 a 5 anos': 2,
    'Acima de 5 anos': 3,
    'Nenhuma: Não possuo experiência prévia e nunca realizei investimentos no mercado financeiro.':1,
    'Limitada: Tenho conhecimento muito básico e comecei a investir recentemente.':1,
    'Moderada: Acompanho esporadicamente e possuo um entendimento básico sobre o mercado financeiro.':2,
    'Suficiente: Tenho um conhecimento abrangente sobre os produtos e ativos disponíveis, incluindo fundos, derivativos e títulos.': 3,
    'Liquidez': 1,
    'Segurança': 1,
    'Rentabilidade': 2,
    'Menos de 25%': 1,
    'Entre 25% e 50%': 2,
    'Acima de 50%': 3,
    'Não conheço ou conheço pouco as regras do mercado financeiro e preciso de toda a orientação possível': 1,
    'Conheço as regras do mercado financeiro e/ou tenho formação na área de finanças, mas ainda necessito de orientação profissional devido à falta de experiência prática': 2,
    'Tenho experiência no mercado financeiro, domino os conceitos e tomo minhas próprias decisões de investimento': 3,
    'Resgataria imediatamente': 1,
    'Estabeleceria um limite máximo de perda antes de resgatar': 2,
    'Investiria mais recursos adicionais': 3,
    'Investidor Profissional: Investidor profissional é uma pessoa jurídica ou física que atua no mercado financeiro, diretamente ou por meio de terceiros, e que possui investimentos financeiros em valor superior a R$ 10 milhões e atestou por escrito(Assinou o termo de Investidor Profissional). ':0,
    'Investidor Qualificado: Pessoa física ou jurídica que possui investimentos financeiros em valor superior a R$ 1 milhão e atestou por escrito(Assinou o termo de Investidor Qualificado).':0,
    'Investidor Não Qualificado: Um Não qualificado é aquele que não se enquadra nas definições de investidor profissional ou qualificado. Geralmente, são indivíduos sem certificações específicas para o mercado financeiro.':0
}


class Calculando_Suitability():

    def __init__(self):
        print('Hello World')

    def definindo_suitability(self,*respostas):
        respostas = tuple(respostas)
        total = sum(mapeamento_respostas[resp] for resp in respostas)
        if total <= 13:
            return 'Conservador'
        elif 14 <= total <= 22:
            return 'Moderado'
        else:
            return 'Arrojado'
