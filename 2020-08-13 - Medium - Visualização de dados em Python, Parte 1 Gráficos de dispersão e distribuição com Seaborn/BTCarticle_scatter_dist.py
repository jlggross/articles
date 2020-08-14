import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import seaborn as sns
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

"""
Function:
    BTGpactual_get98percentileDF
Description:
    Get the DataFrame with data values below the 98th percentile.
Parameters:
    * df : DataFrame with the original data.
Return:
    * df99 : DataFrame with data below the 98th percentile.
References:
    * Distribution of values and boxplot (1): https://medium.com/dayem-siddiqui/understanding-and-interpreting-box-plots-d07aab9d1b6c
    * Distribution of values and boxplot (2): https://www.wellbeingatschool.org.nz/information-sheet/understanding-and-interpreting-box-plots
"""
def calculaPercentil98(df):

    # Define os percentis para ver como os dados estão distribuídos
    description = df.describe(percentiles=[.25, .5, .75, .9, .95, .98, .99, .999])
    print(description)
    description_dict = description.to_dict()

    # Coleta o valor que delimita 98% das amostras no DataFrame
    data_cut = float(description_dict["Taxa %"]["98%"])

    # Seleciona apenas as amostras dentro do intervalo de 98%, removendo os outliers
    df98 = df[df["Taxa %"] <= data_cut]

    return df98

"""
Function:
    BTGpactual_printBTCdata
Description:
    Plot the DataFrame data.
Requirements:
    > pip3 install matplotlib 
    > pip3 install seaborn
Parameters:
    * df_btcBTG : DataFrame with data.
"""
def BTGpactual_printBTCdata(df, bins):

    df98 = calculaPercentil98(df)

    # Plotting
    sns.set_style("white")
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # ------------------------------------------------
    # Scatter plot
    # ------------------------------------------------
    cmap = sns.cubehelix_palette(rot=-.4, as_cmap=True)
    g1 = sns.scatterplot(x="Ação", y="Taxa %",
                        hue="Taxa %", size="Taxa %",
                        palette=cmap,
                        data=df98,
                        ax=ax[0])
    g1.set_title("Taxas de BTC a.a. no Banco BTG Pactual")
    g1.set_xlabel("Ações")
    g1.yaxis.set_major_locator(ticker.MultipleLocator(1))

    for ind, label in enumerate(g1.get_xticklabels()):
        if ind % 5 == 0:  # Mantém apenas os rótulos múltiplos de 4 no eixo x
            label.set_visible(True)
        else:
            label.set_visible(False)
    plt.setp(ax[0].get_xticklabels(), rotation=45)
    plt.legend(loc='upper left')

    # ------------------------------------------------
    # Distribution plot
    # ------------------------------------------------
    # First line of the plot
    g2 = sns.distplot(df98["Taxa %"], ax=ax[1], kde=True, hist=False)

    # Second line of the plot
    new_ax1 = ax[1].twinx()
    g3 = sns.distplot(df98["Taxa %"], ax=new_ax1, kde=False, hist=True, bins=bins, norm_hist=False)

    # Name axis
    g2.set_ylabel("Probabilidade")
    g3.set_ylabel("Qauantidade")
    g3.set_title("BTC BTG Pactual - " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    g2.xaxis.set_major_locator(ticker.MultipleLocator((df98["Taxa %"].max() - df98["Taxa %"].min()) / bins))
    plt.setp(ax[1].get_xticklabels(), rotation=45)

    plt.tight_layout()
    plt.show()

"""
Function:
    BTGpactual_getBTC
Description:
    Collect the BTC taxes annual taxes from BTG Pactual website.
Parameters:
    * driver : Chromedriver to access a website.
Return:
    * df : DataFrame with BTC per stock.
"""
def BTGpactual_getBTC(driver):
    xpath = "/html/body/app-root/div/app-variable-sale/section/app-variable-assets-list/section/div/div[2]/div/ul/li[1]"
    df = pd.DataFrame(columns=["Ação", "Taxa %"])
    url = "https://www.btgpactualdigital.com/renda-variavel/venda-descoberta"

    driver.get(url)

    # Wait element
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Timeout!")

    driver.implicitly_wait(3)
    elements = driver.find_elements_by_xpath(xpath[:-3])
    print("Collecting BTC:")
    for i, element in enumerate(elements):
        if len(element.text) < 11:
            continue
        newElement = {}
        newElement["Ação"] = element.text.split("\n")[0]
        newElement["Taxa %"] = element.text.split("\n")[1]
        print(i, newElement)
        df = df.append(newElement, ignore_index=True)

    df["Taxa %"] = df["Taxa %"].str.replace(",", ".")
    df["Taxa %"] = df["Taxa %"].str.replace("%", "")
    df["Taxa %"] = df["Taxa %"].astype('float')

    print("Info about BTC data From BTG Pactual:")
    print(df.info())

    df.to_excel("output.xlsx")

    return df

"""
Main - Where everything starts. 
"""
if "__main__" == __name__:

    driver = webdriver.Chrome()
    driver.set_window_position(2000, 0)
    driver.minimize_window()

    # Get BTC from BTG Pactual
    print("Web Scrapping: BTG Pactual")
    df_btcBTG = BTGpactual_getBTC(driver)
    BTGpactual_printBTCdata(df_btcBTG, bins=20)

    driver.quit()