import plotly.express as px
import pandas as pd
import plotly.io as pio
from datetime import datetime
from dateutil.relativedelta import relativedelta 

pio.templates.default = "plotly_dark"

def yearly_height() -> None:

    data = pd.read_csv("data/yearly-height.csv")

    # Create the bar plot
    fig = px.bar(
        data_frame=data, 
        x="year", 
        y="height",
        hover_data={'year':False}
    )

    fig.update_traces(
        marker_color='#00d492',
        hovertemplate =
            '<b>Height: %{y}<sup>ft</sup></i>'
    )
    fig.update_layout(
        plot_bgcolor='#030712',
        paper_bgcolor='#030712',
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="x unified",
        xaxis=dict(
            unifiedhovertitle=dict(
                text='<b>%{x|%Y}</b>'
            )
        )
    )
    fig.update_yaxes(
        tickformat=",.2d", #Change how the numbers are rounded & written
        nticks=12,
        title=None,
        gridcolor='#007a55',
        # tickangle=315,
        tickfont=dict(family='Arial', color='white', size=12),
        ticklabelstandoff=6
    )
    fig.update_xaxes(
        title=None,
        ticklabelstandoff=6,
        nticks=12,
        tickfont=dict(family='Arial', color='white', size=12)
    )
    config = {'displayModeBar': False}

    with open('../websitejazzhands/climbing/data/yearly-height.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn', config=config))

def monthly_height() -> None:
    data = pd.read_csv("data/monthly-height.csv")
    end_date = datetime.today()
    start_date = end_date - relativedelta(months=60)

    # Create the bar plot
    fig = px.bar(
        data_frame=data, 
        x="month", 
        y="height"
    )

    fig.update_traces(
        marker_color='#00d492',
        hovertemplate =
            '<b>Height: %{y}<sup>ft</sup></i>'
    )
    fig.update_layout(
        plot_bgcolor='#030712',
        paper_bgcolor='#030712',
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="x unified",
        xaxis=dict(
            unifiedhovertitle=dict(
                text='<b>%{x|%B %Y}</b>'
            )
        ),
        xaxis_tickformat = "%b '%y"
    )
    fig.update_yaxes(
        tickformat=",.2d", #Change how the numbers are rounded & written
        nticks=6,
        title=None,
        gridcolor='#007a55',
        # tickangle=315,
        tickfont=dict(family='Arial', color='white', size=12),
        ticklabelstandoff=6
    )
    fig.update_xaxes(
        type="date",
        title=None,
        ticklabelstandoff=6,
        tickangle=45,
        nticks=32,
        tickfont=dict(family='Arial', color='white', size=10),
        rangeslider_visible=True,
        range=[start_date, end_date]
    )
    config = {'displayModeBar': False}

    with open('../websitejazzhands/climbing/data/monthly-height.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn', config=config))

# def overview() -> None:


yearly_height()
monthly_height()