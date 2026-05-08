import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página
st.set_page_config(
    page_title="Portal do Estudante",
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

# --- CSS PARA SIMETRIA E ALINHAMENTO (BOTÕES LADO A LADO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Remove as margens das laterais da página para a foto e botões ocuparem tudo */
    .block-container { 
        padding-top: 1rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
    }

    /* Remove o espaçamento entre as colunas para os botões "colarem" na largura da foto */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        justify-content: space-between !important;
        width: 100% !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
    }

    /* Estilo dos Botões - Ajustado para simetria */
    div.stButton > button {
        width: 100% !important;
        border-radius: 4px !important;
        height: 42px !important;
        font-weight: 700 !important;
        font-size: 0.65rem !important;
        padding: 0px !important;
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #d1d5db !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
        border-color: #1a237e !important;
    }

    /* Ajuste da Imagem para garantir que ela seja a régua de largura */
    .stImage img {
        width: 100% !important;
        border-radius: 4px;
        margin-bottom: 0.2rem !important;
    }

    /* Ocultar elementos desnecessários */
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Navegação ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'img_idx' not in st.session_state: st.session_state.img_idx = 0
if 'view_mode' not in st.session_state: st.session_state.view_mode = None

def navigate(page):
    st.session_state.page = page
    st.session_state.img_idx = 0
    st.session_state.view_mode = None

# --- Fluxo de Telas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 0.8, 1])
    with col: st.button("ACESSAR", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div style="text-align:center; font-weight:700; color:#1a237e; margin-bottom:20px;">SELECIONE O PERFIL</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    for i, (key, name, initial) in enumerate(profiles):
        with (c1 if i==0 else c2 if i==1 else c3):
            st.markdown(f'<div style="text-align:center; background:white; padding:15px; border-radius:12px; border:1px solid #eee; margin-bottom:10px;"><div style="width:40px; height:40px; background:#1a237e; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 10px auto; font-weight:700;">{initial}</div><div style="font-size:0.75rem; font-weight:600;">{name}</div></div>', unsafe_allow_html=True)
            if st.button("ENTRAR", key=f"sel_{key}"): navigate(key); st.rerun()

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current_user = st.session_state.page
    
    # Foto do Documento
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)

    # --- LINHA 1: NAVEGAÇÃO (SIMÉTRICA À FOTO) ---
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with nav2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    # --- LINHA 2: FUNÇÕES (4 BOTÕES LADO A LADO - SIMÉTRICOS À FOTO) ---
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        if st.button("FREQ."): st.session_state.view_mode = 'freq'; st.rerun()
    with t2:
        if st.button("NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()
    with t3:
        if st.button("QR"): st.session_state.view_mode = 'qr'; st.rerun()
    with t4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    # Área de Dados
    if st.session_state.view_mode:
        st.divider()
        data = get_student_data(name_map[current_user])
        if st.session_state.view_mode == 'notas': st.table(data["Notas"])
        elif st.session_state.view_mode == 'freq': st.table(data["Frequência"])
        elif st.session_state.view_mode == 'qr':
            qr = load_image("qrcode.png")
            if qr:
                _, qcol, _ = st.columns([1, 1, 1])
                with qcol: st.image(qr, use_container_width=True)
