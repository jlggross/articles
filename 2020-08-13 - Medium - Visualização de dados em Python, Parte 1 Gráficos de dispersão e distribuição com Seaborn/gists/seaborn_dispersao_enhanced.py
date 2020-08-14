import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Criando o ambiente do gráfico 
sns.set_style("white")
plt.figure(figsize=(15, 10))

# Gráfico de Dispersão
cmap = sns.cubehelix_palette(rot=-.4, as_cmap=True)
g = sns.scatterplot(x="Ação", y="Taxa %", 
                    hue="Taxa %", size="Taxa %",
                    palette=cmap, data=df98) #df98 calculado anteriormente

# Ajusta rótulos
g.set_title("Taxas de BTC a.a. no Banco BTG Pactual")
g.set_xlabel("Ações")
g.yaxis.set_major_locator(ticker.MultipleLocator(1))

for ind, label in enumerate(g.get_xticklabels()):
    if ind % 4 == 0:  # Mantém apenas os rótulos múltiplos de 4 no eixo x
        label.set_visible(True)
    else:
        label.set_visible(False)
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.show()