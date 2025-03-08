import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], use_pages=True)

server = app.server

# Viewport Meta Tag für Auflösung
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="viewport" content="width=800, height=480, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "2rem",
    "padding": "1px",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    #"padding": "2rem 1rem",
    "background-image": "url('/assets/hop.jpg')",
    "background-repeat": "no-repeat",
    "background-attachment": "fixed",
    "background-position": "center",
    "background-size": "350px 350px",

}

sidebar = html.Div([
        dbc.Nav(
            [
            dbc.NavLink(html.I(className=page["icon"]), href=page["relative_path"], active="exact")
            for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            justified=True,
            card=True,
            fill=True,
            navbar=True
        )
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([sidebar, dash.page_container], style=CONTENT_STYLE)

if __name__ == "__main__":
    app.run_server(port=8888)