import streamlit as st
import pandas as pd
import numpy as np
import io

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Mapa de Oportunidades | By Jéssica Sant'Anna",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO RESPONSIVO A TEMA (CLARO E ESCURO) - VERSÃO CORRIGIDA ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap' );

    /* ================================================================
    VARIÁVEIS DE COR (TEMA CLARO COMO PADRÃO)
    ================================================================ */
    :root {
        --font-family: 'Inter', sans-serif;
        --primary-color: #4f46e5;
        --text-color: #111827;
        --text-color-subtle: #6b7280;
        --bg-color: #f9fafb;
        --sidebar-bg: #ffffff;
        --highlight-bg: #eef2ff;
        --border-color: #e5e7eb;
        --button-bg: #4f46e5;
        --button-text: #ffffff;
        --card-bg: #ffffff; /* Fundo do card de curso */
    }

    /* ================================================================
    SOBRESCRITA DAS VARIÁVEIS PARA O TEMA ESCURO
    ================================================================ */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #818cf8;
            --text-color: #e5e7eb;
            --text-color-subtle: #9ca3af;
            --bg-color: #111827;
            --sidebar-bg: #1f2937;
            --highlight-bg: #374151;
            --border-color: #4b5563;
            --button-bg: #818cf8;
            --button-text: #111827;
            --card-bg: #1f2937;
        }
    }

    /* ================================================================
    APLICAÇÃO DAS VARIÁVEIS
    ================================================================ */
    body, .stApp { font-family: var(--font-family); background-color: var(--bg-color); color: var(--text-color); }
    h1, h2, h3, .stMarkdown { color: var(--text-color); }
    [data-testid="stSidebar"] { background-color: var(--sidebar-bg); border-right: 1px solid var(--border-color); }
    .highlight-box { background-color: var(--highlight-bg); border-left: 5px solid var(--primary-color); padding: 25px; border-radius: 10px; margin: 20px 0; }
    .highlight-box h3 { color: var(--primary-color); }
    a { color: var(--primary-color); font-weight: 600; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .footer { text-align: center; padding: 20px; margin-top: 40px; color: var(--text-color-subtle); border-top: 1px solid var(--border-color); }

    /* Botão Principal */
    .stButton > button { background-color: var(--button-bg); color: var(--button-text); border: 1px solid var(--primary-color); border-radius: 0.5rem; font-weight: 600; }
    
    /* Filtros na Barra Lateral */
    [data-testid="stSidebar"] .stMarkdown h3, [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label { color: var(--text-color) !important; }
    [data-testid="stSelectbox"] > div > div { background-color: var(--sidebar-bg); color: var(--text-color); }


    /* --- NOVO ESTILO: CARDS DE CURSO (UX MOBILE) --- */
    .course-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .course-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .course-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: var(--text-color);
    }
    .course-details {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 15px;
        font-size: 0.9rem;
        color: var(--text-color-subtle);
    }
    .course-detail-item {
        display: flex;
        align-items: center;
    }
    .course-detail-icon {
        margin-right: 5px;
    }
    .course-button-container {
        text-align: right;
    }
    .course-button {
        display: inline-block;
        padding: 10px 20px;
        background-color: var(--button-bg);
        color: var(--button-text) !important;
        text-decoration: none;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    .course-button:hover {
        background-color: var(--primary-color);
        opacity: 0.9;
    }

</style>
""", unsafe_allow_html=True)


# --- 3. CARREGAMENTO DOS DADOS ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('cursos_classificados.csv')
        df.rename(columns={'Categoria_NLP': 'Área de Foco'}, inplace=True)
        df['Área de Foco'] = df['Área de Foco'].fillna('Outras')
        df['Duracao'] = df['Duracao'].fillna('Não Informada')
        return df
    except FileNotFoundError:
        st.error("Arquivo 'cursos_classificados.csv' não encontrado. Verifique o caminho.")
        return pd.DataFrame()

df = load_data()

# --- 4. TELA DE BOAS-VINDAS ---
if "show_main_page" not in st.session_state:
    st.session_state.show_main_page = False

if not st.session_state.show_main_page:
    welcome_image_url = "https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(welcome_image_url, use_column_width=True)
    with col2:
        st.title("O Futuro da sua Carreira Começa Agora.")
        st.markdown("#### Uma plataforma inteligente que mapeia os melhores cursos gratuitos para você.")
        st.write("")
        if st.button("🚀 Começar a Explorar"):
            st.session_state.show_main_page = True
            st.rerun()
    st.stop()

# --- 5. PÁGINA PRINCIPAL ---
st.sidebar.title("🛠️ Filtros Inteligentes")

# VARIÁVEIS DE ESTADO PARA OS FILTROS
if 'selected_categoria' not in st.session_state:
    st.session_state.selected_categoria = 'Todas'
if 'selected_fonte' not in st.session_state:
    st.session_state.selected_fonte = 'Todas'

if not df.empty:
    # FORMULÁRIO DE FILTROS NA SIDEBAR
    with st.sidebar.form(key='filters_form'):
        categorias = ['Todas'] + sorted(df['Área de Foco'].unique())
        st.markdown("### 🧠 Por Área de Foco")
        # Usa selectbox para ocupar menos espaço
        categoria_input = st.selectbox("Selecione a área de interesse:", categorias, index=categorias.index(st.session_state.selected_categoria), label_visibility="collapsed")

        fontes = ['Todas'] + sorted(df['Fonte'].unique())
        st.markdown("### 🏫 Por Instituição")
        fonte_input = st.selectbox("Selecione a instituição:", fontes, index=fontes.index(st.session_state.selected_fonte), label_visibility="collapsed")
        
        st.write("") # Espaçamento
        # Botão de Aplicar
        submit_button = st.form_submit_button(label='Aplicar Filtros 🔍')

    # ATUALIZA O ESTADO SE O BOTÃO FOR CLICADO
    if submit_button:
        st.session_state.selected_categoria = categoria_input
        st.session_state.selected_fonte = fonte_input

    # APLICA OS FILTROS COM BASE NO ESTADO
    df_filtered = df.copy()
    if st.session_state.selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Área de Foco'] == st.session_state.selected_categoria]
    if st.session_state.selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == st.session_state.selected_fonte]

    df_filtered = df_filtered.sort_values(by='Titulo')

    st.title("🎯 Encontre seu curso on-line e gratuito")
    st.markdown(f"### {len(df_filtered)} cursos encontrados para você.")
    st.markdown("""
    <div class="highlight-box">
        <h3>✨ Qualificação ao seu Alcance</h3>
        <p>Navegue por cursos de instituições como <b>FGV, Bradesco e Coursera</b>. Nossa IA organiza tudo para que você encontre a habilidade certa para se destacar.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- EXIBIÇÃO EM CARDS (UX MOBILE OTIMIZADA) ---
    # Itera sobre cada curso filtrado e cria um card HTML
    for index, row in df_filtered.iterrows():
        link = row['Link'] if pd.notna(row['Link']) else '#'
        card_html = f"""
        <div class="course-card">
            <div class="course-title">{row['Titulo']}</div>
            <div class="course-details">
                <div class="course-detail-item">
                    <span class="course-detail-icon">🧠</span> {row['Área de Foco']}
                </div>
                <div class="course-detail-item">
                    <span class="course-detail-icon">🏫</span> {row['Fonte']}
                </div>
                <div class="course-detail-item">
                    <span class="course-detail-icon">⏳</span> {row['Duracao']}
                </div>
            </div>
            <div class="course-button-container">
                <a href="{link}" target="_blank" class="course-button">Acessar Curso ➔</a>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

else:
    st.warning("Aguardando carregamento dos dados...")

# --- 6. RODAPÉ ---
st.markdown("""
<div class="footer">
    Criado por Jéssica Mendes Pereira Sant'Anna
</div>
""", unsafe_allow_html=True)