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

# --- Estilização CSS Profissional ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8f9fb;
    }

    /* Títulos */
    .section-title {
        color: #1a237e;
        font-weight: 700;
        font-size: 1.6rem;
        text-align: center;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: -0.5px;
    }

    /* FORÇAR BOTÕES LADO A LADO NO MOBILE */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
    }

    /* Container do Documento */
    .document-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 10px;
        border: 1px solid #eef0f2;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    /* Estilo dos Botões Profissionais */
    div.stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        height: 54px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        background-color: white !important;
        color: #1a237e !important;
        border: 1px solid #d1d9e6 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: white !important;
        border-color: #1a237e !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(26, 35, 126, 0.2) !important;
    }

    /* Cards de Perfil */
    .profile-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 1px solid #eef0f2;
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }
    .avatar {
        width: 60px; height: 60px;
        background-color: #e8eaf6;
        color: #1a237e;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; font-weight: 700; margin: 0 auto 10px auto;
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

# --- Páginas ---

# 1. HOME
if st.session_state.page == 'home':
    st.markdown('<div style="height: 12vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        b64 = image_to_base64(logo)
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="max-width:250px; border-radius: 20px;"></div>', unsafe_allow_html=True)
    
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
            st.markdown('<div class="profile-card"><div class="avatar">J</div><div style="font-weight:700;">JEAM</div></div>', unsafe_allow_html=True)
            if st.button("SELECIONAR", key="sel_j"): navigate('jean'); st.rerun()

        with c2:
            st.markdown('<div class="profile-card"><div class="avatar">T</div><div style="font-weight:700;">THIAGO</div></div>', unsafe_allow_html=True)
            if st.button("SELECIONAR", key="sel_t"): navigate('thiago'); st.rerun()

        with c3:
            st.markdown('<div class="profile-card"><div class="avatar">H</div><div style="font-weight:700;">HEMILLY</div></div>', unsafe_allow_html=True)
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
    st.markdown(f'<h1 class="section-title">{name_map[current_user]}</h1>', unsafe_allow_html=True)
    
    # Documento (Mantendo a sua rotação de 90 graus original)
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    st.markdown('<div class="document-card">', unsafe_allow_html=True)
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegação entre imagens (Sempre lado a lado)
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with nav2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # Ações Principais (Grade organizada)
    act1, act2 = st.columns(2)
    with act1:
        if st.button("📊 FREQUÊNCIA"): st.session_state.view_mode = 'freq'; st.rerun()
    with act2:
        if st.button("📝 NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()

    act3, act4 = st.columns(2)
    with act3:
        if st.button("📱 QR CODE"): st.session_state.view_mode = 'qr'; st.rerun()
    with act4:
        st.button("🔙 SAIR", on_click=navigate, args=('login',))

    # Área de Dados Dinâmicos
    if st.session_state.view_mode:
        st.divider()
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
                _, qcol, _ = st.columns([1, 0.6, 1])
                with qcol: st.image(qr, use_container_width=True)
