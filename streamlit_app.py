import streamlit as st
import pandas as pd

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Mapa de Oportunidades | By Jéssica Sant'Anna",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO RESPONSIVO A TEMA (CLARO E ESCURO) ---
st.markdown("""
<style>
    /* Importa a fonte do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap' );

    /* 
    ================================================================
    DEFINIÇÃO DAS VARIÁVEIS DE COR (TEMA CLARO COMO PADRÃO)
    ================================================================
    */
    :root {
        --font-family: 'Inter', sans-serif;
        
        /* Tema Claro */
        --primary-color: #4f46e5;       /* Roxo/Índigo vibrante */
        --text-color: #111827;          /* Cinza bem escuro para texto */
        --bg-color: #f9fafb;            /* Fundo principal (cinza muito claro) */
        --sidebar-bg: #ffffff;          /* Fundo da sidebar (branco) */
        --highlight-bg: #eef2ff;        /* Fundo da caixa de destaque */
        --table-header-bg: #4f46e5;     /* Fundo do cabeçalho da tabela */
        --table-header-text: #ffffff;   /* Texto do cabeçalho da tabela */
        --table-row-even-bg: #f3f4f6;   /* Fundo da linha par da tabela */
        --border-color: #e5e7eb;        /* Cor da borda */
    }

    /* 
    ================================================================
    SOBRESCRITA DAS VARIÁVEIS PARA O TEMA ESCURO
    ================================================================
    */
    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #818cf8;       /* Roxo/Índigo mais claro para contraste */
            --text-color: #e5e7eb;          /* Cinza claro para texto */
            --bg-color: #111827;            /* Fundo principal (cinza-azulado escuro) */
            --sidebar-bg: #1f2937;          /* Fundo da sidebar (um tom mais claro) */
            --highlight-bg: #374151;        /* Fundo da caixa de destaque */
            --table-header-bg: #818cf8;     /* Fundo do cabeçalho da tabela */
            --table-header-text: #111827;   /* Texto escuro para cabeçalho claro */
            --table-row-even-bg: #1f2937;   /* Fundo da linha par da tabela */
            --border-color: #4b5563;        /* Cor da borda */
        }
    }

    /* 
    ================================================================
    APLICAÇÃO DAS VARIÁVEIS AOS ELEMENTOS
    ================================================================
    */
    body, .stApp {
        font-family: var(--font-family);
        background-color: var(--bg-color);
        color: var(--text-color);
    }

    h1, h2, h3, .stMarkdown {
        color: var(--text-color);
    }

    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }
    
    .stRadio > label, .stSelectbox > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-color);
    }

    .highlight-box {
        background-color: var(--highlight-bg);
        border-left: 5px solid var(--primary-color);
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .highlight-box h3 {
        color: var(--primary-color);
    }

    .stMarkdown table {
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
    }
    .stMarkdown th {
        background-color: var(--table-header-bg);
        color: var(--table-header-text);
        text-align: left;
        padding: 12px 15px;
    }
    .stMarkdown td {
        padding: 12px 15px;
        border-bottom: 1px solid var(--border-color);
    }
    .stMarkdown tr:nth-of-type(even) {
        background-color: var(--table-row-even-bg);
    }
    .stMarkdown tr:last-of-type td {
        border-bottom: none;
    }
    
    a {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        color: #9ca3af; /* Cinza mais suave para o rodapé */
        border-top: 1px solid var(--border-color);
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
    
    col1, col2 = st.columns([1, 1] )
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
if not df.empty:
    categorias = ['Todas'] + sorted(df['Área de Foco'].unique())
    st.sidebar.markdown("### 🧠 Por Área de Foco")
    selected_categoria = st.sidebar.radio("Selecione a área de interesse:", categorias, label_visibility="collapsed")

    fontes = ['Todas'] + sorted(df['Fonte'].unique())
    st.sidebar.markdown("### 🏫 Por Instituição")
    selected_fonte = st.sidebar.selectbox("Selecione a instituição:", fontes, label_visibility="collapsed")

    df_filtered = df.copy()
    if selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Área de Foco'] == selected_categoria]
    if selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == selected_fonte]

    df_filtered = df_filtered.sort_values(by='Titulo')

    st.title("🎯 Mapa de Oportunidades Gratuitas")
    st.markdown(f"### {len(df_filtered)} cursos encontrados para você.")
    st.markdown("""
    <div class="highlight-box">
        <h3>✨ Qualificação ao seu Alcance</h3>
        <p>Navegue por cursos de instituições como <b>FGV, Bradesco e Coursera</b>. Nossa IA organiza tudo para que você encontre a habilidade certa para se destacar.</p>
    </div>
    """, unsafe_allow_html=True)

    df_display = df_filtered[['Titulo', 'Área de Foco', 'Fonte', 'Duracao', 'Link']].copy()
    df_display.rename(columns={'Titulo': 'Título do Curso', 'Área de Foco': 'Área Principal', 'Fonte': 'Instituição', 'Duracao': 'Duração'}, inplace=True)
    df_display['Link'] = df_display['Link'].apply(lambda link: f'<a href="{link}" target="_blank">Acessar Curso ➔</a>' if pd.notna(link) else 'N/A')
    
    st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.warning("Aguardando carregamento dos dados...")

# --- 6. RODAPÉ ---
st.markdown("""
<div class="footer">
    Criado por Jéssica Mendes Pereira Sant'Anna
</div>
""", unsafe_allow_html=True)
