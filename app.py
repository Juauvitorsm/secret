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
    # Simulação de banco de dados para Notas e Frequência
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

# --- Estilização CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f4f7f6;
    }

    /* Títulos */
    .section-title {
        color: #1a237e;
        font-weight: 700;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    /* Cards de Perfil na Seleção de Usuário */
    .profile-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 10px;
    }
    .profile-card:hover {
        transform: translateY(-5px);
        border-color: #1a237e;
        box-shadow: 0 10px 20px rgba(26, 35, 126, 0.1);
    }
    .avatar {
        width: 70px;
        height: 70px;
        background-color: #e8eaf6;
        color: #1a237e;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 auto 15px auto;
    }

    /* Container do Documento */
    .document-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Botões */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 48px;
        font-weight: 600;
        transition: all 0.2s;
        text-transform: uppercase;
        border: 1px solid #1a237e;
    }
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: white !important;
    }

    /* Ocultar elementos Streamlit */
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

# --- Páginas ---

# 1. HOME
if st.session_state.page == 'home':
    st.markdown('<div style="height: 12vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        b64 = image_to_base64(logo)
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="max-width:250px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<br><br>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 0.6, 1])
    with col:
        st.button("ACESSAR PORTAL", on_click=navigate, args=('login',))

# 2. SELEÇÃO DE USUÁRIO (LOGIN)
elif st.session_state.page == 'login':
    st.markdown('<h1 class="section-title">Quem está acessando?</h1>', unsafe_allow_html=True)
    
    _, col_center, _ = st.columns([0.1, 1, 0.1])
    with col_center:
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown('<div class="profile-card"><div class="avatar">J</div><div style="font-weight:700;">JEAM</div><div style="font-size:0.8rem; color:#666;">Estudante</div></div>', unsafe_allow_html=True)
            if st.button("SELECIONAR", key="sel_j"): navigate('jean'); st.rerun()

        with c2:
            st.markdown('<div class="profile-card"><div class="avatar">T</div><div style="font-weight:700;">THIAGO</div><div style="font-size:0.8rem; color:#666;">Estudante</div></div>', unsafe_allow_html=True)
            if st.button("SELECIONAR", key="sel_t"): navigate('thiago'); st.rerun()

        with c3:
            st.markdown('<div class="profile-card"><div class="avatar">H</div><div style="font-weight:700;">HEMILLY</div><div style="font-size:0.8rem; color:#666;">Estudante</div></div>', unsafe_allow_html=True)
            if st.button("SELECIONAR", key="sel_h"): navigate('hemilly'); st.rerun()

    st.markdown('<br>', unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 0.4, 1])
    with col_back:
        st.button("VOLTAR", on_click=navigate, args=('home',))

# 3. PRONTUÁRIOS INDIVIDUAIS
elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {
        "jean": ["1.png", "2.png"],
        "thiago": ["3.png", "4.png"],
        "hemilly": ["5.png", "6.png"]
    }
    
    current_user = st.session_state.page
    st.markdown(f'<h1 class="section-title">DOCUMENTOS: {name_map[current_user]}</h1>', unsafe_allow_html=True)
    
    # Documento
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    st.markdown('<div class="document-card">', unsafe_allow_html=True)
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegação entre imagens
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with nav2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    st.divider()

    # Ações e Dados
    act1, act2, act3 = st.columns(3)
    with act1:
        if st.button("FREQUÊNCIA"): st.session_state.view_mode = 'freq'; st.rerun()
    with act2:
        if st.button("NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()
    with act3:
        if st.button("QR CODE"): st.session_state.view_mode = 'qr'; st.rerun()

    # Área de Dados Fictícios
    user_data = get_student_data(name_map[current_user])
    
    if st.session_state.view_mode == 'notas':
        st.markdown("### Histórico de Notas")
        st.table(user_data["Notas"])
    
    elif st.session_state.view_mode == 'freq':
        st.markdown("### Relatório de Frequência")
        st.table(user_data["Frequência"])
    
    elif st.session_state.view_mode == 'qr':
        qr = load_image("qrcode.png")
        if qr:
            _, qcol, _ = st.columns([1, 0.4, 1])
            with qcol: st.image(qr, use_container_width=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.button("SAIR DO PERFIL", on_click=navigate, args=('login',))
