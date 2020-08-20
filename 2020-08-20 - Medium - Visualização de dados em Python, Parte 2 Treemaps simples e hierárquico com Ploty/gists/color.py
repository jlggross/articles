# Valores não-numéricos/categóricos. Cores discretas.
fig1 = px.treemap(df98, path=["Ação"], 
                  values="Taxa %", color="Ação")

# Valores numéricos. Cores contínuas.
fig1 = px.treemap(df98, path=["Ação"], 
                  values="Taxa %", color="Taxa %")