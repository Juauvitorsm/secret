import streamlit as st
from PIL import Image

# Configuração da página
st.set_page_config(layout="wide")

# Inicializa o estado da sessão para a imagem atual e o QR Code
if 'current_image_index' not in st.session_state:
    st.session_state.current_image_index = 0
if 'show_qrcode' not in st.session_state:
    st.session_state.show_qrcode = False

# Carrega e rotaciona as imagens
try:
    images = [
        Image.open("1.png").rotate(90, expand=True),
        Image.open("2.png").rotate(90, expand=True)
    ]
    qrcode_image = Image.open("qrcode.png")
except FileNotFoundError:
    st.error("Certifique-se de que os arquivos de imagem estão no mesmo diretório do seu script.")
    st.stop()

# --- Estilos CSS ---
st.markdown("""
<style>
/* ... (Seus estilos CSS anteriores, incluindo cores, fontes, etc.) ... */

/* Estilo para a barra divisória personalizada */
.color-divider {
    border-bottom: 2px solid #1a237e;
    margin-top: 2rem;
    margin-bottom: 2rem;
}

/* Barra estilizada extra */
.styled-bar {
    margin: 2rem 0;
    height: 6px;
    border-radius: 8px;
    background: linear-gradient(90deg, #1a237e, #3949ab, #5c6bc0);
    box-shadow: 0 3px 6px rgba(0,0,0,0.2);
}

/* Estilo para o novo bloco do título e dos novos textos */
.header-container {
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    color: #1a237e;
    font-size: 2.5em;
    font-weight: 700;
    margin-bottom: 2rem;
}

/* Estilo para a nova fonte do texto do link */
.link-text {
    font-family: 'Montserrat', sans-serif;
    font-weight: 400;
    text-align: center;
    color: #333333;
}

/* Estilo para os botões */
.stButton button {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.8em;
    font-weight: 700;
    color: #1a237e !important;
    background-color: #f0f8ff;
    border: 2px solid #1a237e;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 1rem;
    margin-bottom: 1rem;
    transition: 0.3s;
}
.stButton button:hover {
    background-color: #e6eef5;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

/* Contêiner para a imagem atual */
.image-container {
    border: 5px solid #EFEFEF;
    border-radius: 10px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    padding: 5px;
    text-align: center;
    margin-bottom: 20px;
}
.image-container img {
    max-width: 100%;
    height: auto;
}

/* Estilo específico para a imagem do QR Code */
.stImage img[src*="data:image/png;base64"] {
    border: 3px solid #EFEFEF;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 3px;
}
</style>
""", unsafe_allow_html=True)

# --- Funções para Navegação ---
def next_image():
    """Avança para a próxima imagem, voltando para o início se necessário."""
    st.session_state.current_image_index = (st.session_state.current_image_index + 1) % len(images)

def prev_image():
    """Volta para a imagem anterior, indo para o final se necessário."""
    st.session_state.current_image_index = (st.session_state.current_image_index - 1 + len(images)) % len(images)

# --- Estrutura do App Streamlit ---
st.markdown('<div class="color-divider"></div>', unsafe_allow_html=True)

# Título centralizado
st.markdown('<div class="header-container">DOCUMENTO DIGITAL</div>', unsafe_allow_html=True)

# Contêiner para a imagem
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image(images[st.session_state.current_image_index], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Controles de navegação
col_prev, col_spacer, col_next = st.columns([1, 4, 1])

with col_prev:
    st.button("◀️ Anterior", on_click=prev_image, use_container_width=True)
with col_next:
    st.button("Próximo ▶️", on_click=next_image, use_container_width=True)

# Barra estilizada
st.markdown('<div class="styled-bar"></div>', unsafe_allow_html=True)

# Botões de funcionalidade
col_freq, col_notas, col_qrcode = st.columns(3)

with col_freq:
    if st.button("Frequência", use_container_width=True):
        st.write("Frequência: Funcionalidade a ser adicionada.")
with col_notas:
    if st.button("Notas", use_container_width=True):
        st.write("Notas: Funcionalidade a ser adicionada.")
with col_qrcode:
    if st.button("QR Code", use_container_width=True):
        st.session_state.show_qrcode = not st.session_state.show_qrcode

if st.session_state.show_qrcode:
    col_qr_left, col_qr_center, col_qr_right = st.columns([1, 0.5, 1])
    with col_qr_center:
        st.image(qrcode_image, use_container_width=True, caption="QR Code", width=200)

st.markdown('<div class="styled-bar"></div>', unsafe_allow_html=True)

st.markdown("<p class='link-text'>Volta para a home da faculdade Socrates</p>", unsafe_allow_html=True)

col_button = st.columns([1, 0.5, 1])[1]
with col_button:
    st.link_button("www.socrates.com.br", url="https://www.socrates.com.br/", use_container_width=True)