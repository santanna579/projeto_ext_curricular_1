import streamlit as st
import pandas as pd

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Mapa de Oportunidades | By Jéssica Sant'Anna",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO E DESIGN (CSS) ---
# CSS para forçar tema claro, novas cores, fontes e design dos componentes.
st.markdown("""
<style>
    /* Importa uma fonte mais moderna do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap' );

    /* Configurações globais de corpo e fonte */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f0f2f6;
    }

    /* Paleta de Cores */
    :root {
        --primary-color: #4f46e5; /* Roxo/Índigo vibrante */
        --secondary-color: #111827; /* Cinza escuro para texto */
        --background-color: #f9fafb; /* Fundo principal um pouco mais claro */
        --sidebar-bg: #ffffff;
        --highlight-bg: #eef2ff; /* Fundo do highlight (tom de roxo claro) */
    }

    /* Força o fundo do app */
    .stApp {
        background-color: var(--background-color);
    }

    /* Títulos */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--secondary-color);
    }

    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid #e5e7eb;
    }
    
    /* Botões de Rádio (Filtros) */
    .stRadio > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--secondary-color);
    }

    /* Caixa de Destaque */
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

    /* Tabela */
    .stMarkdown table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stMarkdown th {
        background-color: var(--primary-color);
        color: white;
        text-align: left;
        padding: 12px 15px;
    }
    .stMarkdown td {
        padding: 12px 15px;
        border-bottom: 1px solid #e5e7eb;
    }
    .stMarkdown tr:nth-of-type(even) {
        background-color: #f9fafb;
    }
    .stMarkdown tr:last-of-type td {
        border-bottom: none;
    }
    
    /* Link de acesso ao curso */
    a {
        color: var(--primary-color);
        font-weight: 600;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    
    /* Rodapé */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        color: #6b7280;
        border-top: 1px solid #e5e7eb;
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

# --- 4. TELA DE BOAS-VINDAS (POP-UP FAKE) ---
# Usamos o st.session_state para controlar se a tela de boas-vindas já foi vista.
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

if st.session_state.show_welcome:
    # URL de uma imagem inspiradora (substitua se quiser)
    welcome_image_url = "https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    
    col1, col2 = st.columns([1, 1] )
    with col1:
        st.image(welcome_image_url, use_column_width=True)
    with col2:
        st.title("O Futuro da sua Carreira Começa Agora.")
        st.markdown("#### Uma plataforma inteligente que mapeia os melhores cursos gratuitos para você.")
        st.write("") # Espaço
        if st.button("🚀 Começar a Explorar"):
            st.session_state.show_welcome = False
            st.experimental_rerun() # Recarrega o script para mostrar a página principal
    # Para o script aqui até o usuário clicar no botão
    st.stop()


# --- 5. PÁGINA PRINCIPAL (APÓS BOAS-VINDAS) ---

# Barra Lateral com Filtros Melhorados (Radio Buttons)
st.sidebar.title("🛠️ Filtros Inteligentes")

if not df.empty:
    # Filtro por Área de Foco com Radio Buttons
    categorias = ['Todas'] + sorted(df['Área de Foco'].unique())
    st.sidebar.markdown("### 🧠 Por Área de Foco")
    selected_categoria = st.sidebar.radio(
        "Selecione a área de interesse:",
        categorias,
        label_visibility="collapsed" # Esconde o label principal do radio
    )

    # Filtro por Instituição
    fontes = ['Todas'] + sorted(df['Fonte'].unique())
    st.sidebar.markdown("### 🏫 Por Instituição")
    selected_fonte = st.sidebar.selectbox(
        "Selecione a instituição:",
        fontes,
        label_visibility="collapsed"
    )

    # Aplicação dos filtros
    df_filtered = df.copy()
    if selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Área de Foco'] == selected_categoria]
    if selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == selected_fonte]

    # Conteúdo Principal
    st.title("🎯 Mapa de Oportunidades Gratuitas")
    st.markdown(f"### {len(df_filtered)} cursos encontrados para você.")

    # Caixa de Destaque
    st.markdown("""
    <div class="highlight-box">
        <h3>✨ Qualificação ao seu Alcance</h3>
        <p>Navegue por cursos de instituições como <b>FGV, Bradesco e Coursera</b>. Nossa IA organiza tudo para que você encontre a habilidade certa para se destacar.</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabela de Resultados
    df_display = df_filtered[['Titulo', 'Área de Foco', 'Fonte', 'Duracao', 'Link']].copy()
    df_display.rename(columns={
        'Titulo': 'Título do Curso',
        'Área de Foco': 'Área Principal',
        'Fonte': 'Instituição',
        'Duracao': 'Duração'
    }, inplace=True)
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
