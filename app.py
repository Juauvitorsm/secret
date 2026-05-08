import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# Configuração da página
st.set_page_config(
    page_title="Portal do Estudante - Gestão de Documentos",
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
    data = {
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
    return data

# --- Estilização CSS de Alta Fidelidade (UI/UX) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8fafc;
    }

    /* Redução de Gaps Padrão do Streamlit */
    .block-container { padding-top: 1.5rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }

    /* Cabeçalho de Perfil */
    .student-header {
        text-align: center;
        padding: 10px 0;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .student-name {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Forçar colunas lado a lado no Mobile */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0px !important;
    }

    /* Card do Documento (Efeito Carteirinha) */
    .document-wrapper {
        background: #ffffff;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    /* Botões: Estilo Dashboard Administrativo */
    div.stButton > button {
        width: 100% !important;
        border-radius: 8px !important;
        height: 45px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    div.stButton > button:hover {
        background-color: #1a237e !important;
        color: #ffffff !important;
        border-color: #1a237e !important;
        transform: translateY(-1px);
    }

    /* Botão de Navegação de Imagem (Mais discreto) */
    .nav-btn div.stButton > button {
        background-color: #f1f5f9 !important;
        border: none !important;
        color: #475569 !important;
    }

    /* Botão de Sair */
    .exit-btn div.stButton > button {
        background-color: #fff1f2 !important;
        color: #be123c !important;
        border-color: #fecdd3 !important;
    }
    .exit-btn div.stButton > button:hover {
        background-color: #be123c !important;
        color: #ffffff !important;
    }

    /* Grid de Seleção de Usuário */
    .profile-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .avatar-initial {
        width: 55px; height: 55px;
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        color: white;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; font-weight: 700; margin: 0 auto 15px auto;
    }

    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Gestão de Navegação ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'img_idx' not in st.session_state:
    st.session_state.img_idx = 0
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = None

def navigate(page):
    st.session_state.page = page
    st.session_state.img_idx = 0
    st.session_state.view_mode = None

# --- Roteamento ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 12vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        b64 = image_to_base64(logo)
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    st.markdown('<br><br>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 0.7, 1])
    with col:
        st.button("ENTRAR NO PORTAL", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="student-header"><span class="student-name">ACESSO AO SISTEMA</span></div>', unsafe_allow_html=True)
    _, col_center, _ = st.columns([0.05, 1, 0.05])
    with col_center:
        c1, c2, c3 = st.columns(3)
        profiles = [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]
        for i, (key, name, initial) in enumerate(profiles):
            with (c1 if i==0 else c2 if i==1 else c3):
                st.markdown(f'<div class="profile-card"><div class="avatar-initial">{initial}</div><div style="font-weight:600; color:#1e293b; font-size:0.9rem; margin-bottom:10px;">{name}</div></div>', unsafe_allow_html=True)
                if st.button("ACESSAR", key=f"sel_{key}"): navigate(key); st.rerun()
    st.markdown('<br>', unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 0.4, 1])
    with col_back:
        st.button("VOLTAR", on_click=navigate, args=('home',))

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    name_map = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    file_map = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    
    current_user = st.session_state.page
    
    # Header do Aluno
    st.markdown(f'<div class="student-header"><span class="student-name">CENTRAL DO ALUNO: {name_map[current_user]}</span></div>', unsafe_allow_html=True)
    
    # Documento Principal
    images = [load_image(f, rotate_degrees=90) for f in file_map[current_user]]
    st.markdown('<div class="document-wrapper">', unsafe_allow_html=True)
    if images[st.session_state.img_idx]:
        st.image(images[st.session_state.img_idx], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MENU DE AÇÕES ORGANIZADO ---
    
    # Bloco 1: Controle do Documento (Navegação Interna)
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    nav_c1, nav_c2 = st.columns(2)
    with nav_c1:
        if st.button("ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(images); st.rerun()
    with nav_c2:
        if st.button("PRÓXIMO"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(images); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Bloco 2: Consultas Acadêmicas
    data_c1, data_c2 = st.columns(2)
    with data_c1:
        if st.button("FREQUÊNCIA"): st.session_state.view_mode = 'freq'; st.rerun()
    with data_c2:
        if st.button("NOTAS"): st.session_state.view_mode = 'notas'; st.rerun()

    # Bloco 3: Ferramentas e Segurança
    tool_c1, tool_c2 = st.columns(2)
    with tool_c1:
        if st.button("QR CODE"): st.session_state.view_mode = 'qr'; st.rerun()
    with tool_c2:
        st.markdown('<div class="exit-btn">', unsafe_allow_html=True)
        if st.button("SAIR"): navigate('login'); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Área de Exibição de Dados (Tabelas e QR)
    if st.session_state.view_mode:
        st.markdown("<br>", unsafe_allow_html=True)
        user_data = get_student_data(name_map[current_user])
        with st.expander("INFORMAÇÕES DETALHADAS", expanded=True):
            if st.session_state.view_mode == 'notas':
                st.write("**Histórico Acadêmico de Notas**")
                st.table(user_data["Notas"])
            elif st.session_state.view_mode == 'freq':
                st.write("**Relatório de Presença em Aula**")
                st.table(user_data["Frequência"])
            elif st.session_state.view_mode == 'qr':
                qr = load_image("qrcode.png")
                if qr:
                    st.write("**Validação de Autenticidade Digital**")
                    _, qcol, _ = st.columns([1, 0.6, 1])
                    with qcol: st.image(qr, use_container_width=True)
