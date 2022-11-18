import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm
import pandas as pd
import numpy as np
import datetime
from html_utils import *

def get_ols_plot(X, Y, observations, station_name):


    df_linear = pd.DataFrame({'Reported_NOx': X, 'Calculated_NOx':Y})

    #Ploting the graph
    fig = px.scatter(df_linear, x="Reported_NOx", y="Calculated_NOx", trendline="ols")
    fig.update_traces(name = "OLS trendline")



    fig.update_layout(template="ggplot2",title_text = '<b>Linear Regression Model</b>',
                      font=dict(family="Arial, Balto, Courier New, Droid Sans",color='black'), showlegend=True)
    fig.update_layout(
        legend=dict(
            x=0.01,
            y=.98,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="Black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="dimgray",
            borderwidth=2
        ))

    # retrieve model estimates
    model = px.get_trendline_results(fig)
    alpha = model.iloc[0]["px_fit_results"].params[0]
    beta = model.iloc[0]["px_fit_results"].params[1]

    # restyle figure
    fig.data[0].name = observations
    fig.data[0].showlegend = True
    fig.data[1].name = fig.data[1].name  + ' y = ' + str(round(alpha, 2)) + ' + ' + str(round(beta, 2)) + 'x'
    fig.data[1].showlegend = True

    # addition for r-squared
    rsq = model.iloc[0]["px_fit_results"].rsquared
    fig.add_trace(go.Scatter(x=[100], y=[100],
                             name = "R-squared" + ' = ' + str(round(rsq, 2)),
                             showlegend=True,
                             mode='markers',
                             marker=dict(color='rgba(0,0,0,0)')
                             ))

    figures_to_html_app([fig], station_name+ '.html')

    return rsq, alpha, beta
def return_mean(df, col, station_name, st_no):
    return [df[col + '_clean_c'].mean(), df[col].mean(), col, station_name, st_no]
