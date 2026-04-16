import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Load the processed data from the previous task
df = pd.read_csv("formatted_data.csv")

# Make sure the date column is a proper datetime, then sort by date
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Build the line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales ($)"},
)

# Add a vertical line marking the price increase date
fig.add_vline(
    x=pd.Timestamp("2021-01-15").timestamp() * 1000,
    line_dash="dash",
    line_color="red",
    annotation_text="Price increase",
    annotation_position="top right",
)
# Create the Dash app
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "Soul Foods — Pink Morsel Sales Visualiser",
            style={"textAlign": "center"},
        ),
        dcc.Graph(id="sales-line-chart", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)