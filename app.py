import streamlit as st
from PIL import Image

# Configuração da página para ocupar a largura total
st.set_page_config(layout="wide")

# Inicialize o estado da sessão para controlar a exibição da imagem
if 'show_qrcode' not in st.session_state:
    st.session_state.show_qrcode = False

# Carregue as imagens
try:
    image_1 = Image.open("1.png")
    image_2 = Image.open("2.png")
    qrcode_image = Image.open("qrcode.png")
except FileNotFoundError:
    st.error("Certifique-se de que os arquivos de imagem estão no mesmo diretório do seu script.")
    st.stop()

# --- Rotacione as imagens em 90 graus usando PIL ---
rotated_image_1 = image_1.rotate(90, expand=True)
rotated_image_2 = image_2.rotate(90, expand=True)

# --- Estilos CSS ---
st.markdown("""
<style>
/* Importa uma fonte moderna do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

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
    background-color: #f0f8ff; /* Fundo mais claro */
    border: 2px solid #1a237e; /* Borda para destacar */
    border-radius: 10px; /* Borda arredondada */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Sombra suave */
    padding: 1rem;
    margin-bottom: 1rem;
    transition: 0.3s; /* Transição suave para o efeito de hover */
}
.stButton button:hover {
    background-color: #e6eef5; /* Fundo mais escuro ao passar o mouse */
    box-shadow: 0 6px 12px rgba(0,0,0,0.15); /* Sombra mais forte */
}

/* Contêiner principal para a rolagem horizontal */
.scroll-container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    gap: 10px;
    padding-bottom: 20px; /* Adiciona padding para evitar que a sombra seja cortada */
}

/* Oculta a barra de rolagem padrão (opcional) */
.scroll-container::-webkit-scrollbar {
    display: none;
}
.scroll-container {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

/* Estilos para cada imagem dentro do contêiner COM MOLDURA */
.scroll-container .stImage img {
    flex-shrink: 0;
    width: 100vw;
    scroll-snap-align: center;
    border: 5px solid #EFEFEF; /* MOLDURA */
    border-radius: 10px; /* Cantos arredondados */
    box-shadow: 0 8px 16px rgba(0,0,0,0.2); /* Sombra */
    padding: 5px; /* Espaçamento interno */
}

/* Estilo específico para a imagem do QR Code */
.stImage img[src*="data:image/png;base64"] {
    border: 3px solid #EFEFEF;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 3px;
}

/* Ajustes para o container Streamlit principal */
.st-emotion-cache-1ky2q5g {
    overflow-x: hidden !important;
    max-width: none !important;
}

h1, h4, p {
    transform: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- Estrutura do App Streamlit ---

# Adiciona a linha divisória com cor personalizada
st.markdown('<div class="color-divider"></div>', unsafe_allow_html=True)

# Título centralizado
st.markdown('<div class="header-container">DOCUMENTO DIGITAL</div>', unsafe_allow_html=True)

# Carrossel (rolagem horizontal)
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
st.image(rotated_image_1, use_container_width=True)
st.image(rotated_image_2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Barra estilizada separando do resto
st.markdown('<div class="styled-bar"></div>', unsafe_allow_html=True)

# Linha de colunas para os botões
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

# Condicionalmente exibe a imagem do QR Code
if st.session_state.show_qrcode:
    col_qr_left, col_qr_center, col_qr_right = st.columns([1, 0.5, 1])
    with col_qr_center:
        st.image(qrcode_image, use_container_width=True, caption="QR Code", width=200)

# Barra estilizada separando QR Code do rodapé
st.markdown('<div class="styled-bar"></div>', unsafe_allow_html=True)

# Texto e link da faculdade
st.markdown("<p class='link-text'>Volta para a home da faculdade Socrates</p>", unsafe_allow_html=True)

# Centraliza o botão
col_button = st.columns([1, 0.5, 1])[1]
with col_button:
    st.link_button("www.socrates.com.br", url="https://www.socrates.com.br/", use_container_width=True)
