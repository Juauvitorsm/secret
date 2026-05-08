import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# Configuração da página (deve ser o primeiro comando)
st.set_page_config(
    page_title="Sistema de Documentos Digitais",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Funções de Backend ---
@st.cache_data
def load_image(image_path, rotate_degrees=0):
    """Carrega imagem e aplica rotação se necessário."""
    try:
        # Nota: Para manter a imagem EXATAMENTE como no print, 
        # o arquivo de origem já deve estar deitado, então rotate_degrees deve ser 0.
        image = Image.open(image_path)
        if rotate_degrees != 0:
            return image.rotate(rotate_degrees, expand=True)
        return image
    except Exception:
        return None

def image_to_base64(image):
    """Converte objeto PIL para string base64 para uso em HTML."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- CSS Profissional e Alinhado ---
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
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    /* Documento (Alinhamento e Sombra) */
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 25px;
    }
    .stImage img {
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        max-width: 100% !important;
    }

    /* Container Global de Botões (Otimizado Mobile) */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 calc(50% - 10px) !important;
        min-width: calc(50% - 10px) !important;
    }

    /* Estilização Geral dos Botões */
    div.stButton > button {
        width: 100% !important;
        border-radius: 10px !important;
        height: 52px !important; /* Altura ideal para toque */
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #d1d9e6 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease;
        text-transform: uppercase;
        margin-bottom: 0px;
    }

    /* Efeito de Hover/Clique */
    div.stButton > button:hover, div.stButton > button:focus {
        border-color: #1a237e !important;
        background-color: #f0f2ff !important;
        color: #1a237e !important;
    }

    /* Espaçador Profissional */
    .div-bar {
        height: 1px;
        background-color: #e0e0e0;
        margin: 25px 0;
    }

    /* Ocultar elementos Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Gestão de Navegação e Estado ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'img_idx' not in st.session_state:
    st.session_state.img_idx = 0

def navigate(page):
    st.session_state.page = page
    st.session_state.img_idx = 0

# --- Lógica das Páginas ---

# 1. HOME (Entrada)
if st.session_state.page == 'home':
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        b64 = image_to_base64(logo)
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="max-width:280px; border-radius:15px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);"></div>', unsafe_allow_html=True)
    
    st.markdown('<br><br>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 0.7, 1])
    with col:
        st.button("ACESSAR SISTEMA", on_click=navigate, args=('login',))

# 2. LOGIN (Seleção de Usuário)
elif st.session_state.page == 'login':
    st.markdown('<h1 class="section-title">Quem está acessando?</h1>', unsafe_allow_html=True)
    
    _, col_center, _ = st.columns([0.1, 1, 0.1])
    with col_center:
        # Grid de usuários 2x1 no mobile
        c1, c2 = st.columns(2)
        with c1:
            st.button("👤 JEAM", key="sel_j", on_click=navigate, args=('jean',))
        with c2:
            st.button("👤 THIAGO", key="sel_t", on_click=navigate, args=('thiago',))
        
        # Centralizar o terceiro botão
        _, c3, _ = st.columns([0.5, 1, 0.5])
        with c3:
            st.button("👤 HEMILLY", key="sel_h", on_click=navigate, args=('hemilly',))

    st.markdown('<div class="div-bar"></div>', unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 0.5, 1])
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
    
    # Título do Aluno
    st.markdown(f'<h1 class="section-title">DOCUMENTOS: {name_map[current_user]}</h1>', unsafe_allow_html=True)
    
    # EXIBIÇÃO DO DOCUMENTO (MANTIDO EXATAMENTE COMO NO PRINT)
    # Assumindo que a imagem original já está na orientação correta.
    # Se ela estiver deitada e você quiser que ela apareça deitada, rotate_degrees=0.
    images = [load_image(f, rotate_degrees=0) for f in file_map[current_user]]
    
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)
    else:
        st.error(f"Erro ao carregar imagem: {file_map[current_user][st.session_state.img_idx]}")

    # --- ORGANIZAÇÃO PROFISSIONAL DOS BOTÕES ---

    # 1. Navegação de Imagem (Lado a Lado)
    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with nav2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    # 2. Funções (Grid Profissional)
    st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
    func1, func2 = st.columns(2)
    with func1:
        st.button("📊 Frequência")
    with func2:
        st.button("📝 Notas")

    st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
    func3, func4 = st.columns(2)
    with func3:
        st.button("📱 QR Code")
    with func4:
        st.button("🔙 Sair", on_click=navigate, args=('login',))