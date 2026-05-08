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

# --- CSS DE ALTA FIDELIDADE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Redução de Gaps e Paddings para aproximar elementos */
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
    
    /* Forçar colunas lado a lado no mobile com gap mínimo */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        margin-top: -5px !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
    }

    /* Botões: Compactos e Profissionais */
    div.stButton > button {
        width: 100% !important;
        border-radius: 4px !important;
        height: 40px !important;
        font-weight: 600 !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.01em !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e0e6ed !important;
        text-transform: uppercase !important;
    }
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
        border-color: #1a237e !important;
    }

    /* Cards de Perfil (Restaurados) */
    .profile-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 8px;
    }
    .avatar-circle {
        width: 50px; height: 50px;
        background-color: #f3f4f6;
        color: #111827;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; font-weight: 700; margin: 0 auto 10px auto;
        border: 1px solid #e5e7eb;
    }

    /* Ajuste da Imagem para colar nos botões */
    .stImage img {
        border-radius: 6px;
        margin-bottom: 0px !important;
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
    st.markdown('<div style="text-align:center; color:#1a237e; font-weight:700; font-size:1.1rem; margin-bottom:20px;">IDENTIFIQUE-SE</div>', unsafe_allow_html=True)
    
    # Cards de Perfil Restaurados
    c1, c2, c3 = st.columns(3)
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    
    for key, name, initial in profiles:
        with (c1 if key=="jean" else c2 if key=="thiago" else c3):
            st.markdown(f'<div class="profile-card"><div class="avatar-circle">{initial}</div><div style="font-weight:600; font-size:0.8rem;">{name}</div></div>', unsafe_allow_html=True)
            if st.button("ENTRAR", key=f"btn_{key}"):
                navigate(key)
                st.rerun()

    st.markdown('<br>', unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 0.5, 1])
    with col_back: st.button("VOLTAR", on_click=navigate, args=('home',))

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current_user = st.session_state.page
    
    st.markdown(f'<div style="text-align:center; color:#333; font-weight:700; font-size:0.85rem; margin-bottom:-10px;">PRONTUÁRIO: {name_map[current_user]}</div>', unsafe_allow_html=True)
    
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)

    # --- GRID COMPACTO DE BOTÕES ---
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
        st.button("SAIR", on_click=navigate, args=('login',))

    # Exibição de Dados
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
