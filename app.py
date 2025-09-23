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
}

/* Oculta a barra de rolagem padrão (opcional) */
.scroll-container::-webkit-scrollbar {
    display: none;
}
.scroll-container {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

/* Estilos para cada imagem dentro do contêiner */
.scroll-container .stImage {
    flex-shrink: 0;
    width: 100vw;
    scroll-snap-align: center;
}

/* Ajustes para o container Streamlit principal (garante a rolagem sem quebrar o layout) */
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

# Título centralizado no novo estilo
st.markdown('<div class="header-container">DOCUMENTO DIGITAL</div>', unsafe_allow_html=True)

# Usa o contêiner de rolagem horizontal
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
st.image(rotated_image_1, use_container_width=True)
st.image(rotated_image_2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Adiciona uma linha de colunas para os botões
st.markdown("<p style='text-align: center;'>---</p>", unsafe_allow_html=True)
col_freq, col_notas, col_qrcode = st.columns(3)

with col_freq:
    if st.button("Frequência", use_container_width=True):
        st.write("Frequência: Funcionalidade a ser adicionada.")
with col_notas:
    if st.button("Notas", use_container_width=True):
        st.write("Notas: Funcionalidade a ser adicionada.")
with col_qrcode:
    if st.button("QR Code", use_container_width=True):
        # Inverte o estado para mostrar/ocultar a imagem
        st.session_state.show_qrcode = not st.session_state.show_qrcode

# Condicionalmente exibe a imagem do QR Code
if st.session_state.show_qrcode:
    st.image(qrcode_image, use_container_width=False, width=300)

# Adiciona o texto e o link da faculdade
st.markdown("---")
st.markdown("<p class='link-text'>Volta para a home da Faculdade Socrates</p>", unsafe_allow_html=True)

# Centraliza o botão
col_button = st.columns([1, 0.5, 1])[1]
with col_button:
    st.link_button("www.socrates.com.br", url="https://www.socrates.com.br/", use_container_width=True)