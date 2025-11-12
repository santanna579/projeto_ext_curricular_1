import streamlit as st
import pandas as pd

# ------------------------ CONFIGURAÇÕES GERAIS ------------------------
st.set_page_config(
    page_title="Seu Futuro Começa Aqui",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_URL = "cursos_classificados.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_URL)
        df.rename(columns={'Categoria_NLP': 'Área de Foco'}, inplace=True)
        df['Área de Foco'] = df['Área de Foco'].fillna('Outras Habilidades')
        df['Duracao'] = df['Duracao'].fillna('N/A')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# ------------------------ CSS PERSONALIZADO ------------------------
st.markdown("""
<style>
/* Tema claro forçado */
html, body, [data-testid="stAppViewContainer"], .stApp {
  background: linear-gradient(135deg, #f9fbff 0%, #e9f6ff 100%) !important;
  color: #111 !important;
}

/* Corrige cores do modo escuro */
html[data-theme="dark"], html[data-theme="dark"] body {
  background: linear-gradient(135deg, #f9fbff 0%, #e9f6ff 100%) !important;
  color: #111 !important;
}

/* Header */
.header {
  text-align: center;
  padding-top: 60px;
  padding-bottom: 20px;
}
.header h1 {
  font-size: 2.4rem;
  font-weight: 800;
  color: #003366;
}
.header p {
  font-size: 1.1rem;
  color: #00509e;
  margin-top: -10px;
}

/* Botão principal */
.stButton>button {
  width: 70%;
  max-width: 400px;
  background: linear-gradient(90deg, #0073e6, #00a8ff);
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 10px;
  border: none;
  padding: 10px 20px;
  margin-top: 20px;
}
.stButton>button:hover {
  background: linear-gradient(90deg, #005bb5, #008ad9);
}

/* Grid responsivo */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
@media (max-width: 1000px) {
  .cards-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 680px) {
  .cards-grid { grid-template-columns: repeat(1, 1fr); }
}

/* Card de curso */
.course-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.course-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}
.course-title {
  color: #003366;
  font-weight: 600;
  font-size: 1.05rem;
  margin-bottom: 6px;
}
.course-meta {
  color: #444;
  font-size: 0.9rem;
  margin-bottom: 10px;
}
.course-cta a {
  display: inline-block;
  background: #0073e6;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  text-decoration: none;
}
.course-cta a:hover {
  background: #005bb5;
}
</style>
""", unsafe_allow_html=True)

# ------------------------ TELA INICIAL ------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.markdown("🎓", unsafe_allow_html=True)
    st.markdown("<h1>Seu Futuro Começa Aqui</h1>", unsafe_allow_html=True)
    st.markdown("<p>Explore cursos gratuitos das melhores instituições e desenvolva novas habilidades.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("🌟 Explorar Cursos"):
        st.session_state.started = True
        st.experimental_rerun()
    st.stop()

# ------------------------ CONTEÚDO PRINCIPAL ------------------------
st.header("🔎 Explorar Cursos Disponíveis")
st.caption("Filtre por área de foco, duração ou instituição.")

if df.empty:
    st.error("⚠️ Nenhum arquivo CSV encontrado. Coloque 'cursos_classificados.csv' no mesmo diretório do app.")
else:
    # Filtros laterais
    st.sidebar.header("Filtros")
    categorias = ['Todas'] + sorted(df['Área de Foco'].unique())
    selected_categoria = st.sidebar.selectbox("Área de Foco (IA)", categorias)
    fontes = ['Todas'] + sorted(df['Fonte'].unique())
    selected_fonte = st.sidebar.selectbox("Fonte", fontes)
    duracoes = ['Todas'] + sorted(df['Duracao'].unique())
    selected_duracao = st.sidebar.selectbox("Duração", duracoes)

    df_filtered = df.copy()
    if selected_categoria != 'Todas':
        df_filtered = df_filtered[df_filtered['Área de Foco'] == selected_categoria]
    if selected_fonte != 'Todas':
        df_filtered = df_filtered[df_filtered['Fonte'] == selected_fonte]
    if selected_duracao != 'Todas':
        df_filtered = df_filtered[df_filtered['Duracao'] == selected_duracao]

    st.subheader(f"Total de cursos encontrados: {len(df_filtered)}")
    st.write("")  # espaço visual

    # Grade de cards
    html_cards = '<div class="cards-grid">'
    for _, row in df_filtered.iterrows():
        titulo = row.get('Titulo', '-')
        dur = row.get('Duracao', '-')
        nivel = row.get('Nivel', row.get('Area', '-'))
        link = row.get('Link', '')
        fonte = row.get('Fonte', '')
        html_cards += f'''
        <div class="course-card">
            <div class="course-title">{titulo}</div>
            <div class="course-meta"><b>Fonte:</b> {fonte} • <b>Duração:</b> {dur} • <b>Nível:</b> {nivel}</div>
            <div class="course-cta"><a href="{link}" target="_blank">Acessar Curso</a></div>
        </div>
        '''
    html_cards += '</div>'
    st.markdown(html_cards, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.caption("💡 Projeto Integrador | Dados extraídos via script local | Interface feita com Streamlit")
