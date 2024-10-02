import matplotlib.pyplot as plt # Importa Matplotlib para gerar gráficos
import pandas as pd # Importa Pandas para manipulação de dados
import seaborn as sns # Importa Seaborn para visualização de dados
from pandas.plotting import register_matplotlib_converters # Registra conversores para datas no Matplotlib

register_matplotlib_converters() # Ativa os conversores para manipulação de datas

# Importando os dados do arquivo CSV e definindo a coluna 'date' como índice
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Limpeza dos dados para manter apenas os valores entre o 2.5º e 97.5º 
df = df[df["value"].between(df["value"].quantile(0.025), df["value"].quantile(0.975))]

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] # Lista de nomes dos meses para uso nos gráficos

# Função para gerar um gráfico de linhas
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5)) # Cria a figura e o eixo para o gráfico de linhas, definindo o tamanho da figura
    sns.lineplot(data=df, x=df.index, y='value', ax=ax) # Plota os dados do dataframe como um gráfico de linhas
    ax.set(title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019', xlabel="Date", ylabel="Page Views")  # Define o título e os rótulos dos eixos do gráfico
    fig.savefig('line_plot.png')  # Salva o gráfico em um arquivo PNG
    return fig

# Função para gerar um gráfico de barras
def draw_bar_plot():
    # Cria uma cópia do dataframe e adiciona colunas 'year' (ano) e 'month' (nome do mês)
    df_bar = df.copy() 
    df_bar['year'] = df_bar.index.year 
    df_bar['month'] = df_bar.index.month_name() 
    
    # Agrupa os dados por ano e mês, calculando a média dos valores para cada grupo
    df_bar = df_bar.groupby(['year', 'month']).mean().reset_index()
    # Cria a figura e o eixo para o gráfico de barras, definindo o tamanho da figura
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(x='year', y='value', hue='month', data=df_bar, hue_order=months, ci=None, ax=ax)  # Cria o gráfico de barras usando os anos e as médias mensais
    ax.set(xlabel="Years", ylabel="Average Page Views") # Define os rótulos dos eixos do gráfico
    fig.savefig('bar_plot.png') # Salva o gráfico em um arquivo PNG
    return fig

# Função para gerar gráficos de boxplot
def draw_box_plot():
    # Cria uma cópia do dataframe e reseta o índice para trabalhar com a coluna 'date' como uma coluna comum
    df_box = df.copy() 
    df_box.reset_index(inplace=True) 
    # Adiciona colunas 'year' (ano) e 'month' (mês abreviado) ao dataframe
    df_box['year'] = df_box['date'].dt.year 
    df_box['month'] = df_box['date'].dt.strftime('%b') 

    # Adiciona uma coluna 'monthnumber' para facilitar a ordenação dos meses em ordem cronológica
    df_box['monthnumber'] = df_box['date'].dt.month
    df_box = df_box.sort_values('monthnumber')

    # Cria a figura e dois eixos para os gráficos de boxplot, definindo o tamanho da figura
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    # Cria o boxplot para visualizar a variação de 'value' ao longo dos anos
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set(title="Year-wise Box Plot (Trend)", xlabel="Year", ylabel="Page Views")

    # Cria o boxplot para visualizar a variação de 'value' ao longo dos meses
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1])
    ax[1].set(title="Month-wise Box Plot (Seasonality)", xlabel="Month", ylabel="Page Views")

    # Salva a figura com os gráficos de boxplot em um arquivo PNG
    fig.savefig('box_plot.png')
    return fig
