import streamlit as st
from PIL import Image

# Carregue as imagens
try:
    foto_perfil = Image.open("foto.jpeg") 
    logo = Image.open("logo.png")
    qrcode = Image.open("qrcode.png")
except FileNotFoundError:
    st.error("Certifique-se de que os arquivos 'foto.jpeg', 'logo.png' e 'qrcode.png' estão no mesmo diretório do seu script.")
    st.stop()

# --- Estilos CSS personalizados para replicar o layout ---
st.markdown("""
<style>
/* Estilos para o fundo da página Streamlit (cor azul claro) */
body {
    background-color: #ADD8E6; 
}
/* Altera o fundo do main content do Streamlit */
.st-emotion-cache-1ky2q5g {
    background-color: #ADD8E6; 
    padding: 30px;
    border-radius: 25px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    max-width: 600px;
}
/* Outros containers Streamlit que podem ter fundo branco padrão */
.st-emotion-cache-z5fcl4 {
    background-color: #ADD8E6; 
}
/* Estilos para a "carteira" interna */
.card-container {
    background-color: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
}

/* Estilos para a foto de perfil */
.st-emotion-cache-1f8797p img {
    border-radius: 50%;
    border: 3px solid #eee;
    width: 100px;
    height: 100px;
    object-fit: cover;
}

/* Estilos para o texto do nome e graduação */
.name-text h4 {
    margin: 0;
    font-size: 1.4rem;
    font-weight: bold;
    color: #333;
}
.name-text p {
    margin: 5px 0 0;
    font-size: 1rem;
    color: #555;
}

/* Estilos para os detalhes (matrícula, cpf, etc.) */
.detail-text {
    color: #1a237e; /* Ajustado para um azul mais escuro, já que o fundo é claro */
    font-weight: bold;
    margin-bottom: 10px;
    font-size: 1.1rem;
}

/* Estilos para o contêiner de validade e idade */
.validity-box {
    background-color: white;
    padding: 10px 15px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 0 auto;
    max-width: 120px;
}
.validity-box p {
    margin: 0;
    font-size: 0.8rem;
    color: #888;
}
.validity-box h5 {
    margin: 5px 0 0;
    font-size: 1.1rem;
    color: #333;
}

/* Estilos para o QR Code */
.qr-code-box {
    background-color: white;
    width: 80px;
    height: 80px;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Estilos para o logo no topo */
.logo-container {
    text-align: center;
    margin-bottom: 30px;
    padding-top: 20px;
}
.logo-container img {
    max-width: 150px;
    height: auto;
}

/* Centralizar o título */
.st-emotion-cache-h4xjof {
    text-align: center;
    color: #1a237e; /* Ajustado para um azul mais escuro, já que o fundo é claro */
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# --- Estrutura do App Streamlit ---
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Contêiner para o documento completo (fundo azul)
with st.container():
    # Espaço para o logotipo
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    st.image(logo, width=150)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Título do App (barra superior)
    st.markdown("<h2 style='text-align: center; color: #1a237e; margin-top: 0;'>ID DIGITAL</h2>", unsafe_allow_html=True)
    
    # Contêiner para a seção principal com a foto
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        st.markdown('<div>', unsafe_allow_html=True)
        st.image(foto_perfil, width=100)
        st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<div class='name-text'><h4>Jean Francisco da Silva</h4><p>GRADUAÇÃO EM DIREITO</p></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Seção de detalhes
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<p class='detail-text'>Matrícula: 50395-9</p>", unsafe_allow_html=True)
    st.markdown("<p class='detail-text'>CPF: 702.059.836-69</p>", unsafe_allow_html=True)
    st.markdown("<p class='detail-text'>Data de Nascimento: 22/06/2001</p>", unsafe_allow_html=True)
    st.markdown("<p class='detail-text'>Filiação: Nome da mãe: Fabiana Maria</p>", unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # Seção de validade e QR Code e Idade
    col_validade, col_qr, col_idade = st.columns([1, 1, 1])
    
    with col_validade:
        st.markdown("<div class='validity-box'><p>Validade:</p><h5>22/06/2026</h5></div>", unsafe_allow_html=True)
    
    with col_qr:
        st.image(qrcode, width=80) 
    
    with col_idade:
        st.markdown("<div class='validity-box'><p>Idade:</p><h5>24</h5></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)