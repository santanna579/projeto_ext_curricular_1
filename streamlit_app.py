import streamlit as st
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==============================
# CONFIGURAÇÃO GERAL DO APP
# ==============================
st.set_page_config(page_title="Escola Virtual - Fundação Bradesco", page_icon="🎓", layout="wide")

# CSS Customizado para UI + Responsividade
st.markdown("""
    <style>
    /* Estilo geral */
    body, .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Cabeçalho */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #003366;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* Subtítulo */
    .subheader {
        text-align: center;
        font-size: 1.1rem;
        color: #444;
        margin-bottom: 2rem;
    }

    /* Card do curso */
    .course-card {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        padding: 1.5rem;
        transition: all 0.3s ease;
        text-align: center;
        border: 1px solid #eee;
    }

    .course-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }

    .course-title {
        color: #003366;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .course-info {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.3rem;
    }

    .course-link a {
        text-decoration: none;
        color: white;
        background-color: #0066cc;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: background-color 0.2s ease;
    }

    .course-link a:hover {
        background-color: #004d99;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .course-card {
            padding: 1rem;
        }
        .course-title {
            font-size: 1rem;
        }
        .course-info {
            font-size: 0.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# FUNÇÃO DE RASPAGEM
# ==============================
@st.cache_data(show_spinner=False)
def coletar_cursos():
    url = "https://www.ev.org.br/cursos"

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # Rola até o fim da página para carregar todos os cursos
    ultima_altura = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        nova_altura = driver.execute_script("return document.body.scrollHeight")
        if nova_altura == ultima_altura:
            break
        ultima_altura = nova_altura

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("a", class_="m-card")
    lista_cursos = []

    for card in cards:
        try:
            titulo_tag = card.find("h3", class_="m-card_title")
            titulo = titulo_tag.get_text(strip=True) if titulo_tag else "N/A"

            duracao_tag = card.find("p", class_="m-info_desc -small m-card_info", string=re.compile("Duração"))
            duracao = duracao_tag.find("strong").get_text(strip=True) if duracao_tag and duracao_tag.find("strong") else "N/A"

            nivel_tag = card.find("p", class_="m-info_desc -small m-card_info", string=re.compile("Nível"))
            nivel = nivel_tag.find("strong").get_text(strip=True) if nivel_tag and nivel_tag.find("strong") else "N/A"

            link = "https://www.ev.org.br" + card["href"] if card.get("href") else "N/A"

            lista_cursos.append({
                "Titulo": titulo,
                "Duracao": duracao,
                "Nivel": nivel,
                "Link": link
            })
        except Exception:
            continue

    return pd.DataFrame(lista_cursos)

# ==============================
# INTERFACE PRINCIPAL
# ==============================
st.markdown("<h1 class='main-header'>🎓 Escola Virtual Fundação Bradesco</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Explore cursos gratuitos e desenvolva novas habilidades profissionais.</p>", unsafe_allow_html=True)

if st.button("🔍 Carregar Cursos", use_container_width=True):
    with st.spinner("Buscando cursos... isso pode levar alguns segundos ⏳"):
        df = coletar_cursos()

    if df.empty:
        st.warning("⚠️ Nenhum curso encontrado.")
    else:
        # Layout adaptável: 3 colunas no desktop, 1 no mobile
        cols = st.columns(3) if st.session_state.get("wide_mode", True) else st.columns(1)
        for i, (_, curso) in enumerate(df.iterrows()):
            col = cols[i % len(cols)]
            with col:
                st.markdown(f"""
                    <div class="course-card">
                        <div class="course-title">{curso['Titulo']}</div>
                        <div class="course-info"><b>Duração:</b> {curso['Duracao']}</div>
                        <div class="course-info"><b>Nível:</b> {curso['Nivel']}</div>
                        <div class="course-link"><a href="{curso['Link']}" target="_blank">Acessar Curso</a></div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("👆 Clique em **'Carregar Cursos'** para iniciar a busca.")

