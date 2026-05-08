import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# Configuração da página
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

# --- CSS DE ALTA PRECISÃO (Redução de Gaps e Compactação) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Redução drástica de espaços do Streamlit */
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0.4rem !important; }
    
    /* Forçar colunas lado a lado sem margens laterais */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important; /* Espaço mínimo entre botões */
        margin-bottom: -10px !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
    }

    /* Botões: Estilo Minimalista e Compacto */
    div.stButton > button {
        width: 100% !important;
        border-radius: 4px !important; /* Bordas levemente arredondadas (mais sério) */
        height: 42px !important; /* Mais curto */
        font-weight: 600 !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.02em !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e0e6ed !important;
        padding: 0px !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
    }

    /* Botão de Encerramento Sessão */
    .exit-btn div.stButton > button {
        background-color: #fcfcfc !important;
        color: #d32f2f !important;
    }

    /* Ajuste da Imagem */
    .stImage img {
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

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

# --- Estrutura das Páginas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 0.8, 1])
    with col: st.button("ACESSAR PORTAL", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<h3 style="text-align:center; color:#1a237e; font-size:1.1rem; margin-bottom:20px;">SELECIONE O PERFIL</h3>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.button("JEAM", on_click=navigate, args=('jean',))
        st.button("THIAGO", on_click=navigate, args=('thiago',))
        st.button("HEMILLY", on_click=navigate, args=('hemilly',))

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current_user = st.session_state.page
    
    # Título mais discreto
    st.markdown(f'<div style="text-align:center; color:#333; font-weight:700; font-size:0.9rem; margin-bottom:-10px;">PRONTUÁRIO: {name_map[current_user]}</div>', unsafe_allow_html=True)
    
    # Imagem
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)

    # --- MENU DE AÇÕES COMPACTO ---
    
    # Linha 1
    c1, c2 = st.columns(2)
    with c1:
        if st.button("ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with c2:
        if st.button("PRÓXIMO"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    # Linha 2
    c3, c4 = st.columns(2)
    with c3:
        if st.button("FREQUÊNCIA"): st.session_state.view_mode = 'freq'; st.rerun()
    with c4:
        if st.button("NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()

    # Linha 3
    c5, c6 = st.columns(2)
    with c5:
        if st.button("QR CODE"): st.session_state.view_mode = 'qr'; st.rerun()
    with c6:
        st.markdown('<div class="exit-btn">', unsafe_allow_html=True)
        st.button("SAIR", on_click=navigate, args=('login',))
        st.markdown('</div>', unsafe_allow_html=True)

    # Tabelas
    if st.session_state.view_mode:
        st.divider()
        data = get_student_data(name_map[current_user])
        if st.session_state.view_mode == 'notas': st.table(data["Notas"])
        elif st.session_state.view_mode == 'freq': st.table(data["Frequência"])
        elif st.session_state.view_mode == 'qr':
            qr = load_image("qrcode.png")
            if qr:
                _, qc, _ = st.columns([1, 0.5, 1])
                with qc: st.image(qr, use_container_width=True)
