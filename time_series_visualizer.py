import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    plt.plot(df.index, 'value', data=df)
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby([df.index.year.rename('Years'), df.index.month.rename('Months')])['value'].mean()

    # Rename months properly and unstack for plotting
    new_index = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar.index = df_bar.index.set_levels(new_index, level=1)
    df_bar = df_bar.unstack()

    # Draw bar plot
    ax = df_bar.plot(kind='bar')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    fig = ax.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2)
    sns.boxplot(data=df_box, x='year', y='value', ax=ax[0])
  
    df_box['month-idx'] = df_box['date'].dt.month
    df_box.sort_values(by='month-idx', inplace=True)
    sns.boxplot(data=df_box, x='month', y='value', ax=ax[1])
  
    fig.set_figwidth(15)

# Titles and labels
    for a in ax:
      a.title.set_text('Year-wise Box Plot (Trend)') if a == ax[0] else a.title.set_text('Month-wise Box Plot (Seasonality)')
      a.set_xlabel('Year') if a == ax[0] else a.set_xlabel('Month')
      a.set_ylabel('Page Views')

    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
