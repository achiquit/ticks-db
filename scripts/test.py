import pandas as pd
import numpy as np
from plotly_calplot import calplot
from datetime import datetime
import csv

start_date = "2019-06-15"
end_date = datetime.today().strftime("%Y-%m-%d")
# date range from start date to end date and random
# column named value using amount of days as shape
df = pd.DataFrame({
    "date": pd.date_range(start_date, end_date),
    "height": 0
})

with open('data/height-by-date.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)

    values = list(csv_reader)

values.pop(0)

for value in values:
    # value[0] = datetime.strptime(value[0], "%Y-%m-%d").date()
    value[1] = int(value[1])

    df['height'] = np.where(df['date'] == value[0], df['height'] + value[1], df['height'] + 0)

# creating the plot
fig = calplot(
    df,
    x="date",
    y="height",
    dark_theme=True
)
fig.show()