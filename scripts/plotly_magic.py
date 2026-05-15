import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import geopandas as gpd
from datetime import datetime
from dateutil.relativedelta import relativedelta 

pio.templates.default = "plotly_dark"
emerald = '#00d492'
dark_emerald = '#007a55'
bg_black = '#030712'
trad_color = '#fb2c36'
sport_color = '#00a6f4'
boulder_color = '#e12afb'
tr_color = '#fd9a00'
wi_color = '#615fff'
ai_color = '#ad46ff'
scramble_color = '#9ae600'
snow_color = '#f8fafc'
aid_color = '#a50036'
via_color = '#9f2d00'
tradaid_color = '#ffd230'
tradsnow_color = '#53eafd'

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
        marker_color=emerald,
        hovertemplate =
            '<b>Height: %{y}<sup>ft</sup></i>'
    )
    fig.update_layout(
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
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
        gridcolor=dark_emerald,
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
        marker_color=emerald,
        hovertemplate =
            '<b>Height: %{y}<sup>ft</sup></i>'
    )
    fig.update_layout(
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
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
        gridcolor=dark_emerald,
        # tickangle=315,
        tickfont=dict(family='Arial', color='white', size=12),
        ticklabelstandoff=6
    )
    fig.update_xaxes(
        type="date",
        title=None,
        ticklabelstandoff=6,
        tickangle=45,
        nticks=28,
        tickfont=dict(family='Arial', color='white', size=10),
        rangeslider_visible=True,
        range=[start_date, end_date]
    )
    config = {'displayModeBar': False}

    with open('../websitejazzhands/climbing/data/monthly-height.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn', config=config))

def overview() -> None:
    data = pd.read_csv("data/overview-stats.csv")

    headerColor='#1e2939'
    evenColor='#080f1e'
    oddColor=bg_black

    fig = go.Figure(
        data=[go.Table(
            header=dict(
                values=['<b>Timeframe</b>','<b>Days Climbed</b>','<b>Ticks Made</b>','<b>Pitches Climbed</b>','<b>Feet Climbed</b>','<b>Partners</b>','<b>Climbs</b>','<b>Areas</b>','<b>Countries</b>','<b>States</b>'],
                align='center',
                fill_color=headerColor
            ),
            cells=dict(
                values=data.transpose().values.tolist(),
                align='center',
                font_size=14,
                height=30,
                fill_color = [[oddColor,evenColor,oddColor, evenColor,oddColor]*5]
            )
        )
    ])

    fig.update_layout(
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    config = {'displayModeBar': False}

    with open('../websitejazzhands/climbing/data/overview-stats.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn', config=config))

def map() -> None:
    geo_df = gpd.read_file("data/climb-locs.csv")

    fig = px.scatter_geo(geo_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Area",
        hover_data=dict(
            Latitude=False,
            Longitude=False,
            Climb=True,
            Difficulty=True,
            Type=True
        ),
        color='Type',
        color_discrete_map=dict(
            Trad=trad_color,
            Sport=sport_color,
            Boulder=boulder_color,
            TR=tr_color,
            Scramble=scramble_color,
            Snow=snow_color,
            Aid=aid_color,
            Via=via_color
        )
    )
    fig.update_geos(
        resolution=50,
        showcoastlines=True, coastlinecolor=dark_emerald,
        showcountries=True, countrycolor=dark_emerald,
        showland=True, landcolor=bg_black,
        showocean=True, oceancolor=bg_black,
        fitbounds="locations"
    )
    fig.update_layout(
        plot_bgcolor='#030712',
        paper_bgcolor="#030712",
        margin=dict(l=0, r=0, t=0, b=0)
    )
    config = {
        'scrollZoom': True,
        'displaylogo': False,
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['select', 'lasso', 'pan', 'toImage']
    }

    with open('../websitejazzhands/climbing/data/climb-locs.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn', config=config))


yearly_height()
monthly_height()
overview()
map()