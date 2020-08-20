import pandas as pd
import ploty.express as px

# Dados tratados
df98 = calculaPercentil98(df)

# Cria grupos
bins = 20 # Quantidade de grupos
min_value = df98["Taxa %"].min()
max_value = df98["Taxa %"].max()
bin_interval = (max_value - min_value) / bins
ranges = [bin_interval * i for i in range(bins + 2)]
group_names = ["Group" + str(i+1) + " " + ('%.2f' % ranges[i]) + "% a " + ('%.2f' % ranges[i+1]) + "%" for i in range(bins + 1)]

# Atualiza rótulos dos grupos
df_new = df98
df_new["Group"] = pd.cut(df_new["Taxa %"], bins=ranges, labels=group_names)
df_new = df_new.groupby("Group").agg("count")
for i in range(df_new.shape[0]):
    group_names[i] = group_names[i] + " (" + str(df_new.iloc[i][1]) + ")"
df98["Group"] = pd.cut(df98["Taxa %"], bins=ranges, labels=group_names)

# Cria Treemap hierárquico
df98["BTC"] = "BTC"  # In order to have a single root node
fig = px.treemap(df98, path=["BTC", "Group", "Ação"], values="Taxa %", color="Ação")
fig.show()