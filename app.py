import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página (Ajuste para Wide e padding zero)
st.set_page_config(
    page_title="Portal de Documentos",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- TRUQUE TÉCNICO PARA FORÇAR TELA CHEIA E ESCALA NO CELULAR ---
# Isso injeta uma tag no HTML que avisa ao navegador do celular para não "encolher" a página.
st.markdown('''
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    </head>
''', unsafe_allow_html=True)

# --- CSS REVISADO PARA OCUPAR A TELA TODA SEM MUDAR DISPOSIÇÃO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Remove as margens brancas gigantes que o Streamlit coloca nas laterais */
    .block-container { 
        padding-top: 1rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
        max-width: 100% !important; /* Agora ocupa 100% da largura do celular */
        margin: auto;
    }

    /* Título e Linha Decorativa */
    .header-text {
        text-align: center;
        color: #1a237e;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .top-accent {
        height: 6px;
        background-color: #1a237e;
        width: 100%;
        border-radius: 4px 4px 0 0;
    }

    /* MANTÉM A DISPOSIÇÃO EM BLOCO QUE VOCÊ GOSTOU */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        margin-top: -1px !important;
        width: 100% !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    /* Botões: Tamanho otimizado para preencher o bloco */
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        height: 50px !important; /* Um pouco mais alto para facilitar o toque */
        font-weight: 700 !important;
        font-size: 0.8rem !important; /* Aumentado para não precisar de zoom */
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #d1d5db !important;
        white-space: nowrap !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
    }

    /* Imagem: 100% da largura disponível */
    .stImage img {
        width: 100% !important;
        border-radius: 0px;
        margin-bottom: 0px !important;
        display: block;
        border: 1px solid #d1d5db;
        border-top: none;
    }

    /* Esconder Lixo do Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- O restante do seu código de navegação e lógica (Jean, Thiago, Hemilly) continua igual abaixo ---
# ... (Mantenha o código das páginas e botões conforme a última versão)
