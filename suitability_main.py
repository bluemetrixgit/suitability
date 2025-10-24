# -*- coding: utf-8 -*-
import os
import io
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text   import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from datetime import datetime
import streamlit as st

from back_suitability import Calculando_Suitability  # mantém seu cálculo/pesos originais
from pdf_padrao import gerar_pdf                     # PDF com cabeçalho, quebras e assinaturas
from datetime import datetime

# --------------------------- CONFIG PÁGINA / TEMA ---------------------------
st.set_page_config(page_title="Suitability - Bluemetrix", page_icon="📄", layout="centered")


st.markdown("""
<style>
:root { --bg:#0e1117; --panel:#121826; --text:#e5e7eb; --muted:#bfc3ca; --line:#2a2f3a; }
.stApp { background:var(--bg); color:var(--text); }
section.main > div.block-container { max-width: 1400px; padding: 1.2rem 2rem; }

/* Texto geral */
*, .stMarkdown, .stMarkdown p, .stMarkdown li, .stCaption, .st-emotion-cache { color: var(--text) !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
  background: var(--panel) !important; color: var(--text) !important; border-color: var(--line) !important;
}
.stNumberInput input { background: var(--panel) !important; color: var(--text) !important; }

/* Radios / Checkboxes */
div[role="radiogroup"] label, div[role="checkbox"] + label { color: var(--text) !important; }
svg { fill: var(--text); color: var(--text); }

/* Botões */
.stButton>button { background:#d99c3a; color:#fff; border-radius:8px; font-weight:600; }
.stButton>button:hover { background:#b57f2d; }

/* Tabelas/expander */
.stDataFrame, .stTable, .stExpander { color: var(--text) !important; }
.stExpander div[role="button"] { background: var(--panel); color: var(--text); }

/* Links */
a { color:#f5c86a !important; }

/* Header transparente */
div[data-testid="stHeader"]{ background:transparent; }
</style>
""", unsafe_allow_html=True)


# Cabeçalho visual (sem iframe)
st.image("bluemetrix_2024_suitability_cabecalho_100.jpg", use_column_width=True)
st.markdown("## Questionário – Bluemetrix Asset")
st.write("Preencha os campos abaixo para realizar o cadastro do Suitability")


# --------------------------- E-MAIL (envio automático) ---------------------------
# Configuração de e-mail (envio sempre do mesmo endereço)
EMAIL_USER = "suitability.bluemetrix@gmail.com"
EMAIL_PASSWORD = "Blue@2025" 
EMAIL_FROM_NAME = "Middle Office Bluemetrix"
EMAIL_TO = "backoffice@bluemetrix.com.br"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587



def enviar_email(nome_cliente: str, pdf_bytes: bytes) -> bool:
    data_br = datetime.now().strftime("%d/%m/%Y")
    data_nome = datetime.now().strftime("%d-%m-%Y")
    nome_pdf = f"Suitability_{perfil}_{nome_cliente}_{data_nome}.pdf".replace(" ", "_")

    msg = MIMEMultipart("related")  # permite HTML + imagens
    msg["Subject"] = f"Suitability – {nome_cliente} – {data_br}"
    msg["From"] = formataddr((EMAIL_FROM_NAME, EMAIL_USER))
    msg["To"] = EMAIL_TO

    # Bloco alternativo (texto + html)
    msg_alternativo = MIMEMultipart("alternative")
    msg.attach(msg_alternativo)

    corpo_html = f"""
    <p>Olá,</p>
    <p>Segue em anexo o Questionário de Suitability do(a) {nome_cliente}, realizado em {data_br}.</p>
    <br>
    <img src="cid:assinatura_bluemetrix" style="width:500px; height:auto;">
    """

    msg_alternativo.attach(MIMEText(corpo_html, "html", "utf-8"))

    # Adiciona assinatura como imagem inline
    with open("Assinatura Middle.png", "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<assinatura_bluemetrix>")
        img.add_header("Content-Disposition", "inline", filename="assinatura.png")
        msg.attach(img)

    # Anexo PDF
    anexo = MIMEApplication(pdf_bytes, _subtype="pdf")
    anexo.add_header("Content-Disposition", "attachment", filename=nome_pdf)
    msg.attach(anexo)


    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, [EMAIL_TO], msg.as_string())
        return True
    except Exception as e:
        st.error(f"Falha no envio por e-mail: {e}")
        return False


