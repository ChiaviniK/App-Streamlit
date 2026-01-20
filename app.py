import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# ======================
# CONFIGURAÇÃO DA PÁGINA
# ======================
st.set_page_config(
    page_title="Streamflix | Dashboard de Filmes",
    page_icon="🎬",
    layout="wide"
)

# ======================
# ESTILO (UX)
# ======================
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.title("🎬 Streamflix — Dashboard de Filmes")
st.caption("Análise exploratória do catálogo de filmes | Sprint 1")
st.markdown("---")

# ======================
# SIDEBAR — DADOS
# ======================
st.sidebar.header("📁 Dados do Projeto")

CSV_URL = "https://raw.githubusercontent.com/ChiaviniK/App-Streamlit/main/Movies.csv"

response = requests.get(CSV_URL)
csv_bytes = response.content

st.sidebar.download_button(
    label="⬇️ Baixar movies.csv",
    data=csv_bytes,
    file_name="movies.csv",
    mime="text/csv"
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Carregamento de Dados")

# ======================
# FUNÇÃO DE CARGA
# ======================
def load_data(file=None):
    if file is not None:
        return pd.read_csv(file)
    return pd.read_csv(BytesIO(csv_bytes))

# ======================
# CONTROLE DE ESTADO
# ======================
if "df" not in st.session_state:
    st.session_state.df = load_data()

uploaded_file = st.sidebar.file_uploader(
    "Envie o arquivo movies.csv",
    type="csv"
)

if uploaded_file is not None:
    st.session_state.df = load_data(uploaded_file)
    st.sidebar.success("Arquivo carregado com sucesso!")

if st.sidebar.button("🔄 Resetar para dados padrão"):
    st.session_state.df = load_data()
    st.sidebar.info("Dados padrão restaurados")

df = st.session_state.df

# ======================
# VISÃO GERAL
# ======================
st.subheader("📄 Visão Geral dos Dados")
st.dataframe(df.head(), use_container_width=True)

# ======================
# MÉTRICAS
# ======================
st.subheader("📊 Métricas Principais")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎞️ Total de Filmes", len(df))

with col2:
    if "Genre" in df.columns:
        st.metric("🎭 Gêneros Únicos", df["Genre"].nunique())
    else:
        st.metric("🎭 Gêneros Únicos", "N/A")

with col3:
    if "Year" in df.columns:
        st.metric("📆 Anos Únicos", df["Year"].nunique())
    else:
        st.metric("📆 Anos Únicos", "N/A")

# ======================
# FILTROS
# ======================
st.markdown("---")
st.subheader("🔎 Filtros Interativos")

filtered_df = df.copy()

colf1, colf2 = st.columns(2)

with colf1:
    if "Genre" in df.columns:
        genres = st.multiselect(
            "Selecione o(s) gênero(s)",
            options=sorted(df["Genre"].dropna().unique())
        )
        if genres:
            filtered_df = filtered_df[filtered_df["Genre"].isin(genres)]

with colf2:
    if "Year" in df.columns:
        year_range = st.slider(
            "Intervalo de anos",
            int(df["Year"].min()),
            int(df["Year"].max()),
            (
                int(df["Year"].min()),
                int(df["Year"].max())
            )
        )
        filtered_df = filtered_df[
            (filtered_df["Year"] >= year_range[0]) &
            (filtered_df["Year"] <= year_range[1])
        ]

# ======================
# VISUALIZAÇÕES
# ======================
st.markdown("---")
st.subheader("📈 Análises")

colg1, colg2 = st.columns(2)

with colg1:
    st.markdown("**🎭 Filmes por Gênero**")
    if "Genre" in filtered_df.columns:
        genre_count = filtered_df["Genre"].value_counts()
        st.bar_chart(genre_count)
    else:
        st.info("Coluna 'Genre' não encontrada.")

with colg2:
    st.markdown("**📆 Filmes por Ano**")
    if "Year" in filtered_df.columns:
        year_count = filtered_df["Year"].value_counts().sort_index()
        st.line_chart(year_count)
    else:
        st.info("Coluna 'Year' não encontrada.")

# ======================
# TABELA FILTRADA
# ======================
st.markdown("---")
st.subheader("📋 Dados Filtrados")
st.dataframe(filtered_df, use_container_width=True)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("💡 Projeto educacional • Sprint 1 • Streamflix Dashboard")
