import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da Página (Deve ser o primeiro comando)
st.set_page_config(
    page_title="Portal Digital",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Funções de Suporte (Imagens e Dados) com Cache
@st.cache_data
def load_image(image_path, rotate_degrees=0):
    """Carrega imagem e aplica rotação APENAS se especificado."""
    try:
        image = Image.open(image_path)
        # Forçamos a não usar metadados de auto-rotação (EXIF)
        if hasattr(image, '_getexif'): 
            image = Image.open(image_path) # Reabre para limpar cache interno

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

# 3. CSS Profissional (Correção Mobile + Visual Limpo)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f8f9fa; }

    /* Estilo da Imagem do Documento - Evitar distorções */
    .stImage img {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        max-width: 100% !important;
        height: auto !important;
    }

    /* FORÇAR COLUNAS LADO A LADO NO MOBILE (Fix definitivo) */
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

    /* Estilo dos Botões - Fácil de clicar */
    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        color: #1a237e !important;
        border: 1px solid #e0e6ed !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        margin-bottom: 0px !important;
    }
    div.stButton > button:hover {
        border-color: #1a237e !important;
        background-color: #f0f2ff !important;
    }

    /* Títulos e Layout */
    .section-title {
        color: #1a237e;
        font-weight: 700;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 20px;
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
    st.markdown("<h2 class='section-title'>IDENTIFIQUE-SE</h2>", unsafe_allow_html=True)
    
    # Lista simples de botões para mobile
    _, col_center, _ = st.columns([0.1, 1, 0.1])
    with col_center:
        st.button("👤 JEAM", key="j", on_click=navigate, args=('jean',))
        st.button("👤 THIAGO", key="t", on_click=navigate, args=('thiago',))
        st.button("👤 HEMILLY", key="h", on_click=navigate, args=('hemilly',))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("VOLTAR AO INÍCIO", on_click=navigate, args=('home',))

# PÁGINAS DE DOCUMENTOS
elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    users = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    
    current = st.session_state.page
    st.markdown(f"<h3 class='section-title'>DOCUMENTOS: {names[current]}</h3>", unsafe_allow_html=True)
    
    # --- EXIBIÇÃO DA IMAGEM ---
    # Usamos rotate_degrees=0 e use_container_width=True 
    # para garantir que ela fique deitada conforme o print original.
    imgs = [load_image(f, rotate_degrees=0) for f in users[current]]
    
    if imgs[st.session_state.img_idx]:
        st.image(imgs[st.session_state.img_idx], use_container_width=True)
    else:
        st.error("Erro ao carregar imagem.")

    # --- GRID DE BOTÕES (Lado a Lado no Mobile) ---
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    
    # Linha 1: Navegação de Imagem
    n1, n2 = st.columns(2)
    with n1:
        if st.button("← ANTERIOR"):
            st.session_state.img_idx = (st.session_state.img_idx - 1) % len(imgs); st.rerun()
    with n2:
        if st.button("PRÓXIMO →"):
            st.session_state.img_idx = (st.session_state.img_idx + 1) % len(imgs); st.rerun()

    # Linha 2: Funções do Aluno
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        if st.button("📊 Frequência"): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("📝 Notas"): st.session_state.view = 'n'; st.rerun()

    # Linha 3: Extras e Sair
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    e1, e2 = st.columns(2)
    with e1:
        if st.button("📱 QR CODE"): st.session_state.view = 'q'; st.rerun()
    with e2:
        st.button("🔙 SAIR", on_click=navigate, args=('login',))

    # Área de Exibição de Dados Fictícios
    if st.session_state.view:
        st.divider()
        data = get_student_data()
        if st.session_state.view == 'n':
            st.markdown("#### Histórico de Notas"); st.table(data["Notas"])
        elif st.session_state.view == 'f':
            st.markdown("#### Relatório de Presença"); st.table(data["Frequência"])
        elif st.session_state.view == 'q':
            qr = load_image("qrcode.png")
            if qr: 
                _, qcol, _ = st.columns([1, 1, 1])
                with qcol: st.image(qr, use_container_width=True)
