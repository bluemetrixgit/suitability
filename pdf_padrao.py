# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, re
from textwrap import wrap
from datetime import datetime

# Fonte (opcional)
try:
    pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    FONT_NAME = "DejaVuSans"
except Exception:
    FONT_NAME = "Helvetica"

PAGE_W, PAGE_H = A4
LEFT = 20 * mm
RIGHT = PAGE_W - 20 * mm
TOP = PAGE_H - 20 * mm
BOTTOM = 20 * mm
LINE_H = 6 * mm
NEW_PAGE_TOP = PAGE_H - 60*mm  # ponto seguro abaixo do cabeçalho
CONTENT_LEFT = LEFT
CONTENT_WIDTH = RIGHT - LEFT


LOGO_PATH = "bluemetrix_2024_suitability_cabecalho_100.jpg"


def draw_header(c: canvas.Canvas, titulo: str):
    if os.path.exists(LOGO_PATH):
        c.drawImage(ImageReader(LOGO_PATH), 0, PAGE_H - 45*mm, width=PAGE_W, height=45*mm, mask='auto')


def desenhar_rodape(c: canvas.Canvas, page_num: int):
    c.setFont(FONT_NAME, 11)  # um pouco maior para destacar
    c.setFillColorRGB(0.4, 0.4, 0.4)

    # Texto central
    c.drawCentredString(PAGE_W/2, 15*mm, "Bluemetrix Asset")

    # Número da página no canto direito
    c.setFont(FONT_NAME, 9)
    c.drawRightString(RIGHT, 15*mm, f"página {page_num}")



def draw_wrapped_text(c: canvas.Canvas, text: str, x: float, y: float, max_width: float, font_size: int = 11):
    """Escreve texto com quebra automática por largura; retorna a nova coordenada Y."""
    c.setFont(FONT_NAME, font_size)
    avg_char_w = pdfmetrics.stringWidth("M", FONT_NAME, font_size) * 0.6 + 0.1
    max_chars = max(int(max_width / avg_char_w), 10)
    for line in text.splitlines():
        for chunk in wrap(line, width=max_chars):
            c.drawString(x, y, chunk)
            y -= LINE_H
    return y


def nova_pagina(c: canvas.Canvas, titulo: str, page_num=[1]):
    desenhar_rodape(c, page_num[0])
    c.showPage()
    page_num[0] += 1
    draw_header(c, titulo)
    c.setFillColorRGB(0, 0, 0)
    c.setStrokeColorRGB(0, 0, 0)


def formatar_cpf(cpf: str) -> str:
    d = re.sub(r'\D', '', cpf or '')
    if len(d) == 11:
        return f"{d[0:3]}.{d[3:6]}.{d[6:9]}-{d[9:11]}"
    return cpf

# ---------- UI helpers: painel de destaque ----------
def chip(c, x, y, w, h, title, value, accent=False):
    # fundo suave
    if accent:
        c.setFillColorRGB(0.90, 0.93, 1.00)   # levemente azulado p/ destaque do Perfil
    else:
        c.setFillColorRGB(0.95, 0.95, 0.95)   # cinza claro
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.roundRect(x, y - h, w, h, 3*mm, stroke=1, fill=1)

    # textos
    c.setFillColorRGB(0.20, 0.20, 0.20)
    c.setFont(FONT_NAME, 10)
    pad = 4*mm
    c.drawString(x + pad, y - pad - 2, title)
    c.setFont(FONT_NAME, 13 if not accent else 14)
    c.drawString(x + pad, y - pad - 2 - 5*mm, value)
# ----------------------------------------------------


def gerar_pdf(nome_arquivo: str, nome: str, cpf: str, respostas: dict, perfil: str):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    c.setTitle("Bluemetrix Asset")
    draw_header(c, "Bluemetrix Asset")

    # Capa
    y = PAGE_H - 60*mm
    
    c.setFillColorRGB(0, 0, 0)
    c.setStrokeColorRGB(0, 0, 0)
    c.setFont(FONT_NAME, 12)
    
    
    # -------- Painel de destaque (Nome / CPF / Perfil) --------
    panel_gap = 3*mm
    row_h = 12*mm
    col_w = (CONTENT_WIDTH - panel_gap) / 2
    
    # Linha 1: Nome | CPF
    chip(c, CONTENT_LEFT, y, col_w, row_h, "Nome", nome)
    chip(c, CONTENT_LEFT + col_w + panel_gap, y, col_w, row_h, "CPF", formatar_cpf(cpf))
    y -= (row_h + panel_gap)
    
    # Linha 2: Perfil (largura total) + Data no canto direito
    chip(c, CONTENT_LEFT, y, CONTENT_WIDTH, row_h, "Perfil apurado", perfil, accent=True)
    c.setFillColorRGB(0, 0, 0)
    c.setFont(FONT_NAME, 10)
    c.drawRightString(CONTENT_LEFT + CONTENT_WIDTH - 4*mm, y - 4*mm - 2, datetime.now().strftime("%d/%m/%Y"))
    y -= (row_h + 4*panel_gap)
    # -------- fim do painel --------

    # Perguntas/Respostas (exatamente como vierem do app)
    c.setFont(FONT_NAME, 12)
    for pergunta, resposta in respostas.items():
        if y < BOTTOM + 4*LINE_H:
            nova_pagina(c, "Bluemetrix Asset")
            y = NEW_PAGE_TOP
        y = draw_wrapped_text(c, f"{pergunta}", LEFT, y, RIGHT-LEFT, font_size=12)
        y = draw_wrapped_text(c, f"Resposta: {resposta}", LEFT+6*mm, y, RIGHT-LEFT-6*mm, font_size=11)
        y -= LINE_H/2

    # Assinaturas
    if y < BOTTOM + 6*LINE_H:
        nova_pagina(c, "Questionário de Suitability – Bluemetrix Asset")
        y = NEW_PAGE_TOP

    y -= 2*LINE_H
    c.line(LEFT, y, RIGHT, y); y -= LINE_H
    c.setFont(FONT_NAME, 11)
    c.drawString(LEFT, y, "Declaro estar ciente de que este questionário tem como objetivo identificar meu perfil de investimento.")
    y -= 2*LINE_H


    # Rodapé da última página
    desenhar_rodape(c, 1)
    c.save()
