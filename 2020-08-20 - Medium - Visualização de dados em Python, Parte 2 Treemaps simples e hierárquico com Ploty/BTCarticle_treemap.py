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
    calculaPercentil98
Description:
    Get the DataFrame with data values below the 98th percentile.
Parameters:
    * df : DataFrame with the original data.
Return:
    * df98 : DataFrame with data below the 98th percentile.
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
    df98.reset_index(inplace=True, drop=True)

    return df98

"""
Function:
    BTGpactual_printTreemap
Description:
    Plot the DataFrame data in a treemap
Requirements:
    > pip3 install plotly
Parameters:
    * df_btcBTG : DataFrame with data.
    * bins : Define the number of groups to categorize the data.
References:
    * Treemap Charts in Python: https://plotly.com/python/treemaps/
"""
def BTGpactual_imprimeTreemap(df, bins):
    df98 = calculaPercentil98(df)

    # Treemap simples
    fig1 = px.treemap(df98, path=["Ação"], values="Taxa %", color="Taxa %")
    fig1.show()

    # Treemap hierárquico

    # Cria grupos
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
Main - Onde tudo começa
"""
if "__main__" == __name__:

    driver = webdriver.Chrome()
    driver.set_window_position(2000, 0)
    driver.minimize_window()

    # Get BTC from BTG Pactual
    print("Web Scrapping: BTG Pactual")
    df_btcBTG = BTGpactual_getBTC(driver)
    BTGpactual_imprimeTreemap(df_btcBTG, bins=20)

    driver.quit()