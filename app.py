import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página
st.set_page_config(
    page_title="Sistema de Identificação",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Funções de Suporte ---
@st.cache_data
def load_image(image_path, rotate_degrees=0):
    try:
        image = Image.open(image_path)
        if rotate_degrees != 0:
            return image.rotate(rotate_degrees, expand=True)
        return image
    except Exception:
        return None

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- CSS: BLOCO INTEGRADO E CARD DE VALIDADE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .block-container { 
        padding-top: 0.5rem !important; 
        padding-left: 0rem !important; 
        padding-right: 0rem !important; 
        max-width: 100% !important; 
    }

    /* CARD DE VALIDADE (Design inspirado no seu print) */
    .validade-container {
        background-color: #1a237e;
        color: white;
        padding: 15px;
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-bottom: 1px solid #ffffff33;
        width: 100vw;
    }
    .val-label { font-size: 0.7rem; opacity: 0.8; margin-bottom: 2px; }
    .val-date { font-size: 1.1rem; font-weight: 700; margin-bottom: 10px; }
    
    .val-box {
        background: white;
        color: #1a237e;
        padding: 5px 15px;
        border-radius: 10px;
        display: inline-block;
        width: fit-content;
        margin-top: 5px;
    }

    /* Título e Linha */
    .section-header { text-align: center; color: #1a237e; font-weight: 700; font-size: 1rem; margin: 10px 0; }
    .blue-line { height: 6px; background-color: #1a237e; width: 100%; }

    /* Layout de Botões */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 2px !important;
        margin-top: -1px !important;
        width: 100vw !important;
    }
    [data-testid="column"] { flex: 1 !important; padding: 0px !important; }

    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        height: 50px !important;
        font-weight: 700 !important;
        font-size: 0.7rem !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e5e7eb !important;
    }

    .stImage img { width: 100vw !important; border-radius: 0px; display: block; }
    
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Navegação e Estado ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'img_idx' not in st.session_state: st.session_state.img_idx = 0
if 'view' not in st.session_state: st.session_state.view = None

def navigate(p):
    st.session_state.page = p
    st.session_state.img_idx = 0
    st.session_state.view = None

# --- Páginas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:200px;"></div>', unsafe_allow_html=True)
    st.button("ACESSAR SISTEMA", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="section-header">SELECIONE O ALUNO</div>', unsafe_allow_html=True)
    for key, name, initial in [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]:
        if st.button(f"ALUNO: {name}", key=f"btn_{key}"): navigate(key); st.rerun()

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    # Certifique-se de que os nomes dos arquivos estão corretos
    files = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current = st.session_state.page
    
    st.markdown(f'<div class="section-header">IDENTIFICAÇÃO: {names[current]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)
    
    # Foto
    imgs = [load_image(f, rotate_degrees=90) for f in files[current]]
    if imgs[st.session_state.img_idx]:
        st.image(imgs[st.session_state.img_idx], use_container_width=True)

    # --- NOVO CARD DE VALIDADE (Abaixo da foto) ---
    st.markdown(f"""
        <div class="validade-container">
            <div class="val-label">Data da Matrícula:</div>
            <div class="val-date">01/03/2019</div>
            <div class="val-box">
                <span style="font-size:0.7rem; font-weight:700;">Validade:</span><br>
                <span style="font-size:1.1rem; font-weight:800;">30/06/2026</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Navegação (Botão Próximo corrigido com rerun)
    n1, n2 = st.columns(2)
    with n1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(imgs)
            st.rerun()
    with n2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(imgs)
            st.rerun()

    # Barra de Funções
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if st.button("FREQ."): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view = 'n'; st.rerun()
    with f3:
        if st.button("QR"): st.session_state.view = 'q'; st.rerun()
    with f4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    # Área de Dados
    if st.session_state.view == 'q':
        qr = load_image("qrcode.png")
        if qr: 
            st.markdown("<br>", unsafe_allow_html=True)
            _, qc, _ = st.columns([1, 2, 1])
            with qc: st.image(qr, use_container_width=True)
