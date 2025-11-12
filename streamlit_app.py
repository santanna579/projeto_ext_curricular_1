import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURAÇÕES E ESTILO ---
st.set_page_config(
    page_title="Seu Futuro Começa Aqui: Oportunidades Gratuitas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho para o arquivo final gerado pelo NLP
DATA_URL = 'cursos_classificados.csv'

# Função para carregar e cachear os dados
@st.cache_data
def load_data():
    """Carrega e prepara os dados classificados."""
    try:
        df = pd.read_csv(DATA_URL)
        # 1. REMOVER JARGÃO TÉCNICO: Renomear a coluna NLP para algo intuitivo
        df.rename(columns={'Categoria_NLP': 'Área de Foco'}, inplace=True)
        
        # Limpeza e preenchimento
        df['Área de Foco'] = df['Área de Foco'].fillna('Outras Habilidades')
        df['Duracao'] = df['Duracao'].fillna('N/A')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

# Carregar os dados
df = load_data()

# ==============================================================================
# 1. ESTILO E PÁGINA INICIAL (Gatilhos Mentais)
# ==============================================================================
st.title("🎯 Seu Mapa para Oportunidades Profissionais Gratuitas")

st.markdown("""
<style>
/* 1. CORREÇÃO CRÍTICA: Fundo da Aplicação (Força a cor clara em todos os contêineres) */
/* Usa um seletor abrangente para garantir que a cor #f0f2f6 se aplique universalmente */
.stApp {
    background-color: #f0f2f6; 
}
[data-testid="stAppViewContainer"] {
    background-color: #f0f2f6 !important;
}
[data-testid="stSidebarContent"] {
    background-color: #e6f7ff !important; /* Um azul pastel leve para a sidebar */
}


/* 2. Destaque Inicial (Azul Pastel/Acolhedor) */
.highlight-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #e6f7ff; /* Azul pastel */
    border-left: 6px solid #1e90ff; /* Borda azul vibrante */
    margin-bottom: 25px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
}
h3 {
    color: #007bff;
}

/* 3. Estilo da Tabela (Contraste e Legibilidade) */
table {
    background-color: white !important; /* Fundo branco puro para destaque */
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
}
/* Estilo do cabeçalho da tabela */
thead {
    background-color: #f0f8ff !important; 
    color: #333333; 
}
/* Fundo sutil para linhas pares (Zebra) */
tbody tr:nth-of-type(even) {
    background-color: #f9f9f9; 
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="highlight-box">
    <h3>🚀 ALAVANQUE SUA CARREIRA</h3>
    <p>Nossa plataforma varre e organiza centenas de cursos de instituições de ponta (FGV, Bradesco, Coursera) usando <b>Inteligência Artificial</b> para que você encontre a habilidade exata que o mercado de trabalho precisa. <b>Sua próxima certificação está aqui.</b></p>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. SIDEBAR E FILTROS
# ==============================================================================
st.sidebar.title("🛠️ Encontre a Oportunidade Perfeita")

if not df.empty:
    # FILTRO 1: ÁREA DE FOCO (Categoria classificada pela IA)
    categorias = ['Todas'] + sorted(df['Área de Foco'].unique())
    selected_categoria = st.sidebar.selectbox(
        "🧠 Filtro de Habilidade (Organizado pela IA)",
        categorias
    )

    # FILTRO 2: Fonte
    fontes = ['Todas'] + sorted(df['Fonte'].unique())
    selected_fonte = st.sidebar.selectbox(
        "📍 Instituição de Ensino",
        fontes
    )
    
    # FILTRO 3: Duração
    duracoes = ['Todas'] + sorted(df['Duracao'].unique())
    selected_duracao = st.sidebar.selectbox(
        "⏳ Duração Estimada",
        duracoes
    )

    # Aplica os filtros
    df_filtered = df.copy()
    
    if selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Área de Foco'] == selected_categoria]
        
    if selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == selected_fonte]

    if selected_duracao != 'Todas':
        df_filtered = df_filtered[df_filtered['Duracao'] == selected_duracao]
    
    
    # ==============================================================================
    # 3. TABELA DE RESULTADOS (LINKS CLICÁVEIS)
    # ==============================================================================
    
    st.header(f"Total de Oportunidades Encontradas: {len(df_filtered)}")
    st.markdown("---")

    # Função para gerar link clicável que abre em nova aba
    def make_clickable(link):
        """Transforma URL em link clicável que abre em nova aba (target='_blank')."""
        if isinstance(link, str) and link.startswith('http'):
            return f'<a target="_blank" href="{link}">Acessar Curso 🔗</a>'
        return 'N/A'

    df_display = df_filtered[['Fonte', 'Área de Foco', 'Titulo', 'Duracao', 'Link']].copy()
    df_display.columns = ['Fonte', 'Área Principal (IA)', 'Título do Curso', 'Duração', 'Acesso Rápido']
    
    # Aplica a função para criar os links CLICÁVEIS
    df_display['Acesso Rápido'] = df_display['Acesso Rápido'].apply(make_clickable)

    # Exibe a tabela final
    st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"Projeto Integrador: {len(df)} oportunidades analisadas de {df['Fonte'].nunique()} instituições. Solução de impacto social e replicabilidade.")

else:
    st.title("Sistema de Mapeamento de Oportunidades (Projeto Integrador)")
    st.warning("Aguardando carregamento dos dados classificados...")
