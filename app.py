import streamlit as st
from PIL import Image

# Configuração da página para ocupar a largura total
st.set_page_config(layout="wide")

# Carregue as imagens
try:
    image_1 = Image.open("1.png")
    image_2 = Image.open("2.png")
except FileNotFoundError:
    st.error("Certifique-se de que os arquivos '1.png' e '2.png' estão no mesmo diretório do seu script.")
    st.stop()

# --- Rotacione as imagens em 90 graus usando PIL ---
rotated_image_1 = image_1.rotate(90, expand=True)
rotated_image_2 = image_2.rotate(90, expand=True)

# --- Estilos CSS ---
st.markdown("""
<style>
/* Importa uma fonte moderna do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

/* Estilo para a barra divisória personalizada */
.color-divider {
    border-bottom: 2px solid #1a237e;
    margin-top: 2rem;
    margin-bottom: 2rem;
}

/* Estilo para o novo bloco do título */
.header-container {
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    color: #1a237e;
    font-size: 2.5em;
    font-weight: 700;
    margin-bottom: 2rem;
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
    width: 100vw; /* Faz cada imagem ocupar a largura total da tela */
    scroll-snap-align: center;
}

/* Ajustes para o container Streamlit principal (garante a rolagem sem quebrar o layout) */
.st-emotion-cache-1ky2q5g {
    overflow-x: hidden !important;
}

/* Remove a largura máxima do main content para que o layout se expanda */
.st-emotion-cache-1ky2q5g {
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
# Este contêiner envolve as imagens para que a rolagem funcione
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

# Insere a primeira imagem rotacionada
st.image(rotated_image_1, use_container_width=True)

# Insere a segunda imagem rotacionada
st.image(rotated_image_2, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Adiciona o link da faculdade
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>Volta para a home da faculdade Socrates</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><a href='https://www.socrates.com.br/' target='_blank'>www.socrates.com.br</a></p>", unsafe_allow_html=True)