import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.templates["my_styles"] = go.layout.Template(
    layout=go.Layout(
        'bgcolor': 'white'
    )
)
pio.templates.default = "plotly+my_styles"

data = pd.read_csv("data/outputs/yearly-height.csv")

# Create the bar plot
fig = px.bar(data_frame=data, 
             x="year", 
             y="height")
# fig.update_traces(marker_color='#00d492')

fig.show()

with open('../websitejazzhands/climbing/data/plotly_graph_test.html', 'w') as f:
    f.write(fig.to_html(include_plotlyjs='cdn'))