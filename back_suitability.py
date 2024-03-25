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
    'Geração de renda': 3,
    'Carteira sem oscilações negativas, com rendimentos previsíveis': 1,
    'Carteira com oscilações moderadas, possibilidade de retornos negativos, com a capacidade de alcançar rendimentos elevados': 2,
    'Carteira com alta volatilidade, com retornos negativos frequentes, mas com possibilidade de ganhos expressivos': 3,
    'Este seria o meu primeiro investimento': 1,
    'Menos de 1 ano': 2,
    'De 1 a 5 anos': 3,
    'Acima de 5 anos': 4,
    'Previdência privada ,Títulos privados (CDB, LCA, LCI)Títulos públicos (Tesouro Direto)':1,
    'Fundos (imobiliários, multimercado, de ações, direitos creditórios, de renda fixa)':2,
    'Derivativos, Investimentos no exterior':3,
    'Não tenho familiaridade com investimentos': 1,
    'Liquidez': 1,
    'Segurança': 2,
    'Rentabilidade': 3,
    'Menos de 25%': 1,
    'Entre 25% e 50%': 2,
    'Acima de 50%': 3,
    'Não conheço ou conheço pouco as regras do mercado financeiro e preciso de toda a orientação possível': 1,
    'Conheço as regras do mercado financeiro e/ou tenho formação na área de finanças, mas ainda necessito de orientação profissional devido à falta de experiência prática': 2,
    'Tenho experiência no mercado financeiro, domino os conceitos e tomo minhas próprias decisões de investimento': 3,
    'Resgataria imediatamente': 1,
    'Estabeleceria um limite máximo de perda antes de resgatar': 2,
    'Investiria mais recursos adicionais': 3
}


class Calculando_Suitability():

    def __init__(self):
        print('Hello World')

    def definindo_suitability(self,*respostas):
        respostas = tuple(respostas)
        print(respostas)
        total = sum(mapeamento_respostas[resp] for resp in respostas)
        if total <= 10:
            return 'Conservador'
        elif 10 < total <= 20:
            return 'Moderado'
        else:
            return 'Arrojado'

