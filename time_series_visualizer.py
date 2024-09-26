import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Importando os dados e fazendo o parsing das datas, com a coluna 'date' como índice
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Limpeza dos dados, mantendo valores entre o 2.5º e o 97.5º percentil
df = df[df["value"].between(df["value"].quantile(0.025), df["value"].quantile(0.975))]

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.lineplot(data=df, x=df.index, y='value', ax=ax)
    ax.set(title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019', xlabel="Date", ylabel="Page Views")
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Agrupando os dados por ano e mês, calculando a média
    df_bar = df_bar.groupby(['year', 'month']).mean().reset_index()

    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(x='year', y='value', hue='month', data=df_bar, hue_order=months, ci=None, ax=ax)
    ax.set(xlabel="Years", ylabel="Average Page Views")
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Ordenando os meses no formato de três letras
    df_box['monthnumber'] = df_box['date'].dt.month
    df_box = df_box.sort_values('monthnumber')

    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    # Boxplot por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set(title="Year-wise Box Plot (Trend)", xlabel="Year", ylabel="Page Views")

    # Boxplot por mês
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1])
    ax[1].set(title="Month-wise Box Plot (Seasonality)", xlabel="Month", ylabel="Page Views")

    fig.savefig('box_plot.png')
    return fig
