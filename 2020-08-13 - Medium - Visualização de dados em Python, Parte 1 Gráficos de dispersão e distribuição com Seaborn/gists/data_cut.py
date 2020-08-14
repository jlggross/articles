def calculaPercentil98(df):

    # Define os percentis para ver como os dados estão distribuídos
    description = df.describe(percentiles=[.25, .5, .75, .9, .95, .98, .99, .999])
    description_dict = description.to_dict()

    # Coleta o valor que delimita 98% das amostras no DataFrame
    data_cut = float(description_dict["Taxa %"]["98%"])

    # Seleciona apenas as amostras dentro do intervalo de 98%, removendo os outliers
    df98 = df[df["Taxa %"] <= data_cut]

    return df98

df = pd.read_excel("dadosBTC.xlsx", index_col=0)
df98 = calculaPercentil98(df)