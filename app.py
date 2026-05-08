import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Documentos",
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

def get_student_data(name):
    data = {
        "Notas": pd.DataFrame({
            "Disciplina": ["Cálculo I", "Física Geral", "Programação", "Algoritmos"],
            "Nota": [8.5, 7.2, 9.8, 8.0],
            "Status": ["Aprovado", "Aprovado", "Aprovado", "Aprovado"]
        }),
        "Frequência": pd.DataFrame({
            "Mês": ["Fevereiro", "Março", "Abril", "Maio"],
            "Presenças": ["95%", "100%", "88%", "92%"],
            "Faltas": [1, 0, 3, 2]
        })
    }
    return data

# --- Estilização CSS Corporativa (Foco em Grid e Tipografia) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #fcfcfd;
    }

    /* Títulos e Identidade */
    .section-title {
        color: #111827;
        font-weight: 700;
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 24px;
        letter-spacing: -0.02em;
    }

    /* Forçar colunas lado a lado no Mobile */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 12px !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
    }

    /* Card do Documento */
    .document-wrapper {
        background: #ffffff;
        border-radius: 8px;
        padding: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Botões: Estilo 'Action Tiles' */
    div.stButton > button {
        width: 100% !important;
        border-radius: 6px !important;
        height: 50px !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.05em !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
        border-color: #1a237e !important;
    }

    /* Botão de Sair (Diferenciado) */
    .exit-btn div.stButton > button {
        background-color: #fef2f2 !important;
        color: #991b1b !important;
        border-color: #fecaca !important;
    }
    .exit-btn div.stButton > button:hover {
        background-color: #991b1b !important;
        color: #ffffff !important;
    }

    /* Cards de Perfil */
    .profile-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
    }
    .avatar-initial {
        width: 48px; height: 48px;
        background-color: #f3f4f6;
        color: #111827;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; font-weight: 600; margin: 0 auto 12px auto;
        border: 1px solid #e5e7eb;
    }

    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Gestão de Navegação ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'img_idx' not in st.session_state:
    st.session_state.img_idx = 0
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = None

def navigate(page):
    st.session_state.page = page
    st.session_state.img_idx = 0
    st.session_state.view_mode = None

# --- Roteamento ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        b64 = image_to_base64(logo)
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="max-width:200px;"></div>', unsafe_allow_html=True)
    st.markdown('<br><br>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 0.6, 1])
    with col:
        st.button("ACESSAR SISTEMA", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<h1 class="section-title">SELEÇÃO DE USUÁRIO</h1>', unsafe_allow_html=True)
    _, col_center, _ = st.columns([0.1, 1, 0.1])
    with col_center:
        c1, c2, c3 = st.columns(3)
        for key, name, initial in [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]:
            with (c1 if key=="jean" else c2 if key=="thiago" else c3):
                st.markdown(f'<div class="profile-card"><div class="avatar-initial">{initial}</div><div style="font-weight:600; font-size:0.9rem;">{name}</div></div>', unsafe_allow_html=True)
                if st.button("SELECIONAR", key=f"sel_{key}"): navigate(key); st.rerun()
    st.markdown('<br>', unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 0.4, 1])
    with col_back:
        st.button("VOLTAR", on_click=navigate, args=('home',))

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    
    current_user = st.session_state.page
    st.markdown(f'<h1 class="section-title">PRONTUÁRIO: {name_map[current_user]}</h1>', unsafe_allow_html=True)
    
    # Exibição do Documento
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    st.markdown('<div class="document-wrapper">', unsafe_allow_html=True)
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- GRID DE AÇÕES (Nova Disposição) ---
    
    # Bloco 1: Navegação de Páginas do Documento
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("PÁGINA ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with nav_col2:
        if st.button("PRÓXIMA PÁGINA"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)

    # Bloco 2: Consultas de Dados
    data_col1, data_col2 = st.columns(2)
    with data_col1:
        if st.button("CONSULTAR FREQUÊNCIA"): st.session_state.view_mode = 'freq'; st.rerun()
    with data_col2:
        if st.button("CONSULTAR NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()

    st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)

    # Bloco 3: Ferramentas e Saída
    tool_col1, tool_col2 = st.columns(2)
    with tool_col1:
        if st.button("VALIDAR QR CODE"): st.session_state.view_mode = 'qr'; st.rerun()
    with tool_col2:
        st.markdown('<div class="exit-btn">', unsafe_allow_html=True)
        st.button("ENCERRAR SESSÃO", on_click=navigate, args=('login',))
        st.markdown('</div>', unsafe_allow_html=True)

    # Exibição de Tabelas
    if st.session_state.view_mode:
        st.divider()
        user_data = get_student_data(name_map[current_user])
        if st.session_state.view_mode == 'notas':
            st.table(user_data["Notas"])
        elif st.session_state.view_mode == 'freq':
            st.table(user_data["Frequência"])
        elif st.session_state.view_mode == 'qr':
            qr = load_image("qrcode.png")
            if qr:
                _, qcol, _ = st.columns([1, 0.4, 1])
                with qcol: st.image(qr, use_container_width=True)
