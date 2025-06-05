
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregando os dados
xls = pd.ExcelFile("teste dashboard.xlsx")
df_resumo = xls.parse("Planilha1")
df_detalhado = xls.parse("Planilha2", skiprows=2)

# Tratando dados da Planilha1
df_resumo.rename(columns={"Unnamed: 0": "Categoria"}, inplace=True)
df_resumo.set_index("Categoria", inplace=True)
df_resumo = df_resumo.T

# Tratando dados da Planilha2
df_detalhado.rename(columns={"Rótulos de Linha": "Categoria"}, inplace=True)
df_detalhado = df_detalhado.dropna(subset=["Categoria"])
df_detalhado.set_index("Categoria", inplace=True)
df_detalhado = df_detalhado.iloc[:, :-1]  # Remove "Total Geral"
df_detalhado = df_detalhado.apply(pd.to_numeric, errors="coerce")

# Streamlit App
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("Dashboard Financeiro")

# Seção 1: Gráfico de Linhas - Resumo
st.subheader("Resumo Mensal")
fig1, ax1 = plt.subplots(figsize=(10, 5))
df_resumo.plot(ax=ax1, marker='o')
ax1.set_ylabel("R$")
ax1.set_title("Entradas, Saídas e Lucro por Mês")
ax1.grid(True)
st.pyplot(fig1)

# Seção 2: Filtro de Mês e Tabela
st.subheader("Tabela Interativa")
meses = df_resumo.index.tolist()
mes_escolhido = st.selectbox("Selecione o mês para ver os dados detalhados:", meses)
st.write(df_resumo.loc[mes_escolhido].to_frame(name=mes_escolhido))

# Seção 3: Despesas por Categoria
st.subheader("Distribuição de Despesas")
mes_despesas = st.selectbox("Escolha o mês para ver as despesas:", df_detalhado.columns.tolist())
data = df_detalhado[mes_despesas].dropna()
fig2, ax2 = plt.subplots()
ax2.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
ax2.axis("equal")
ax2.set_title(f"Despesas - {mes_despesas.upper()}")
st.pyplot(fig2)

# Seção 4: Download
st.subheader("Download dos Dados")
with pd.ExcelWriter("dados_dashboard_export.xlsx") as writer:
    df_resumo.T.to_excel(writer, sheet_name="Resumo")
    df_detalhado.to_excel(writer, sheet_name="Detalhado")
with open("dados_dashboard_export.xlsx", "rb") as file:
    st.download_button("Baixar Excel Consolidado", file, file_name="dados_dashboard.xlsx")
