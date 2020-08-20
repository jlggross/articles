import plotly.express as px

# Dados tratados da Parte 1, sem outliers.
df98 = calculaPercentil98(df) 

# Simple treemap
fig1 = px.treemap(df98, path=["Ação"], values="Taxa %")
fig1.show()