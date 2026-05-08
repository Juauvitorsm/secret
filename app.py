import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página
st.set_page_config(
    page_title="Identificação Digital",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Funções ---
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

# --- CSS: DESIGN INTEGRADO E TELA CHEIA ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* CARD DE VALIDADE: Cor Ajustada para combinar com o ID */
    .validade-card {
        background: linear-gradient(90deg, #0056b3 0%, #007bff 100%);
        color: white;
        padding: 20px;
        text-align: left;
        width: 100vw;
        border-bottom: 2px solid #00f2fe;
    }
    .val-label { font-size: 0.75rem; font-weight: 400; opacity: 0.9; }
    .val-date { font-size: 1.2rem; font-weight: 700; margin-bottom: 12px; }
    .val-box {
        background: rgba(255, 255, 255, 0.9);
        color: #0056b3;
        padding: 8px 20px;
        border-radius: 8px;
        display: inline-block;
    }

    /* Ajuste das Tabs para parecerem um menu de fotos */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        justify-content: center;
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        font-weight: 700;
        font-size: 0.8rem;
    }

    /* Botões de Função */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 2px !important;
        width: 100vw !important;
        margin: 0 !important;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        height: 55px !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        border: 1px solid #e9ecef !important;
    }

    .stImage img { width: 100vw !important; border-radius: 0px; }
    
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Navegação ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'view' not in st.session_state: st.session_state.view = None

def navigate(p):
    st.session_state.page = p
    st.session_state.view = None

# --- Fluxo ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 20vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:220px;"></div>', unsafe_allow_html=True)
    st.button("ACESSAR IDENTIFICAÇÃO", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div style="padding:20px; text-align:center; font-weight:700;">SELECIONE O ALUNO</div>', unsafe_allow_html=True)
    for key, name, initial in [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]:
        if st.button(f"👤 {name}", key=f"btn_{key}"): navigate(key); st.rerun()

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    files = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current = st.session_state.page
    
    st.markdown(f'<div style="padding:15px; text-align:center; font-weight:700; background:white;">IDENTIFICAÇÃO: {names[current]}</div>', unsafe_allow_html=True)
    
    # --- TROCA DE FOTOS POR ABAS (Simula Swipe no Celular) ---
    tab_frente, tab_verso = st.tabs(["FRENTE DO DOCUMENTO", "VERSO DO DOCUMENTO"])
    
    imgs = [load_image(f, rotate_degrees=90) for f in files[current]]
    
    with tab_frente:
        if imgs[0]: st.image(imgs[0], use_container_width=True)
        
    with tab_verso:
        if len(imgs) > 1: st.image(imgs[1], use_container_width=True)
        else: st.warning("Verso não disponível.")

    # --- CARD DE VALIDADE (Design Combinado) ---
    st.markdown(f"""
        <div class="validade-card">
            <div class="val-label">Data da Matrícula:</div>
            <div class="val-date">01/03/2019</div>
            <div class="val-box">
                <span style="font-size:0.7rem; font-weight:700;">VALIDADE:</span><br>
                <span style="font-size:1.2rem; font-weight:800;">30/06/2026</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Botões de Função Acadêmica
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if st.button("FREQ."): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view = 'n'; st.rerun()
    with f3:
        if st.button("QR"): st.session_state.view = 'q'; st.rerun()
    with f4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    # Dados
    if st.session_state.view == 'q':
        qr = load_image("qrcode.png")
        if qr:
            st.markdown("<br>", unsafe_allow_html=True)
            _, qc, _ = st.columns([1, 2, 1])
            with qc: st.image(qr, use_container_width=True)
