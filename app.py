import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página
st.set_page_config(
    page_title="Sistema de Identificação Acadêmica",
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

def get_student_data():
    return {
        "Notas": pd.DataFrame({
            "Matéria": [
                "Anatomia Humana", 
                "Fisiologia do Exercício", 
                "Cinesiologia", 
                "Psicologia do Esporte",
                "Metodologia do Treinamento"
            ],
            "Nota": [9.0, 8.5, 7.8, 9.5, 8.2],
            "Resultado": ["Aprovado", "Aprovado", "Aprovado", "Aprovado", "Aprovado"]
        }),
        "Frequência": pd.DataFrame({
            "Unidade Curricular": [
                "Práticas Corporais", 
                "Esportes Coletivos", 
                "Atletismo", 
                "Dança e Ritmo"
            ],
            "Presença": ["98%", "92%", "100%", "85%"],
            "Faltas": [0, 2, 0, 4]
        })
    }

# --- CSS PARA TELA CHEIA E IDENTIDADE VISUAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .block-container { 
        padding-top: 0.5rem !important; 
        padding-left: 0rem !important; 
        padding-right: 0rem !important; 
        max-width: 100% !important; 
        margin: 0 !important;
    }

    .page-title {
        text-align: center;
        color: #1a237e;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 10px 0;
        text-transform: uppercase;
    }

    .top-line {
        height: 6px;
        background-color: #1a237e;
        width: 100%;
    }

    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
        margin-top: -1px !important;
        width: 100vw !important;
    }
    
    [data-testid="column"] {
        flex: 1 !important;
        padding: 0px !important;
        min-width: 0px !important;
    }

    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        height: 52px !important;
        font-weight: 700 !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e5e7eb !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
    }

    .stImage img {
        width: 100vw !important;
        border-radius: 0px;
        margin-bottom: 0px !important;
        display: block;
    }

    .profile-box {
        background: white;
        padding: 15px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Gestão de Navegação ---
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
    st.button("INICIAR IDENTIFICAÇÃO", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="page-title">SELECIONE O ALUNO</div>', unsafe_allow_html=True)
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    for key, name, initial in profiles:
        st.markdown(f'<div class="profile-box"><div style="background:#1a237e; color:white; width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700;">{initial}</div><b>ALUNO: {name}</b></div>', unsafe_allow_html=True)
        if st.button(f"ABRIR IDENTIFICAÇÃO - {name}", key=f"btn_{key}"):
            navigate(key)
            st.rerun()

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    files = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current = st.session_state.page
    
    st.markdown(f'<div class="page-title">IDENTIFICAÇÃO: {names[current]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)
    
    imgs = [load_image(f, rotate_degrees=90) for f in files[current]]
    if imgs[st.session_state.img_idx]:
        st.image(imgs[st.session_state.img_idx], use_container_width=True)

    n1, n2 = st.columns(2)
    with n1:
        if st.button("← VOLTAR PÁGINA"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(imgs); st.rerun()
    with n2:
        if st.button("PRÓXIMA PÁGINA →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(imgs); st.rerun()

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if st.button("FREQ."): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view = 'n'; st.rerun()
    with f3:
        if st.button("QR CODE"): st.session_state.view = 'q'; st.rerun()
    with f4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    if st.session_state.view:
        st.markdown("<br>", unsafe_allow_html=True)
        data = get_student_data()
        
        if st.session_state.view == 'f':
            st.markdown("<h5 style='text-align:center;'>Frequência - Educação Física</h5>", unsafe_allow_html=True)
            st.table(data["Frequência"])
        
        elif st.session_state.view == 'n':
            st.markdown("<h5 style='text-align:center;'>Boletim - Ciclo Atual</h5>", unsafe_allow_html=True)
            st.table(data["Notas"])
            
        elif st.session_state.view == 'q':
            st.markdown("<h5 style='text-align:center;'>Autenticação Digital</h5>", unsafe_allow_html=True)
            qr_img = load_image("qrcode.png")
            if qr_img:
                _, q_col, _ = st.columns([1, 2, 1])
                with q_col: st.image(qr_img, use_container_width=True)
