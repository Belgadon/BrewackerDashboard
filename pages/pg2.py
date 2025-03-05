import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, icon="bi bi-info-circle")

layout = html.Div(
    [
        dcc.Markdown('# Recipe'),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.Article([
                            html.H1("Get all the good ingredients."),
                            html.Article(
                                [html.H2("Malt"),
                                html.P("Pure and clean."),
                                 ], className="ingredient"
                            ),
                            html.Article(
                                [html.H2("Hops"),
                                html.P("Best of the best."),
                                 ], className="ingredient"
                            ),
                            html.Article(
                                [html.H2("Water"),
                                html.P("Soak that stuff!"),
                                 ], className="ingredient"
                            )
                        ], className="ingredients",
                        ),
                    ],
                    title="Step 1",
                ),
                dbc.AccordionItem(
                    [
                        html.P("Brew a delicious beer.")],
                    title="Step 2",
                ),
                dbc.AccordionItem(
                    [html.P("Don't forget to taste. :-)")],
                    title="Step 3",
                ),
            ],
        )
    ]
)
