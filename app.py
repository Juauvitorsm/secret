import streamlit as st
from PIL import Image

# Carregue as imagens
try:
    image_1 = Image.open("1.png")
    image_2 = Image.open("2.png")
except FileNotFoundError:
    st.error("Certifique-se de que os arquivos '1.png' e '2.png' estão no mesmo diretório do seu script.")
    st.stop()

# --- Estrutura do App Streamlit ---


# Exibe a primeira imagem
st.image(image_1)

# Adiciona um espaço para separar as imagens
st.markdown("---")

# Exibe a segunda imagem
st.image(image_2)