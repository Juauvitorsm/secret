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

# --- CSS: BLOCO FIXO E SIMETRIA TOTAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Fundo geral mais escuro para destacar o bloco branco */
    .main { background-color: #f0f2f5; }

    /* Container Principal: Fixa o tamanho no Computador e Mobile */
    .block-container { 
        padding-top: 2rem !important; 
        max-width: 450px !important; /* Tamanho fixo ideal para simular um celular no PC */
        margin: auto;
    }

    /* Linha decorativa acima da foto */
    .top-line {
        height: 4px;
        background-color: #1a237e;
        width: 100%;
        border-radius: 4px 4px 0 0;
        margin-bottom: 0px;
    }

    /* Título da Página Interna */
    .page-title {
        text-align: center;
        color: #111827;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Forçar colunas lado a lado sem quebra */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important; /* Gap mínimo para simetria total */
        margin-top: -1px !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    /* Botões do Bloco */
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important; /* Bordas retas para efeito de bloco colado */
        height: 45px !important;
        font-weight: 700 !important;
        font-size: 0.65rem !important;
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e5e7eb !important;
        margin: 0px !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
    }

    /* Estilo da Imagem: Sem arredondamento embaixo para colar nos botões */
    .stImage img {
        width: 100% !important;
        border-radius: 0px;
        margin-bottom: 0px !important;
        display: block;
        border-left: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
    }

    /* Cards de Perfil na Seleção */
    .profile-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
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

# --- Roteamento de Telas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.button("ACESSAR PORTAL", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="page-title">IDENTIFIQUE-SE</div>', unsafe_allow_html=True)
    profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
    for key, name, initial in profiles:
        st.markdown(f'''
            <div class="profile-card">
                <div style="width:35px; height:35px; background:#1a237e; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700;">{initial}</div>
                <div style="font-weight:600; font-size:0.9rem;">{name}</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button(f"ENTRAR COMO {name}", key=f"btn_{key}"):
            navigate(key)
            st.rerun()
    st.markdown('<br>', unsafe_allow_html=True)
    st.button("VOLTAR", on_click=navigate, args=('home',))

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current_user = st.session_state.page
    
    # Título e Linha Decorativa
    st.markdown(f'<div class="page-title">PRONTUÁRIO: {name_map[current_user]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="top-line"></div>', unsafe_allow_html=True)
    
    # 1. Foto do Documento (Parte superior do bloco)
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)

    # 2. Navegação (Parte central do bloco)
    n1, n2 = st.columns(2)
    with n1:
        if st.button("ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with n2:
        if st.button("PRÓXIMO"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()

    # 3. Funções (Base do bloco)
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        if st.button("FREQ."): st.session_state.view_mode = 'freq'; st.rerun()
    with t2:
        if st.button("NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()
    with t3:
        if st.button("QR"): st.session_state.view_mode = 'qr'; st.rerun()
    with t4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    # Resultados (Fora do bloco fixo)
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
