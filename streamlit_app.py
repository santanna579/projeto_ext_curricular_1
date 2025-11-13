import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURAÇÃO DA PÁGINA E ESTILO ---
st.set_page_config(
    page_title="Mapa de Oportunidades | Cursos Gratuitos",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Forçar o tema claro e injetar CSS customizado ---
# Este CSS resolve o problema de fontes claras no tema claro e melhora o design geral.
st.markdown("""
<style>
    /* Força o tema claro (background principal e texto) */
    .stApp {
        background-color: #f0f2f6; /* Cinza claro para o fundo */
    }

    /* Títulos e textos com cores de alto contraste */
    h1, h2, h3, h4, h5, h6 {
        color: #1a202c; /* Cor escura para os títulos */
    }
    
    p, .stMarkdown {
        color: #2d3748; /* Cor um pouco mais suave para parágrafos */
    }

    /* Design da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Caixa de destaque com gatilhos mentais */
    .highlight-box {
        background-color: #e6f7ff; /* Azul bem claro */
        border-left: 5px solid #1c64f2; /* Borda azul forte */
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .highlight-box h3 {
        color: #1c64f2; /* Azul forte para o título da caixa */
        margin-bottom: 10px;
    }
    .highlight-box p {
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Estilo da tabela de cursos */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Link de acesso ao curso mais chamativo */
    a {
        color: #1c64f2;
        font-weight: bold;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)


# --- 2. CARREGAMENTO E CACHE DOS DADOS ---
# Caminho para o arquivo CSV gerado pelo seu script de NLP
DATA_URL = 'cursos_classificados.csv'

@st.cache_data
def load_data():
    """
    Carrega os dados do CSV, renomeia colunas para clareza e trata valores ausentes.
    O cache acelera o carregamento em execuções futuras.
    """
    try:
        df = pd.read_csv(DATA_URL)
        # Renomeia a coluna para ser mais intuitiva para o usuário final
        df.rename(columns={'Categoria_NLP': 'Área de Foco'}, inplace=True)
        # Preenche categorias e durações vazias para evitar erros nos filtros
        df['Área de Foco'] = df['Área de Foco'].fillna('Outras')
        df['Duracao'] = df['Duracao'].fillna('Não Informada')
        return df
    except FileNotFoundError:
        # Se o arquivo não for encontrado, exibe um aviso em vez de quebrar o app
        st.error(f"Erro: O arquivo '{DATA_URL}' não foi encontrado. Por favor, verifique se o arquivo está no mesmo diretório do seu app.")
        return pd.DataFrame()

# Carrega os dados na inicialização do app
df = load_data()

# --- 3. LAYOUT DA PÁGINA PRINCIPAL ---

# Título e subtítulo com gatilhos mentais
st.title("🎯 Seu Mapa para a Próxima Oportunidade")
st.markdown("### Encontre cursos gratuitos das melhores instituições, analisados e organizados por Inteligência Artificial.")

# Caixa de destaque
st.markdown("""
<div class="highlight-box">
    <h3>🚀 Impulsione sua Carreira, Hoje.</h3>
    <p>Navegue por centenas de cursos gratuitos de instituições como <b>FGV, Bradesco e Coursera</b>. Nossa IA classifica cada oportunidade para que você encontre exatamente o que precisa para se destacar no mercado. <b>Sua qualificação está a um clique de distância.</b></p>
</div>
""", unsafe_allow_html=True)


# --- 4. BARRA LATERAL COM FILTROS ---
st.sidebar.header("🛠️ Filtros Inteligentes")

if not df.empty:
    # Filtro por Área de Foco (gerada pelo NLP)
    categorias = ['Todas'] + sorted(df['Área de Foco'].unique())
    selected_categoria = st.sidebar.selectbox(
        "🧠 Filtrar por Área de Foco:",
        categorias,
        help="Áreas identificadas automaticamente pela nossa IA."
    )

    # Filtro por Instituição
    fontes = ['Todas'] + sorted(df['Fonte'].unique())
    selected_fonte = st.sidebar.selectbox(
        "🏫 Filtrar por Instituição:",
        fontes
    )

    # Aplicação dos filtros no DataFrame
    df_filtered = df.copy()
    if selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Área de Foco'] == selected_categoria]
    if selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == selected_fonte]

    # --- 5. EXIBIÇÃO DOS RESULTADOS ---
    
    st.header(f"✨ {len(df_filtered)} Oportunidades Encontradas")
    st.markdown("Use a tabela abaixo para explorar os cursos. Clique no link para acessar diretamente a página.")

    # Preparação da tabela para exibição
    df_display = df_filtered[['Titulo', 'Área de Foco', 'Fonte', 'Duracao', 'Link']].copy()
    df_display.rename(columns={
        'Titulo': 'Título do Curso',
        'Área de Foco': 'Área Principal (IA)',
        'Fonte': 'Instituição',
        'Duracao': 'Duração'
    }, inplace=True)

    # Transforma a coluna 'Link' em links HTML clicáveis que abrem em nova aba
    df_display['Link'] = df_display['Link'].apply(lambda link: f'<a href="{link}" target="_blank">Acessar Curso ➔</a>' if pd.notna(link) else 'Link indisponível')

    # Exibe a tabela usando st.markdown para renderizar o HTML dos links
    st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.markdown("---")

    # --- 6. GRÁFICO DE VISÃO DE MERCADO ---
    st.header("📊 Visão Geral das Oportunidades")
    st.markdown("Veja a distribuição de cursos por área de foco. Isso pode te ajudar a identificar as áreas com mais oportunidades disponíveis.")

    if not df_filtered.empty:
        # Contagem de cursos por categoria
        chart_data = df_filtered['Área de Foco'].value_counts().reset_index()
        chart_data.columns = ['Área de Foco', 'Quantidade de Cursos']

        # Criação do gráfico de barras com Plotly
        fig = px.bar(
            chart_data,
            x='Quantidade de Cursos',
            y='Área de Foco',
            orientation='h',
            title='Quantidade de Cursos por Área',
            labels={'Quantidade de Cursos': 'Nº de Cursos', 'Área de Foco': 'Área'},
            color_discrete_sequence=['#1c64f2']
        )
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'}, # Ordena as barras da menor para a maior
            plot_bgcolor='rgba(0,0,0,0)', # Fundo transparente
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    # Mensagem exibida se o DataFrame estiver vazio (ex: arquivo não encontrado)
    st.warning("Ainda não há dados para exibir. Carregue o arquivo `cursos_classificados.csv` para começar.")

