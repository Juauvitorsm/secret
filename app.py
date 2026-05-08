import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página (DEVE SER A PRIMEIRA LINHA)
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
            "Matéria": ["Anatomia", "Fisiologia do Exercício", "Cinesiologia", "Práticas Corporais"],
            "Nota": [8.5, 7.2, 9.8, 8.0],
            "Resultado": ["Aprovado", "Aprovado", "Aprovado", "Aprovado"]
        }),
        "Frequência": pd.DataFrame({
            "Unidade": ["Biomecânica", "Esportes Coletivos", "Psicologia do Esporte"],
            "Presença": ["95%", "100%", "88%"],
            "Faltas": [1, 0, 3]
        })
    }

# --- CSS DE ALTA FIDELIDADE: TELA CHEIA E SIMETRIA ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* REMOVE MARGENS PARA TELA CHEIA NO CELULAR */
    .block-container { 
        padding-top: 0rem !important; 
        padding-left: 0rem !important; 
        padding-right: 0rem !important; 
        max-width: 100% !important; 
        margin: 0 !important;
    }

    /* Título e Identidade */
    .section-title {
        color: #1a237e;
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        margin: 15px 0 10px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .top-accent {
        height: 6px;
        background-color: #1a237e;
        width: 100%;
        margin-top: 0px;
    }

    /* GRID DE BOTÕES: LADO A LADO E COLADO */
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

    /* Botões: Estilo 'Bloco Sólido' */
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
        border-color: #1a237e !important;
    }

    /* Imagem: Largura total sem bordas */
    .stImage img {
        width: 100vw !important;
        border-radius: 0px;
        margin-bottom: 0px !important;
        display: block;
    }

    /* Cards de Perfil */
    .profile-item {
        background: white;
        padding: 15px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    /* Ocultar elementos nativos do Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Gestão de Estado de Navegação ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'img_idx' not in st.session_state: st.session_state.img_idx = 0
if 'view' not in st.session_state: st.session_state.view = None

def navigate(p):
    st.session_state.page = p
    st.session_state.img_idx = 0
    st.session_state.view = None

# --- Estrutura das Páginas ---

if st.session_state.page == 'home':
    # Tela de Entrada
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:200px;"></div>', unsafe_allow_html=True)
    st.button("ACESSAR SISTEMA", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    # Tela de Seleção de Perfil
    st.markdown('<div class="section-title">IDENTIFIQUE-SE</div>', unsafe_allow_html=True)
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    for key, name, initial in profiles:
        st.markdown(f'<div class="profile-item"><div style="background:#1a237e; color:white; width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700;">{initial}</div><b>ALUNO: {name}</b></div>', unsafe_allow_html=True)
        if st.button(f"ACESSAR {name}", key=f"btn_{key}"):
            navigate(key)
            st.rerun()

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    # Tela da Carteirinha Acadêmica
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    # Usando o mesmo arquivo para simular frente e verso compatíveis
    users = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "3.png"], "hemilly": ["5.png", "6.png"]} 
    current = st.session_state.page
    
    st.markdown(f'<div class="section-title">IDENTIFICAÇÃO: {names[current]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="top-accent"></div>', unsafe_allow_html=True)
    
    # Imagem da Carteirinha
    imgs = [load_image(f, rotate_degrees=90) for f in users[current]]
    if imgs[st.session_state.img_idx]:
        st.image(imgs[st.session_state.img_idx], use_container_width=True)

    # Navegação entre Imagens (Anterior/Próximo)
    n1, n2 = st.columns(2)
    with n1:
        if st.button("Anterior"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(imgs); st.rerun()
    with n2:
        if st.button("Próximo"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(imgs); st.rerun()

    # Barra de Ferramentas Acadêmicas
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if st.button("FREQ."): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view = 'n'; st.rerun()
    with f3:
        if st.button("QR CODE"): st.session_state.view = 'q'; st.rerun()
    with f4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    # Área de Dados Dinâmicos
    if st.session_state.view:
        st.markdown("<br>", unsafe_allow_html=True)
        data = get_student_data()
        
        if st.session_state.view == 'f':
            st.table(data["Frequência"])
        
        elif st.session_state.view == 'n':
            st.table(data["Notas"])
            
        elif st.session_state.view == 'q':
            qr = load_image("qrcode.png")
            if qr:
                # Centraliza o QR Code
                _, qc, _ = st.columns([1, 1.5, 1])
                with qc: st.image(qr, use_container_width=True)
