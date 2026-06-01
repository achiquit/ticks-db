import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import geopandas as gpd
import numpy as np
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import no_plus_minus 

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
        hover_data={'year':False},
        text_auto='.2s'
    )

    fig.update_traces(
        marker_color=emerald,
        hovertemplate =
            '<b>Height: %{y}<sup>ft</sup></i>',
        textposition="outside"
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
    fig.add_annotation(
        x="2025-12-01",
        y=7000,
        text='<a href="/adventures/2026/potrero-chico/" target="_blank"><b>Potrero Trip</b></a>',
        showarrow=True,
        arrowhead=0,
        ax=-50,
        ay=0
    )
    fig.add_annotation(
        x="2024-12-01",
        y=9000,
        text='<a href="/adventures/2024/freeze-thaw/climbing-in-brazil/" target="_blank"><b>Rio Trip</b></a>',
        showarrow=True,
        arrowhead=0,
        ax=-50,
        ay=0
    )
    fig.add_annotation(
        x="2021-11-20",
        y=1000,
        text='<a href="/adventures/2021/pan-american-highway/" target="_blank"><b>Pan-American Trip</b></a>',
        showarrow=True,
        arrowhead=0,
        ax=70,
        ay=-60
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
    states_geojson = requests.get(
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_1_states_provinces_lines.geojson"
    ).json()

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
    fig = fig.add_trace(
        go.Scattergeo(
            lat=[
                v
                for sub in [
                    np.array(f["geometry"]["coordinates"])[:, 1].tolist() + [None]
                    for f in states_geojson["features"]
                ]
                for v in sub
            ],
            lon=[
                v
                for sub in [
                    np.array(f["geometry"]["coordinates"])[:, 0].tolist() + [None]
                    for f in states_geojson["features"]
                ]
                for v in sub
            ],
            line_color=dark_emerald,
            line_width=1,
            mode="lines",
            showlegend=False,
            hoverinfo='skip'
        )
    )
    fig.update_geos(
        resolution=50,
        scope='world',
        showcoastlines=True, coastlinecolor=dark_emerald,
        showcountries=True, countrycolor=dark_emerald,
        showsubunits=True, subunitcolor=dark_emerald,
        showlakes=True, lakecolor=dark_emerald,
        showland=True, landcolor=bg_black,
        showocean=True, oceancolor=bg_black,
        fitbounds="locations"
    )
    fig.update_layout(
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
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

def map_test() -> None:
    geo_df = gpd.read_file("data/climb-locs.csv")
    states_geojson = requests.get(
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_1_states_provinces_lines.geojson"
    ).json()

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
    fig = fig.add_trace(
        go.Scattergeo(
            lat=[
                v
                for sub in [
                    np.array(f["geometry"]["coordinates"])[:, 1].tolist() + [None]
                    for f in states_geojson["features"]
                ]
                for v in sub
            ],
            lon=[
                v
                for sub in [
                    np.array(f["geometry"]["coordinates"])[:, 0].tolist() + [None]
                    for f in states_geojson["features"]
                ]
                for v in sub
            ],
            line_color=dark_emerald,
            line_width=1,
            mode="lines",
            showlegend=False,
            hoverinfo='skip'
        )
    )
    fig.update_geos(
        resolution=50,
        scope='world',
        showcoastlines=True, coastlinecolor=dark_emerald,
        showcountries=True, countrycolor=dark_emerald,
        showsubunits=True, subunitcolor=dark_emerald,
        showlakes=True, lakecolor=dark_emerald,
        showland=True, landcolor=bg_black,
        showocean=True, oceancolor=bg_black,
        fitbounds="locations"
    )
    fig.update_layout(
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
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

def ticks_by_grade_mobile() -> None:
    no_plus_minus.magic()

    data = pd.read_csv("data/ticks-by-grade.csv")

    fig = px.bar(data,
                x="Grade",
                y="Count",
                color="Type",
                color_discrete_sequence=[trad_color, sport_color],
                hover_data={'Grade':False}
            )

    fig.update_layout(
        barmode='stack',
        xaxis={
            'categoryorder':'array',
            'categoryarray':['5.1','5.2','5.3','5.4','5.5','5.6','5.7','5.8','5.9','5.10a','5.10b','5.10c','5.10d','5.11a','5.11b','5.11c','5.11d','5.12a','5.12b','5.12c','5.12d','5.13a','5.13b','5.13c','5.13d','5.14a','5.14b','5.14c','5.14d','5.15a','5.15b','5.15c','5.15d']
        },
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="x unified"
    )
    config = {
        'displayModeBar': False
    }

    with open('../websitejazzhands/climbing/data/ticks-by-grade-mobile.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn', config=config))

def ticks_by_grade_desktop() -> None:
    no_plus_minus.magic()

    data = pd.read_csv("data/ticks-by-grade.csv")

    fig = px.bar(data,
                x="Grade",
                y="Count",
                color="Type",
                color_discrete_sequence=[trad_color, sport_color],
                hover_data={'Grade':False}
            )

    fig.update_layout(
        barmode='group',
        xaxis={
            'categoryorder':'array',
            'categoryarray':['5.1','5.2','5.3','5.4','5.5','5.6','5.7','5.8','5.9','5.10a','5.10b','5.10c','5.10d','5.11a','5.11b','5.11c','5.11d','5.12a','5.12b','5.12c','5.12d','5.13a','5.13b','5.13c','5.13d','5.14a','5.14b','5.14c','5.14d','5.15a','5.15b','5.15c','5.15d']
        },
        plot_bgcolor=bg_black,
        paper_bgcolor=bg_black,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="x unified"
    )
    config = {
        'displayModeBar': False
    }

    with open('../websitejazzhands/climbing/data/ticks-by-grade-desktop.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn', config=config))

yearly_height()
monthly_height()
overview()
map()
ticks_by_grade_mobile()
ticks_by_grade_desktop()