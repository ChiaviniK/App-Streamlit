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
# SIDEBAR
# ======================
st.sidebar.header("📁 Dados do Projeto")

CSV_URL = "https://raw.githubusercontent.com/ChiaviniK/App-Streamlit/main/Movies.csv"

# Download do arquivo
response = requests.get(CSV_URL)
csv_bytes = response.content

st.sidebar.download_button(
    label="⬇️ Baixar movies.csv",
    data=csv_bytes,
    file_name="movies.csv",
    mime="text/csv"
)

st.sidebar.markdown("---")

st.sidebar.header("⚙️ Configurações")
uploaded_file = st.sidebar.file_uploader(
    "Ou envie o arquivo movies.csv",
    type="csv"
)

# ======================
# CARREGAMENTO DOS DADOS
# ======================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv(BytesIO(csv_bytes))

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

with col3:
    if "Year" in df.columns:
        st.metric("📆 Anos Únicos", df["Year"].nunique())

# ======================
# FILTROS
# ======================
st.markdown("---")
st.subheader("🔎 Filtros Interativos")

colf1, colf2 = st.columns(2)

filtered_df = df.copy()

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
            (int(df["Year"].min()), int(df["Year"].max()))
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

with colg2:
    st.markdown("**📆 Filmes por Ano**")
    if "Year" in filtered_df.columns:
        year_count = filtered_df["Year"].value_counts().sort_index()
        st.line_chart(year_count)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("💡 Projeto educacional • Sprint 1 • Streamflix Dashboard")
