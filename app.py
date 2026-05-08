import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página
st.set_page_config(
    page_title="Portal de Documentos",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Funções de Backend ---
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

# --- CSS DE ALTA FIDELIDADE: OTIMIZAÇÃO MOBILE NO COMPUTADOR ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Fundo Neutro para destaque do Bloco */
    .main { background-color: #f4f6f9; }

    /* FIXAÇÃO DO CONTAINER CENTRAL (SIMULAÇÃO CELULAR) */
    .block-container { 
        padding-top: 1.5rem !important; 
        max-width: 480px !important; /* Largura ideal para simetria */
        margin: auto;
        background-color: transparent;
    }

    /* Títulos e Elementos de Topo */
    .header-text {
        text-align: center;
        color: #1a237e;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 12px;
        text-transform: uppercase;
    }
    .top-accent {
        height: 6px;
        background-color: #1a237e;
        width: 100%;
        border-radius: 4px 4px 0 0;
    }

    /* GRID DE BOTÕES: TOTALMENTE SIMÉTRICO E COLADO */
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

    /* Botões: Estilo Bloco Profissional */
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important; /* Bordas retas para efeito de bloco */
        height: 48px !important;
        font-weight: 700 !important;
        font-size: 0.7rem !important;
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

    /* Imagem: Encaixe Perfeito no Bloco */
    .stImage img {
        width: 100% !important;
        border-radius: 0px;
        margin-bottom: 0px !important;
        display: block;
        border: 1px solid #d1d5db;
        border-top: none;
    }

    /* CARDS DE SELEÇÃO DE PERFIL */
    .profile-card {
        background: white;
        border-radius: 10px;
        padding: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
        border: 1px solid #e0e4e8;
        margin-bottom: 8px;
    }
    .avatar-icon {
        width: 38px; height: 38px;
        background: #1a237e;
        color: white;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 0.9rem;
    }

    /* Esconder Lixo do Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Gestão de Estado ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'img_idx' not in st.session_state: st.session_state.img_idx = 0
if 'view_mode' not in st.session_state: st.session_state.view_mode = None

def navigate(page):
    st.session_state.page = page
    st.session_state.img_idx = 0
    st.session_state.view_mode = None

# --- Fluxo de Telas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.button("ACESSAR PORTAL", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="header-text">SELECIONE O ALUNO</div>', unsafe_allow_html=True)
    
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    for key, name, initial in profiles:
        st.markdown(f'''
            <div class="profile-card">
                <div class="avatar-icon">{initial}</div>
                <div style="font-weight:600; font-size:0.85rem; color:#333;">{name}</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button(f"ENTRAR COMO {name}", key=f"btn_{key}"):
            navigate(key)
            st.rerun()
    
    st.markdown('<br>', unsafe_allow_html=True)
    st.button("VOLTAR AO INÍCIO", on_click=navigate, args=('home',))

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current_user = st.session_state.page
    
    # Estrutura do Bloco de Prontuário
    st.markdown(f'<div class="header-text">PRONTUÁRIO: {name_map[current_user]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="top-accent"></div>', unsafe_allow_html=True)
    
    # Imagem (Central do Bloco)
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)

    # Navegação Simétrica (ANTERIOR / PRÓXIMO)
    n1, n2 = st.columns(2)
    with n1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with n2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    # Funções Simétricas (FREQ / NOTAS / QR / SAIR)
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if st.button("FREQ."): st.session_state.view_mode = 'freq'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()
    with f3:
        if st.button("QR"): st.session_state.view_mode = 'qr'; st.rerun()
    with f4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    # Área de Dados (Expansível abaixo do bloco)
    if st.session_state.view_mode:
        st.divider()
        if st.session_state.view_mode == 'qr':
            qr = load_image("qrcode.png")
            if qr:
                _, qc, _ = st.columns([1, 1.5, 1])
                with qc: st.image(qr, use_container_width=True)
        else:
            st.info(f"MODO: {st.session_state.view_mode.upper()}")
