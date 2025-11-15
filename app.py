import streamlit as st
from PIL import Image
from io import BytesIO  # <-- ADICIONADO AQUI
import base64           # <-- ADICIONADO AQUI

# Configuração da página (deve ser a primeira cois do Streamlit)
st.set_page_config(layout="wide")

# --- Função de Cache para Imagens ---
@st.cache_data
def load_image(image_path, rotate_degrees=0):
    """
    Carrega uma imagem do disco, aplica rotação (se necessário) e a mantém em cache.
    Retorna o objeto de imagem PIL ou None se o arquivo não for encontrado.
    """
    try:
        image = Image.open(image_path)
        if rotate_degrees != 0:
            return image.rotate(rotate_degrees, expand=True)
        return image
    except FileNotFoundError:
        st.error(f"Erro: Arquivo de imagem não encontrado em: {image_path}")
        return None

# --- Função auxiliar para converter imagem (MOVIDA PARA CIMA) ---
def image_to_base64(image):
    """Converte um objeto de imagem PIL para string base64."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# --- Estilos CSS Corporativos (Injetados apenas uma vez) ---
st.markdown("""
<style>
/* ... (Todo o seu CSS continua o mesmo, omitido aqui para ser breve) ... */
/* Corpo da página */
body {
    font-family: 'Montserrat', sans-serif;
    background-color: #f4f6f9;
}

/* Logo centralizado */
.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 3rem;
    margin-bottom: 2rem;
}
.logo-image {
    max-width: 60%;
    height: auto;
    border-radius: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}
.logo-image:hover {
    transform: scale(1.05);
}

/* Cabeçalhos */
.header-container {
    text-align: center;
    color: #1a237e;
    font-size: 2.4em;
    font-weight: 800;
    margin-bottom: 1.5rem;
}

/* Divisores e barras estilizadas */
.color-divider {
    border-bottom: 2px solid #5c6bc0;
    margin: 2rem 0;
}
.styled-bar {
    margin: 2rem 0;
    height: 8px;
    border-radius: 12px;
    background: linear-gradient(90deg, #1a237e, #3949ab, #5c6bc0);
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

/* Botões modernos */
.stButton button {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.1em;
    font-weight: 600;
    color: #1a237e !important;
    background-color: #e6eef5;
    border: 2px solid #5c6bc0;
    border-radius: 35px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    padding: 0.8rem 2.5rem;
    transition: all 0.3s ease;
}
.stButton button:hover {
    background-color: #5c6bc0;
    color: #fff !important;
    border-color: #5c6bc0;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    transform: translateY(-2px);
}

/* Cartões de imagem */
.image-container {
    border-radius: 20px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    padding: 15px;
    background: #ffffff;
    margin-bottom: 25px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.image-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 35px rgba(0,0,0,0.25);
}

/* Texto de links */
.link-text {
    font-weight: 400;
    text-align: center;
    color: #333333;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Inicialização do estado da sessão ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
    st.session_state.current_image_index = 0
    st.session_state.show_qrcode = False

# --- Funções de Navegação ---
def go_to_login_page():
    st.session_state.page = 'login'

def go_to_jeam_page():
    st.session_state.page = 'jeam'
    st.session_state.current_image_index = 0
    st.session_state.show_qrcode = False

def go_to_hayane_page():
    st.session_state.page = 'hayane'
    st.session_state.current_image_index = 0
    st.session_state.show_qrcode = False

def go_to_gustavo_page():
    st.session_state.page = 'gustavo'
    st.session_state.current_image_index = 0
    st.session_state.show_qrcode = False

def go_to_home_page():
    st.session_state.page = 'home'

# --- Função genérica para exibir o conteúdo do documento ---
def digital_document_page(title, image_files):
    
    # Carrega imagens usando a função cacheada
    images = [load_image(f, rotate_degrees=90) for f in image_files]
    qrcode_image = load_image("qrcode.png")

    # Verifica se alguma imagem falhou ao carregar
    if any(img is None for img in images) or qrcode_image is None:
        st.error("Uma ou mais imagens não puderam ser carregadas. Verifique os nomes e caminhos dos arquivos.")
        st.button("Voltar", on_click=go_to_login_page)
        st.stop() 

    def next_image():
        st.session_state.current_image_index = (st.session_state.current_image_index + 1) % len(images)

    def prev_image():
        st.session_state.current_image_index = (st.session_state.current_image_index - 1 + len(images)) % len(images)

    st.markdown('<div class="color-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="header-container">{title}</div>', unsafe_allow_html=True)

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(images[st.session_state.current_image_index], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_prev, col_spacer, col_next = st.columns([1, 4, 1])
    with col_prev:
        st.button("Anterior", on_click=prev_image, use_container_width=True)
    with col_next:
        st.button("Próximo", on_click=next_image, use_container_width=True)

    st.markdown('<div class="styled-bar"></div>', unsafe_allow_html=True)

    col_freq, col_notas, col_qrcode = st.columns(3)
    with col_freq:
        st.button("Frequência", use_container_width=True)
    with col_notas:
        st.button("Notas", use_container_width=True)
    with col_qrcode:
        if st.button("QR Code", use_container_width=True):
            st.session_state.show_qrcode = not st.session_state.show_qrcode

    if st.session_state.show_qrcode:
        col_qr_left, col_qr_center, col_qr_right = st.columns([1, 0.5, 1])
        with col_qr_center:
            st.image(qrcode_image, use_container_width=True, caption="QR Code", width=200)

    st.markdown('<div class="styled-bar"></div>', unsafe_allow_html=True)
    st.button("Voltar", on_click=go_to_login_page)

# --- Página Inicial ---
if st.session_state.page == 'home':
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    logo = load_image("logo.png")
    if logo:
        # Adicionando a classe CSS para o efeito de hover
        # Agora a função image_to_base64() é definida ANTES daqui
        st.markdown(
            f'<img src="data:image/png;base64,{image_to_base64(logo)}" class="logo-image">', 
            unsafe_allow_html=True
        )
    else:
        st.error("Certifique-se de que o arquivo 'logo.png' está no mesmo diretório do seu script.")
        st.stop()
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col2:
        st.button("Entrar", on_click=go_to_login_page)

# --- Página de Login ---
elif st.session_state.page == 'login':
    st.markdown('<div class="header-container">Quem é você?</div>', unsafe_allow_html=True)

    col_jeam, col_hayane, col_gustavo = st.columns(3) 
    
    with col_jeam:
        st.button("Jeam", on_click=go_to_jeam_page, use_container_width=True)
    with col_hayane:
        st.button("Hayane", on_click=go_to_hayane_page, use_container_width=True)
    with col_gustavo:
        st.button("Gustavo", on_click=go_to_gustavo_page, use_container_width=True)

    st.markdown('<div class="styled-bar"></div>', unsafe_allow_html=True)
    st.button("Voltar", on_click=go_to_home_page)

# --- Conteúdo de Jeam ---
elif st.session_state.page == 'jeam':
    digital_document_page("DOCUMENTO DIGITAL", ["1.png", "2.png"])

# --- Conteúdo de Hayane ---
elif st.session_state.page == 'hayane':
    digital_document_page("DOCUMENTO DIGITAL", ["3.png", "4.png"])

# --- Conteúdo de Gustavo ---
elif st.session_state.page == 'gustavo':
    digital_document_page("DOCUMENTO DIGITAL", ["5.png", "6.png"])

# --- A FUNÇÃO AUXILIAR FOI REMOVIDA DAQUI ---