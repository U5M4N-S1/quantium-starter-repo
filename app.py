import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Load and prepare the data
df = pd.read_csv("formatted_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Create the Dash app
app = Dash(__name__)

# --- Styles ---
COLORS = {
    "background": "#FFF0F5",   # soft pink background
    "panel": "#FFFFFF",
    "accent": "#E91E63",       # pink morsel vibes
    "text": "#2C2C2C",
    "muted": "#6B6B6B",
}

app_style = {
    "fontFamily": "'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    "backgroundColor": COLORS["background"],
    "minHeight": "100vh",
    "padding": "40px 20px",
}

card_style = {
    "backgroundColor": COLORS["panel"],
    "maxWidth": "1100px",
    "margin": "0 auto",
    "padding": "30px 40px",
    "borderRadius": "16px",
    "boxShadow": "0 10px 30px rgba(233, 30, 99, 0.15)",
}

header_style = {
    "textAlign": "center",
    "color": COLORS["accent"],
    "fontSize": "36px",
    "fontWeight": "700",
    "marginBottom": "8px",
    "letterSpacing": "0.5px",
}

subheader_style = {
    "textAlign": "center",
    "color": COLORS["muted"],
    "fontSize": "16px",
    "marginBottom": "30px",
    "fontWeight": "400",
}

filter_label_style = {
    "fontWeight": "600",
    "color": COLORS["text"],
    "marginBottom": "10px",
    "fontSize": "15px",
}

radio_style = {
    "display": "flex",
    "gap": "20px",
    "justifyContent": "center",
    "flexWrap": "wrap",
    "marginBottom": "25px",
}

radio_label_style = {
    "padding": "8px 16px",
    "marginRight": "6px",
    "color": COLORS["text"],
    "fontSize": "15px",
    "cursor": "pointer",
    "textTransform": "capitalize",
}

# --- Layout ---
app.layout = html.Div(
    style=app_style,
    children=[
        html.Div(
            style=card_style,
            children=[
                html.H1("Soul Foods — Pink Morsel Sales Visualiser", style=header_style),
                html.P(
                    "Explore sales trends before and after the price increase on 15 January 2021",
                    style=subheader_style,
                ),
                html.Div(
                    children=[
                        html.Div("Filter by region:", style=filter_label_style),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                                {"label": "All", "value": "all"},
                            ],
                            value="all",
                            style=radio_style,
                            labelStyle=radio_label_style,
                            inputStyle={"marginRight": "6px"},
                        ),
                    ]
                ),
                dcc.Graph(id="sales-line-chart"),
            ],
        ),
    ],
)

# --- Callback ---
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered = df.copy()
        # Aggregate across all regions per day
        filtered = filtered.groupby("date", as_index=False)["sales"].sum()
        fig = px.line(
            filtered,
            x="date",
            y="sales",
            title=f"Pink Morsel Sales — All Regions",
            labels={"date": "Date", "sales": "Sales ($)"},
        )
    else:
        filtered = df[df["region"] == selected_region]
        filtered = filtered.groupby("date", as_index=False)["sales"].sum()
        fig = px.line(
            filtered,
            x="date",
            y="sales",
            title=f"Pink Morsel Sales — {selected_region.capitalize()} Region",
            labels={"date": "Date", "sales": "Sales ($)"},
        )

    # Styling the figure
    fig.update_traces(line=dict(color=COLORS["accent"], width=2.5))
    fig.update_layout(
        plot_bgcolor="#FAFAFA",
        paper_bgcolor=COLORS["panel"],
        font=dict(family="Segoe UI, sans-serif", color=COLORS["text"]),
        title=dict(font=dict(size=20, color=COLORS["text"]), x=0.5),
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis=dict(showgrid=True, gridcolor="#EEEEEE"),
        yaxis=dict(showgrid=True, gridcolor="#EEEEEE"),
    )

    # Vertical line marking the price increase
    fig.add_vline(
        x=pd.Timestamp("2021-01-15").timestamp() * 1000,
        line_dash="dash",
        line_color=COLORS["accent"],
        annotation_text="Price increase",
        annotation_position="top right",
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)