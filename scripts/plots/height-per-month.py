import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_dark"

data = pd.read_csv("data/outputs/yearly-height.csv")

# Create the bar plot
fig = px.bar(
    data_frame=data, 
    x="year", 
    y="height"
)

fig.update_traces(
    marker_color='#00d492'
)
fig.update_layout(
    plot_bgcolor='#030712',
    paper_bgcolor='#030712',
    margin=dict(l=0, r=0, t=0, b=0)
)
fig.update_yaxes(
    tickformat=",.2d", #Change how the numbers are rounded & written
    nticks=12,
    title=None,
    gridcolor='#007a55',
    tickangle=315,
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

with open('../websitejazzhands/climbing/data/plotly_graph_test.html', 'w') as f:
    f.write(fig.to_html(include_plotlyjs='cdn', config=config))