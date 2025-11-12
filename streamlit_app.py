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
        # Renomeia a coluna NLP para um nome mais intuitivo
        df.rename(columns={'Categoria_NLP': 'Área de Foco'}, inplace=True)
        df['Área de Foco'] = df['Área de Foco'].fillna('Outras Habilidades')
        df['Duracao'] = df['Duracao'].fillna('N/A')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

# Carregar os dados
df = load_data()

# ========================================================================
# 1. ESTILO E PÁGINA INICIAL
# ========================================================================
st.markdown("""
<style>
/* ================================
   1. Forçar Tema Claro Universal
   ================================ */
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebarContent"], .stApp {
    background-color: #f0f2f6 !important;
    color: #1c1c1c !important;
    filter: none !important;
}
html[data-theme="dark"], body[data-theme="dark"] {
    background-color: #f0f2f6 !important;
    color: #1c1c1c !important;
}

/* ================================
   2. Sidebar e Containers
   ================================ */
[data-testid="stSidebarContent"] {
    background-color: #e6f7ff !important;
    color: #1c1c1c !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}

/* ================================
   3. Blocos de Destaque
   ================================ */
.highlight-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #e6f7ff !important;
    border-left: 6px solid #1e90ff;
    margin-bottom: 25px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
}
h3, h2, h1, label, p, .css-16huue1, .css-10trblm {
    color: #003366 !important;
}

/* ================================
   4. Tabelas e Textos
   ================================ */
table {
    background-color: white !important;
    color: #222 !important;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
thead {
    background-color: #f0f8ff !important;
    color: #333 !important;
}
tbody tr:nth-of-type(even) {
    background-color: #f9f9f9 !important;
}
tbody tr:hover {
    background-color: #e6f7ff !important;
}

/* ================================
   5. Links e Botões
   ================================ */
a, a:visited {
    color: #1e90ff !important;
    text-decoration: none !important;
}
a:hover {
    color: #0056b3 !important;
    text-decoration: underline !important;
}

/* ================================
   6. Correções de Tema Escuro Nativo
   ================================ */
@media (prefers-color-scheme: dark) {
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebarContent"], .stApp {
        background-color: #f0f2f6 !important;
        color: #1c1c1c !important;
    }
    h1, h2, h3, p, span, div {
        color: #1c1c1c !important;
    }
    table {
        background-color: white !important;
        color: #222 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ========================================================================
# 2. CONTEÚDO PRINCIPAL
# ========================================================================
st.title("🎯 Seu Mapa para Oportunidades Profissionais Gratuitas")

st.markdown("""
<div class="highlight-box">
    <h3>🚀 ALAVANQUE SUA CARREIRA</h3>
    <p>Nossa plataforma varre e organiza centenas de cursos de instituições de ponta (FGV, Bradesco, Coursera) usando <b>Inteligência Artificial</b> para que você encontre a habilidade exata que o mercado de trabalho precisa. <b>Sua próxima certificação está aqui.</b></p>
</div>
""", unsafe_allow_html=True)

# ========================================================================
# 3. SIDEBAR E FILTROS
# ========================================================================
st.sidebar.title("🛠️ Encontre a Oportunidade Perfeita")

if not df.empty:
    categorias = ['Todas'] + sorted(df['Área de Foco'].unique())
    selected_categoria = st.sidebar.selectbox("🧠 Filtro de Habilidade (Organizado pela IA)", categorias)

    fontes = ['Todas'] + sorted(df['Fonte'].unique())
    selected_fonte = st.sidebar.selectbox("📍 Instituição de Ensino", fontes)
    
    duracoes = ['Todas'] + sorted(df['Duracao'].unique())
    selected_duracao = st.sidebar.selectbox("⏳ Duração Estimada", duracoes)

    # Aplica os filtros
    df_filtered = df.copy()
    if selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Área de Foco'] == selected_categoria]
    if selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == selected_fonte]
    if selected_duracao != 'Todas':
        df_filtered = df_filtered[df_filtered['Duracao'] == selected_duracao]

    # ====================================================================
    # 4. RESULTADOS
    # ====================================================================
    st.header(f"Total de Oportunidades Encontradas: {len(df_filtered)}")
    st.markdown("---")

    def make_clickable(link):
        """Transforma URL em link clicável que abre em nova aba."""
        if isinstance(link, str) and link.startswith('http'):
            return f'<a target="_blank" href="{link}">Acessar Curso 🔗</a>'
        return 'N/A'

    df_display = df_filtered[['Fonte', 'Área de Foco', 'Titulo', 'Duracao', 'Link']].copy()
    df_display.columns = ['Fonte', 'Área Principal (IA)', 'Título do Curso', 'Duração', 'Acesso Rápido']
    df_display['Acesso Rápido'] = df_display['Acesso Rápido'].apply(make_clickable)

    st.markdown(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"Projeto Integrador: {len(df)} oportunidades analisadas de {df['Fonte'].nunique()} instituições. Solução de impacto social e replicabilidade.")
else:
    st.title("Sistema de Mapeamento de Oportunidades (Projeto Integrador)")
    st.warning("Aguardando carregamento dos dados classificados...")
