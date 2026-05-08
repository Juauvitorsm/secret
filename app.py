import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da Página
st.set_page_config(
    page_title="Portal Digital",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Funções de Suporte (Imagens e Dados)
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

# 3. CSS Customizado (Correção Mobile + Visual Profissional)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f8f9fa; }

    /* FORÇAR COLUNAS LADO A LADO NO MOBILE */
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

    /* Estilo dos Botões */
    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #d1d9e6 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    div.stButton > button:hover {
        border-color: #1a237e !important;
        background-color: #f0f2ff !important;
    }

    /* Estilo dos Cards de Perfil */
    .profile-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #eee;
        margin-bottom: 10px;
    }
    .avatar {
        width: 60px; height: 60px;
        background: #e8eaf6;
        color: #1a237e;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 10px auto;
        font-weight: 700; font-size: 1.5rem;
    }

    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 4. Gestão de Navegação
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'img_idx' not in st.session_state: st.session_state.img_idx = 0
if 'view' not in st.session_state: st.session_state.view = None

def navigate(page):
    st.session_state.page = page
    st.session_state.img_idx = 0
    st.session_state.view = None

# --- ROTEAMENTO DE PÁGINAS ---

# PÁGINA: HOME
if st.session_state.page == 'home':
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:250px; border-radius:12px;"></div>', unsafe_allow_html=True)
    st.markdown('<br><br>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 0.8, 1])
    with col:
        st.button("ENTRAR NO PORTAL", on_click=navigate, args=('login',))

# PÁGINA: LOGIN (SELEÇÃO)
elif st.session_state.page == 'login':
    st.markdown("<h2 style='text-align:center; color:#1a237e;'>IDENTIFIQUE-SE</h2>", unsafe_allow_html=True)
    
    # Grid de Usuários
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="profile-card"><div class="avatar">J</div>JEAM</div>', unsafe_allow_html=True)
        st.button("ACESSAR", key="j", on_click=navigate, args=('jean',))
    with c2:
        st.markdown('<div class="profile-card"><div class="avatar">T</div>THIAGO</div>', unsafe_allow_html=True)
        st.button("ACESSAR", key="t", on_click=navigate, args=('thiago',))
    
    _, c3, _ = st.columns([0.5, 1, 0.5])
    with c3:
        st.markdown('<div class="profile-card"><div class="avatar">H</div>HEMILLY</div>', unsafe_allow_html=True)
        st.button("ACESSAR", key="h", on_click=navigate, args=('hemilly',))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("VOLTAR AO INÍCIO", on_click=navigate, args=('home',))

# PÁGINAS DE DOCUMENTOS
elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    users = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    
    current = st.session_state.page
    st.markdown(f"<h3 style='text-align:center; color:#1a237e;'>DOCUMENTOS: {names[current]}</h3>", unsafe_allow_html=True)
    
    # Imagem (Mantendo como você pediu: em pé/conforme arquivo)
    imgs = [load_image(f) for f in users[current]]
    if imgs[st.session_state.img_idx]:
        st.image(imgs[st.session_state.img_idx], use_container_width=True)

    # GRID DE BOTÕES (Obrigatório 2 por linha no Mobile)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Linha 1: Navegação
    n1, n2 = st.columns(2)
    with n1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(imgs); st.rerun()
    with n2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(imgs); st.rerun()

    # Linha 2: Funções
    f1, f2 = st.columns(2)
    with f1:
        if st.button("FREQUÊNCIA"): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view = 'n'; st.rerun()

    # Linha 3: Extras
    e1, e2 = st.columns(2)
    with e1:
        if st.button("QR CODE"): st.session_state.view = 'q'; st.rerun()
    with e2:
        st.button("SAIR", on_click=navigate, args=('login',))

    # Exibição de Dados Fictícios
    data = get_student_data()
    if st.session_state.view == 'n':
        st.divider(); st.markdown("#### Histórico de Notas"); st.table(data["Notas"])
    elif st.session_state.view == 'f':
        st.divider(); st.markdown("#### Relatório de Presença"); st.table(data["Frequência"])
    elif st.session_state.view == 'q':
        qr = load_image("qrcode.png")
        if qr: 
            st.divider()
            _, qcol, _ = st.columns([1, 1, 1])
            with qcol: st.image(qr, width=150)