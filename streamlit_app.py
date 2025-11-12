import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURAÇÕES BÁSICAS ---
st.set_page_config(
    page_title="Projeto Integrador - Mapeamento de Oportunidades",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho para o arquivo final gerado pelo NLP
DATA_URL = 'cursos_classificados.csv'

# Função para carregar e cachear os dados
# O decorator 'cache_data' garante que os dados sejam lidos do CSV apenas uma vez, tornando o app rápido!
@st.cache_data
def load_data():
    """Carrega e prepara os dados classificados."""
    try:
        df = pd.read_csv(DATA_URL)
        # Limpeza e preenchimento de N/A para melhor filtragem
        df['Categoria_NLP'] = df['Categoria_NLP'].fillna('Sem Categoria')
        df['Duracao'] = df['Duracao'].fillna('N/A')
        return df
    except FileNotFoundError:
        st.error(f"Erro: Arquivo {DATA_URL} não encontrado. Execute o nlp_classifier.py primeiro!")
        return pd.DataFrame()

# Carregar os dados
df = load_data()

# ==============================================================================
# 1. SIDEBAR (Filtros)
# ==============================================================================
st.sidebar.title("🔍 Painel de Filtros")
st.sidebar.markdown("Use os filtros para explorar as oportunidades classificadas pelo modelo de NLP.")

if not df.empty:
    # FILTRO 1: Categoria (O MAIS IMPORTANTE - Resultado do NLP)
    categorias = ['Todas'] + sorted(df['Categoria_NLP'].unique())
    selected_categoria = st.sidebar.selectbox(
        "🧠 Categoria Classificada (NLP)",
        categorias
    )

    # FILTRO 2: Fonte (Ex: FGV, Bradesco)
    fontes = ['Todas'] + sorted(df['Fonte'].unique())
    selected_fonte = st.sidebar.selectbox(
        "📍 Fonte de Dados",
        fontes
    )
    
    # FILTRO 3: Duração
    duracoes = ['Todas'] + sorted(df['Duracao'].unique())
    selected_duracao = st.sidebar.selectbox(
        "⏳ Duração",
        duracoes
    )

    # Aplica os filtros
    df_filtered = df.copy()
    
    if selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Categoria_NLP'] == selected_categoria]
        
    if selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == selected_fonte]
        
    if selected_duracao != 'Todas':
        df_filtered = df_filtered[df_filtered['Duracao'] == selected_duracao]

# ==============================================================================
# 2. CORPO PRINCIPAL DO DASHBOARD
# ==============================================================================

if df.empty:
    st.title("Sistema de Mapeamento de Oportunidades (Projeto Integrador)")
    st.write("Aguardando carregamento dos dados classificados...")
else:
    st.title("🎯 Sistema de Mapeamento de Oportunidades")
    st.subheader(f"Análise de {len(df)} Oportunidades Classificadas")

    # KPIs (Indicadores Chave)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registros", len(df))
    col2.metric("Fontes Analisadas", df['Fonte'].nunique())
    col3.metric("Categorias Encontradas (NLP)", df['Categoria_NLP'].nunique())

    st.markdown("---")
    
    # Gráfico 1: Distribuição de Cursos por Categoria (NLP)
    st.subheader("📊 Distribuição de Cursos por Categoria (Modelo NLP)")
    
    # Calcula a contagem de cursos por categoria
    category_counts = df_filtered['Categoria_NLP'].value_counts().reset_index()
    category_counts.columns = ['Categoria', 'Contagem']
    
    # Exibe um gráfico de barras interativo (Pode ser ajustado para Altair ou Plotly)
    st.bar_chart(category_counts, x='Categoria', y='Contagem', height=400)
    
    st.markdown("---")
    
    # Tabela de Resultados Filtrados
    st.subheader(f"Lista de Oportunidades ({len(df_filtered)} resultados)")

    # Exibe a tabela final, formatando o link como um hyperlink
    df_display = df_filtered[['Fonte', 'Categoria_NLP', 'Titulo', 'Duracao', 'Link']].copy()
    df_display['Link'] = df_display['Link'].apply(lambda x: f"[Acessar]({x})" if isinstance(x, str) and x.startswith('http') else 'N/A')
    
    st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Projeto Integrador de Ciências de Dados - Evolução Social e Replicabilidade.")