# --------------------------- UTIL ---------------------------
def validar_cpf(cpf: str) -> bool:
    d = re.sub(r'\D', '', cpf or '')
    return len(d) == 11

def gerar_pdf_em_memoria(nome: str, cpf: str, respostas_dict: dict, perfil: str) -> bytes:
    """Gera PDF (via pdf_padrao.gerar_pdf) usando arquivo temporário e devolve bytes."""
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        gerar_pdf(tmp_path, nome, cpf, respostas_dict, perfil)
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        try: os.remove(tmp_path)
        except Exception: pass

# --------------------------- FORM ---------------------------
nome_cliente = st.text_input("Nome completo *", "")
cpf          = st.text_input("CPF *", placeholder="000.000.000-00")

st.divider()

# === PERGUNTAS ORIGINAIS (mantidas exatamente) ==============================
class Interface_suitability():
    def __init__(self): super().__init__()
    def questionamentos(self):
        primeira_pergunta = st.radio('Qual é o patrimônio financeiro já investido?',
                                     ['Até 200 mil','De 200 mil a 1 milhão','De 1 milhão a 10 milhões','Acima de 10 milhões'],
                                     key='primeira'); st.text("")
        segunda_pergunta  = st.radio('Por quanto tempo você planeja manter seus investimentos?',
                                     ['Por até 1 ano','Entre 1 e 5 anos','Por mais de 5 anos'],
                                     key='Segunda'); st.text("")
        terceira_pergunta = st.radio('Qual é o seu objetivo com os investimentos?',
                                     ['Preservação de patrimônio','Aumento de capital','Geração de renda'],
                                     key='Terceira'); st.text("")
        quarta_pergunta   = st.radio('Em uma relação de risco-retorno, qual carteira você prefere?',
                                     ['Carteira sem oscilações negativas, com rendimentos previsíveis',
                                      'Carteira com oscilações moderadas, possibilidade de retornos negativos, com a capacidade de alcançar rendimentos elevados',
                                      'Carteira com alta volatilidade, com retornos negativos frequentes, mas com possibilidade de ganhos expressivos'],
                                     key='Quarta'); st.text("")
        quinta_pergunta   = st.radio('Há quanto tempo você possui investimentos no mercado financeiro?',
                                     ['Este seria o meu primeiro investimento','Menos de 1 ano','De 1 a 5 anos','Acima de 5 anos'],
                                     key='Quinta'); st.text("")
        sexta_pergunta    = st.radio("Qual é a sua experiência e conhecimento sobre os produtos e serviços oferecidos no mercado financeiro?",
                                     ['Nenhuma: Não possuo experiência prévia e nunca realizei investimentos no mercado financeiro.',
                                      'Limitada: Tenho conhecimento muito básico e comecei a investir recentemente.',
                                      'Moderada: Acompanho esporadicamente e possuo um entendimento básico sobre o mercado financeiro.',
                                      'Suficiente: Tenho um conhecimento abrangente sobre os produtos e ativos disponíveis, incluindo fundos, derivativos e títulos.'],
                                     key='Sexta'); st.text("")
        setima_pergunta   = st.radio('Qual característica é mais importante para você ao investir?',
                                     ['Liquidez','Segurança','Rentabilidade']); st.text("")
        oitava_pergunta   = st.radio("Qual é a proporção do valor a ser investido em relação ao seu patrimônio total?",
                                     ['Menos de 25%','Entre 25% e 50%','Acima de 50%']); st.text("")
        nona_pergunta     = st.radio('Qual das opções abaixo melhor descreve sua relação com o mercado financeiro e sua formação acadêmica?',
                                     ['Não conheço ou conheço pouco as regras do mercado financeiro e preciso de toda a orientação possível',
                                      'Conheço as regras do mercado financeiro e/ou tenho formação na área de finanças, mas ainda necessito de orientação profissional devido à falta de experiência prática',
                                      'Tenho experiência no mercado financeiro, domino os conceitos e tomo minhas próprias decisões de investimento'],
                                     key='Nona'); st.text("")
        decima_pergunta   = st.radio('Com relação aos riscos de investimentos, como você reagiria ao verificar um retorno negativo devido à volatilidade do mercado?',
                                     ['Resgataria imediatamente','Estabeleceria um limite máximo de perda antes de resgatar','Investiria mais recursos adicionais'],
                                     key='Decima'); st.text("")
        decima_primeira_pregunta = st.radio('"Qual é o seu perfil de investidor: Profissional, Qualificado ou Não Qualificado?"',
                                     ['Investidor Profissional: Investidor profissional é uma pessoa jurídica ou física que atua no mercado financeiro, diretamente ou por meio de terceiros, e que possui investimentos financeiros em valor superior a R$ 10 milhões e atestou por escrito(Assinou o termo de Investidor Profissional). ',
                                      'Investidor Qualificado: Pessoa física ou jurídica que possui investimentos financeiros em valor superior a R$ 1 milhão e atestou por escrito(Assinou o termo de Investidor Qualificado).',
                                      'Investidor Não Qualificado: Um Não qualificado é aquele que não se enquadra nas definições de investidor profissional ou qualificado. Geralmente, são indivíduos sem certificações específicas para o mercado financeiro.'])
        st.write('Conforme Instrução CVM N. 554/2014')
        return (primeira_pergunta,segunda_pergunta,terceira_pergunta,quarta_pergunta,quinta_pergunta,
                sexta_pergunta,setima_pergunta,oitava_pergunta,nona_pergunta,decima_pergunta,decima_primeira_pregunta)

