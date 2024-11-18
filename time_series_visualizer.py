import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
from pandas.plotting import register_matplotlib_converters

# Temporarily patch np.float to np.float64 to avoid the AttributeError
np.float = float  # Patch np.float to avoid deprecation issues in seaborn

register_matplotlib_converters()

# 1 - Use Pandas to import the data from "fcc-forum-pageviews.csv". Set the index to the date column.
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# 2 - Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.
lower_percentile = df['value'].quantile(0.025)
upper_percentile = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_percentile) & (df['value'] <= upper_percentile)]

# 3 - Create a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png".
#  The title should be Daily freeCodeCamp Forum Page Views 5/2016-12/2019.
#  The label on the x axis should be Date and the label on the y axis should be Page Views.
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red', lw=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.grid(True)

    fig.savefig('line_plot.png')
    return fig

# 4 - Create a draw_bar_plot function that draws a bar chart similar to "examples/Figure_2.png".
#  It should show average daily page views for each month grouped by year.
#  The legend should show month labels and have a title of Months.
#  On the chart, the label on the x axis should be Years and the label on the y axis should be Average Page Views.
def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    monthly_avg = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    fig, ax = plt.subplots(figsize=(12, 6))

    monthly_avg.plot(kind='bar', ax=ax, width=0.8)

    ax.set_title('Average Daily Page Views by Year and Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Set legend labels and title for months.
    ax.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    plt.xticks(rotation=45)

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

# 5 - Create a draw_box_plot function that uses Seaborn to draw two adjacent box plots similar to "examples/Figure_3.png".
#  These box plots should show how the values are distributed within a given year or month and how it compares over time.
#  The title of the first chart should be Year-wise Box Plot (Trend) and the title of the second chart should be Month-wise Box Plot (Seasonality).
#  Make sure the month labels on bottom start at Jan and the x and y axis are labeled correctly.
#  The boilerplate includes commands to prepare the data.

def draw_box_plot():
        # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Month abbreviated
    
    # Convert 'value' column to native Python float
    df_box['value'] = df_box['value'].astype(int)
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
