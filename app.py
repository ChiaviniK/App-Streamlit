import streamlit as st
import pandas as pd

st.set_page_config(page_title="Streamflix Dashboard", layout="wide")

st.title("🎬 Streamflix — Dashboard de Filmes")
st.write("Análise exploratória inicial do catálogo de filmes")

# Upload ou leitura do CSV
uploaded_file = st.file_uploader("Envie o arquivo movies.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Visão geral dos dados")
    st.dataframe(df.head())

    st.subheader("📊 Métricas básicas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de filmes", len(df))

    with col2:
        if "genre" in df.columns:
            st.metric("Gêneros únicos", df["genre"].nunique())

    with col3:
        if "year" in df.columns:
            st.metric("Anos únicos", df["year"].nunique())

    st.subheader("🎥 Filmes por gênero")
    if "genre" in df.columns:
        genre_count = df["genre"].value_counts()
        st.bar_chart(genre_count)

else:
    st.info("👆 Envie o arquivo movies.csv para iniciar a análise.")
