import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# 1. Configuração da página
st.set_page_config(
    page_title="Identificação Digital Académica",
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
            "Disciplina": ["Anatomia Humana", "Fisiologia do Exercício", "Cinesiologia", "Psicologia do Esporte"],
            "Nota": [9.2, 8.5, 7.9, 9.8],
            "Situação": ["Aprovado", "Aprovado", "Aprovado", "Aprovado"]
        }),
        "Frequência": pd.DataFrame({
            "Atividade": ["Práticas Corporais", "Atletismo", "Natação", "Ginástica Geral"],
            "Presença": ["100%", "92%", "88%", "95%"],
            "Faltas": [0, 2, 3, 1]
        })
    }

# --- CSS: DESIGN TOTAL E TELA CHEIA ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Remove margens do Streamlit */
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }

    /* Estilo do Título Superior */
    .header-identificacao {
        text-align: center;
        padding: 15px;
        background: white;
        color: #1a237e;
        font-weight: 700;
        text-transform: uppercase;
        border-bottom: 4px solid #1a237e;
    }

    /* Card de Validade com Cor Ajustada */
    .validade-card {
        background: linear-gradient(135deg, #0044cc 0%, #007bff 100%);
        color: white;
        padding: 20px;
        width: 100vw;
    }
    .val-box {
        background: white;
        color: #0044cc;
        padding: 8px 15px;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
        font-weight: 800;
    }

    /* Cards de Seleção de Aluno */
    .student-card {
        background: white;
        padding: 15px;
        margin: 5px 10px;
        border: 1px solid #ddd;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .avatar-circle {
        width: 40px; height: 40px;
        background: #1a237e;
        color: white;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700;
    }

    /* Botões de Função colados */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 2px !important;
        width: 100vw !important;
    }
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        height: 55px !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        background: white;
        border: 1px solid #eee;
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

# --- Fluxo de Telas ---

if st.session_state.page == 'home':
    st.markdown('<div style="height: 20vh;"></div>', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{image_to_base64(logo)}" style="max-width:220px;"></div>', unsafe_allow_html=True)
    st.button("ENTRAR NO PORTAL ACADÉMICO", on_click=navigate, args=('login',))

elif st.session_state.page == 'login':
    st.markdown('<div class="header-identificacao">Selecione o Estudante</div>', unsafe_allow_html=True)
    for key, name, initial in [("jean", "JEAM", "J"), ("thiago", "THIAGO", "T"), ("hemilly", "HEMILLY", "H")]:
        st.markdown(f'<div class="student-card"><div class="avatar-circle">{initial}</div><b>ALUNO: {name}</b></div>', unsafe_allow_html=True)
        if st.button(f"ACESSAR IDENTIFICAÇÃO - {name}", key=f"btn_{key}"): 
            navigate(key)
            st.rerun()

elif st.session_state.page in ['jean', 'thiago', 'hemilly']:
    names = {"jean": "JEAM", "thiago": "THIAGO", "hemilly": "HEMILLY"}
    files = {"jean": ["1.png", "2.png"], "thiago": ["3.png", "4.png"], "hemilly": ["5.png", "6.png"]}
    current = st.session_state.page
    
    st.markdown(f'<div class="header-identificacao">Identificação: {names[current]}</div>', unsafe_allow_html=True)
    
    # Troca por Abas (Simula Swipe)
    t1, t2 = st.tabs(["FRENTE DO DOCUMENTO", "VERSO DO DOCUMENTO"])
    imgs = [load_image(f, rotate_degrees=90) for f in files[current]]
    
    with t1:
        if imgs[0]: st.image(imgs[0], use_container_width=True)
    with t2:
        if len(imgs) > 1: st.image(imgs[1], use_container_width=True)

    # Card de Validade
    st.markdown("""
        <div class="validade-card">
            <span style="font-size:0.8rem; opacity:0.8;">Data da Matrícula: 01/03/2019</span><br>
            <div class="val-box">VALIDADE: 30/06/2026</div>
        </div>
    """, unsafe_allow_html=True)

    # Botões
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        if st.button("FREQ."): st.session_state.view = 'f'; st.rerun()
    with f2:
        if st.button("NOTAS"): st.session_state.view = 'n'; st.rerun()
    with f3:
        if st.button("QR"): st.session_state.view = 'q'; st.rerun()
    with f4:
        if st.button("SAIR"): navigate('login'); st.rerun()

    # Dados Fictícios de Educação Física
    if st.session_state.view:
        data = get_student_data()
        st.markdown("<div style='padding:15px;'>", unsafe_allow_html=True)
        if st.session_state.view == 'f':
            st.write("**Relatório de Frequência:**")
            st.table(data["Frequência"])
        elif st.session_state.view == 'n':
            st.write("**Boletim Académico:**")
            st.table(data["Notas"])
        elif st.session_state.view == 'q':
            qr = load_image("qrcode.png")
            if qr: st.image(qr, width=200)
        st.markdown("</div>", unsafe_allow_html=True)
