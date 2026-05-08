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

def get_student_data(name):
    return {
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

# --- CSS REVISADO: LARGURA AMPLIADA E AJUSTE DE TEXTO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #f0f2f5; }

    /* Aumentei para 550px para dar mais respiro e preencher a tela */
    .block-container { 
        padding-top: 1.5rem !important; 
        max-width: 550px !important; 
        margin: auto;
    }

    .top-line {
        height: 5px;
        background-color: #1a237e;
        width: 100%;
        border-radius: 4px 4px 0 0;
    }

    .page-title {
        text-align: center;
        color: #111827;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 15px;
        text-transform: uppercase;
    }

    /* Grid de botões sem quebra */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        margin-top: -1px !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    /* Botões: Fonte ajustada para NOTAS não quebrar */
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        height: 48px !important;
        font-weight: 700 !important;
        font-size: 0.62rem !important; /* Reduzi um pouco para garantir simetria */
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e5e7eb !important;
        padding: 0px 2px !important; /* Reduzi o padding lateral interno */
        white-space: nowrap !important; /* Impede a quebra de linha do texto */
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
    }

    .stImage img {
        width: 100% !important;
        border-radius: 0px;
        margin-bottom: 0px !important;
        display: block;
        border-left: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
    }

    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Lógica de Navegação ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'img_idx' not in st.session_state: st.session_state.img_idx = 0
if 'view_mode' not in st.session_state: st.session_state.view_mode = None

def navigate(page):
    st.session_state.page = page
    st.session_state.img_idx = 0
    st.session_state.view_mode = None

# --- Telas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:220px;"></div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.button("ACESSAR PORTAL", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="page-title">IDENTIFIQUE-SE</div>', unsafe_allow_html=True)
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    for key, name, initial in profiles:
        if st.button(f"PERFIL: {name}", key=f"btn_{key}"):
            navigate(key)
            st.rerun()
    st.button("VOLTAR", on_click=navigate, args=('home',))

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current_user = st.session_state.page
    
    st.markdown(f'<div class="page-title">PRONTUÁRIO: {name_map[current_user]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)
    
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)

    # Navegação colada
    n1, n2 = st.columns(2)
    with n1:
        if st.button("ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with n2:
        if st.button("PRÓXIMO"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    # Funções na base
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        if st.button("FREQ."): st.session_state.view_mode = 'freq'; st.rerun()
    with t2:
        if st.button("NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()
    with t3:
        if st.button("QR CODE"): st.session_state.view_mode = 'qr'; st.rerun()
    with t4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    if st.session_state.view_mode:
        st.markdown("<br>", unsafe_allow_html=True)
        data = get_student_data(name_map[current_user])
        if st.session_state.view_mode == 'notas': st.table(data["Notas"])
        elif st.session_state.view_mode == 'freq': st.table(data["Frequência"])
        elif st.session_state.view_mode == 'qr':
            qr = load_image("qrcode.png")
            if qr:
                _, qc, _ = st.columns([1, 1, 1])
                with qc: st.image(qr, use_container_width=True)
