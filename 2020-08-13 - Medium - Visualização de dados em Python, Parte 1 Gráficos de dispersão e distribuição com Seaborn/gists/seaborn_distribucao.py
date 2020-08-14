import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

bins = 20

# Criando o ambiente do gráfico 
sns.set_style("white")
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Insere curva KDE (Kernel Density Estimation)
g1 = sns.distplot(df98["Taxa %"], ax=ax, 
                  kde=True, hist=False) 

# Insere histograma
ax_copy = ax.twinx()
g2 = sns.distplot(df98["Taxa %"], ax=ax_copy, kde=False, hist=True, 
             bins=bins, norm_hist=False)

# Ajusta rótulos
g1.set_ylabel("Probabilidade")
g2.set_ylabel("Qauantidade")
g2.set_title("BTC BTG Pactual - " + datetime.now().strftime("%Y-%m-%d %H:%M"))
g1.xaxis.set_major_locator(ticker.MultipleLocator((df98["Taxa %"].max()-df98["Taxa %"].min())/bins))
plt.setp(ax.get_xticklabels(), rotation=45)
plt.show()