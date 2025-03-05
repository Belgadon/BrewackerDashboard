import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__, icon="bi bi-pass")

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 3'),
        dcc.Checklist(
            ['Important first step', 'Important second step', 'Are we done yet?', 'Haven\'t we done this already?', 'There is more?', 'Done! Finally!', 'Cheers! :-)'],
            ['Important first step', 'Important second step']
)
    ]
)