interface = Interface_suitability()
respostas_tuple = interface.questionamentos()

# Dicionário de respostas para o PDF
respostas_dict = {
    'Qual é o patrimônio financeiro já investido?': respostas_tuple[0],
    'Por quanto tempo você planeja manter seus investimentos?': respostas_tuple[1],
    'Qual é o seu objetivo com os investimentos?': respostas_tuple[2],
    'Em uma relação de risco-retorno, qual carteira você prefere?': respostas_tuple[3],
    'Há quanto tempo você possui investimentos no mercado financeiro?': respostas_tuple[4],
    'Qual é a sua experiência e conhecimento sobre os produtos e serviços oferecidos no mercado financeiro?': respostas_tuple[5],
    'Qual característica é mais importante para você ao investir?': respostas_tuple[6],
    'Qual é a proporção do valor a ser investido em relação ao seu patrimônio total?': respostas_tuple[7],
    'Qual das opções abaixo melhor descreve sua relação com o mercado financeiro e sua formação acadêmica?': respostas_tuple[8],
    'Com relação aos riscos de investimentos, como você reagiria ao verificar um retorno negativo devido à volatilidade do mercado?': respostas_tuple[9],
    'Qual é o seu perfil de investidor: Profissional, Qualificado ou Não Qualificado?': respostas_tuple[10],
}

# Só pontuam as 10 primeiras
respostas_que_pontuam = respostas_tuple[:-1]

# LGPD
consent = st.checkbox("Autorizo o tratamento dos meus dados para fins de suitability (LGPD). *")

st.divider()
if st.button("Gerar e Enviar"):
    # validações
    if not nome_cliente.strip() or not validar_cpf(cpf) or not consent:
        st.error("⚠️ Informe Nome, CPF válido (11 dígitos) e aceite o termo (LGPD).")
        st.stop()

    # calcula perfil com seus pesos originais
    calc = Calculando_Suitability()
    perfil = calc.definindo_suitability(*respostas_que_pontuam)
    st.info(f"**Perfil apurado:** {perfil}")
    data_br   = datetime.now().strftime("%d/%m/%Y")   # para o assunto do e-mail
    data_nome = datetime.now().strftime("%d-%m-%Y")   # para o nome do arquivo
    nome_pdf  = f"Suitability_{perfil}_{nome_cliente}_{data_nome}.pdf".replace(" ", "_")

    # gera PDF
    pdf_bytes = gerar_pdf_em_memoria(nome_cliente, cpf, respostas_dict, perfil)

    # download para conferência
    #st.download_button(
    #"Baixar PDF",
    #data=pdf_bytes,
    #file_name=nome_pdf,
    #mime="application/pdf",
#)
    # envio automático
    try:
        enviar_email(nome_cliente, pdf_bytes)
        st.success("E-mail enviado com sucesso para o Backoffice.")
    except Exception as e:
        st.error(f"Falha no envio por e-mail: {e}")
