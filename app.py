import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página (DEVE SER A PRIMEIRA LINHA)
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

# --- CSS ESTRUTURAL (Sem erros de injeção) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Forçar preenchimento total da tela no celular */
    .block-container { 
        padding-top: 1rem !important; 
        padding-left: 0rem !important; 
        padding-right: 0rem !important; 
        max-width: 600px !important; 
        margin: auto;
    }

    /* Estilo do Título */
    .page-title {
        text-align: center;
        color: #1a237e;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    /* Linha azul superior */
    .top-line {
        height: 6px;
        background-color: #1a237e;
        width: 100%;
    }

    /* BOTÕES EM BLOCO (Simetria Total) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        margin-top: -1px !important;
    }
    [data-testid="column"] {
        flex: 1 !important;
        padding: 0px !important;
    }

    /* Estilo dos Botões */
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        height: 50px !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e5e7eb !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
    }

    /* Ajuste da Imagem */
    .stImage img {
        width: 100% !important;
        border-radius: 0px;
        margin-bottom: 0px !important;
        border-left: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
    }

    /* Cards de Seleção */
    .profile-item {
        background: white;
        padding: 15px;
        border: 1px solid #ddd;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Gestão de Estado ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'img_idx' not in st.session_state: st.session_state.img_idx = 0
if 'view' not in st.session_state: st.session_state.view = None

def navigate(p):
    st.session_state.page = p
    st.session_state.img_idx = 0
    st.session_state.view = None

# --- Páginas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:200px;"></div>', unsafe_allow_html=True)
    st.button("ENTRAR NO SISTEMA", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="page-title">SELECIONE O PERFIL</div>', unsafe_allow_html=True)
    
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    for key, name, initial in profiles:
        st.markdown(f'<div class="profile-item"><div style="background:#1a237e; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center;">{initial}</div><b>ALUNO: {name}</b></div>', unsafe_allow_html=True)
        if st.button(f"ACESSAR {name}", key=f"btn_{key}"):
            navigate(key)
            st.rerun()

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    users = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    current = st.session_state.page
    
    st.markdown(f'<div class="page-title">{names[current]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)
    
    imgs = [load_image(f, rotate_degrees=90) for f in users[current]]
    if imgs[st.session_state.img_idx]:
        st.image(imgs[st.session_state.img_idx], use_container_width=True)

    # Navegação
    n1, n2 = st.columns(2)
    with n1:
        if st.button("ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(imgs); st.rerun()
    with n2:
        if st.button("PRÓXIMO"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(imgs); st.rerun()

    # Ações
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if st.button("FREQ."): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view = 'n'; st.rerun()
    with f3:
        if st.button("QR"): st.session_state.view = 'q'; st.rerun()
    with f4:
        if st.button("SAIR"): navigate('login'); st.rerun()
            
