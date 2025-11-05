import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12,6)

st.title("Análise Exploratória do Campeonato Brasileiro")

# Carregar dados
df = pd.read_csv("Tabela_Clubes.csv")

# Sidebar: filtros
st.sidebar.header("Filtros")
ano_inicio = int(df['Ano'].min())
ano_fim = int(df['Ano'].max())
ano_selecionado = st.sidebar.slider("Selecionar período de anos", ano_inicio, ano_fim, (ano_inicio, ano_fim))

df_filtrado = df[(df['Ano'] >= ano_selecionado[0]) & (df['Ano'] <= ano_selecionado[1])]

st.subheader("Dados Filtrados")
st.dataframe(df_filtrado)

# Total de clubes únicos
times_unicos = df_filtrado['Clube'].nunique()
st.write(f"Total de clubes únicos no período: {times_unicos}")

# Frequência dos clubes
st.subheader("Frequência de Participação dos Clubes")
frequencia_times = df_filtrado['Clube'].value_counts()
st.bar_chart(frequencia_times)

# Campeões por ano
st.subheader("Campeões por Ano")
campeoes = df_filtrado[df_filtrado['Posição'] == 1][['Ano','Clube']].sort_values('Ano')
st.dataframe(campeoes)

# Clube com mais títulos
titulos = df_filtrado[df_filtrado['Posição'] == 1]['Clube'].value_counts()
if not titulos.empty:
    time_mais_titulos = titulos.idxmax()
    quantidade_titulos = titulos.max()
    st.write(f"Time com mais títulos: {time_mais_titulos} ({quantidade_titulos} títulos)")

# Clube com mais derrotas
derrotas = df_filtrado.groupby('Clube')['Derrotas'].sum().sort_values(ascending=False)
if not derrotas.empty:
    mais_derrotas = derrotas.idxmax()
    quantidade_derrotas = derrotas.max()
    st.write(f"Clube com mais derrotas: {mais_derrotas} ({quantidade_derrotas} derrotas)")

# Clube com menos derrotas
if not derrotas.empty:
    menos_derrotas = derrotas.idxmin()
    quantidade_menos_derrotas = derrotas.min()
    st.write(f"Clube com menos derrotas: {menos_derrotas} ({quantidade_menos_derrotas} derrotas)")

# Visualizações
st.subheader("Distribuição de Derrotas")
fig, ax = plt.subplots()
sns.histplot(df_filtrado['Derrotas'], bins=20, kde=False, ax=ax)
ax.set_xlabel("Derrotas")
ax.set_ylabel("Frequência")
st.pyplot(fig)

st.subheader("Top 10 Clubes com Mais Títulos")
top10_titulos = titulos.head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top10_titulos.values, y=top10_titulos.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Número de Títulos")
ax2.set_ylabel("Clube")
st.pyplot(fig2)

st.subheader("Evolução Histórica de Títulos por Clube")
df_campeoes = df_filtrado[df_filtrado['Posição'] == 1]
df_cum = df_campeoes.groupby(['Ano','Clube']).size().unstack(fill_value=0).cumsum()
st.line_chart(df_cum)
