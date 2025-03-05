import dash
from dash import dcc, html, callback
from dash import dcc
from dash import html
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import random
import datetime

dash.register_page(__name__, path='/', icon="bi bi-thermometer-half") # , path='/'

#layout = html.Div(
#    [
#        dcc.Markdown('# This will be the content of Page 1')
#    ]
#)

# -- Globale Variablen --
TEMP_HISTORY_1 = []  # Historische Temperaturdaten für Thermometer 1
TEMP_HISTORY_2 = []  # Historische Temperaturdaten für Thermometer 2
MAX_HISTORY_LENGTH = 20 # Maximale Anzahl an historischen Datenpunkten

# -- Hilfsfunktionen --
def randint(min=0,max=100):
    a = random.randint(min,max)
    return a

def create_line_chart(data, title):
    """Erstellt ein Liniendiagramm mit Plotly."""
    fig = go.Figure(data=[go.Scatter(x=[d['timestamp'] for d in data], y=[d['temperature'] for d in data], mode='lines+markers')])
    fig.update_layout(title=title, xaxis_title="Zeit", yaxis_title="Temperatur (°C)", autosize=False,
        width=445,
        height=300)
    return fig

# -- Layout der App --
layout = html.Div(
    id='app-container',
    style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh'},  # Horizontal und volle Höhe
    children=[
        # Erster Container (Temperatursensoren)
        html.Div(
            style={'width': '50%', 'padding': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'},
            children=[
                #html.H2("Temperatursensoren", style={'textAlign': 'center'}),
                html.Div( # Container für die Thermometer (nebeneinander)
                    style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around', 'width': '100%'},
                    children=[
                        html.Div( # Wrapper für Thermometer 1 und Modal
                            children=[
                                html.Button( # Button der wie ein Thermometer aussieht
                                    daq.Thermometer( # eigentliches Thermometer
                                        id='temp-thermometer-1',
                                        value=25,  # Startwert
                                        min=0,
                                        max=100,
                                        height=250, # Höhe des Thermometers
                                        showCurrentValue=True,
                                        units="°C",
                                        style={"color": "black"}
                                    ),
                                    id='thermometer-button-1', # ID für den Button
                                    n_clicks=0,
                                    style={ # Style damit der Button wie ein Thermometer aussieht
                                        'background': 'none',
                                        'border': 'none',
                                        'padding': '0',
                                        'margin': '0',
                                        'cursor': 'pointer', # Cursor-Stil ändern
                                    }
                                ),
                                dbc.Input( # Number Input Feld
                                    id='temp-threshold-1',
                                    type='number',
                                    value=35, # Startwert
                                    min=0,
                                    max=100,
                                    style={'marginTop': '10px', 'width': '100px'}
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalBody(dcc.Graph(id='temp-history-chart-1')),
                                    ],
                                    id="modal-1",
                                    is_open=False,
                                    #style={'maxHeight': '450px', 'overflowY': 'auto'}, # Beschränke die Höhe
                                ),
                            ]
                        ),
                        html.Div( # Wrapper für Thermometer 2 und Modal
                            children=[
                                html.Button( # Button der wie ein Thermometer aussieht
                                    daq.Thermometer( # eigentliches Thermometer
                                        id='temp-thermometer-2',
                                        value=30,  # Startwert
                                        min=0,
                                        max=100,
                                        height=250, # Höhe des Thermometers
                                        showCurrentValue=True,
                                        units="°C",
                                        style={"color": "black"}
                                    ),
                                    id='thermometer-button-2', # ID für den Button
                                    n_clicks=0,
                                    style={ # Style damit der Button wie ein Thermometer aussieht
                                        'background': 'none',
                                        'border': 'none',
                                        'padding': '0',
                                        'margin': '0',
                                        'cursor': 'pointer', # Cursor-Stil ändern
                                    }
                                ),
                                dbc.Input( # Number Input Feld
                                    id='temp-threshold-2',
                                    type='number',
                                    value=35, # Startwert
                                    min=0,
                                    max=100,
                                    style={'marginTop': '10px', 'width': '100px'}
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalBody(dcc.Graph(id='temp-history-chart-2')),
                                    ],
                                    id="modal-2",
                                    is_open=False,
                                    #style={'max-width': 'none', 'width': '750px'}, # Beschränke die Höhe
                                ),
                            ]
                        ),
                    ]
                ),
                dcc.Interval(  # Aktualisiert die Temperaturwerte regelmäßig
                    id='temp-interval',
                    interval=1000,  # Aktualisiert alle 3 Sekunden (3000 ms)
                    n_intervals=0
                )
            ]
        ),

        # Zweiter Container (Timer)
        html.Div(
            style={'width': '50%', 'padding': '20px'},
            children=[
                #html.H2("Timer", style={'textAlign': 'center'}),
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}, # Zentriert die Timer
                    children=[
                        # Timer 1
                        html.Div(
                            style={'marginBottom': '20px'},
                            children=[
                                html.H3("Timer 1", style={'display': 'flex', 'justify-content': 'center'}),
                                html.Div(id='timer-display-1', style={'fontSize': '2em', 'display': 'flex', 'justify-content': 'center'}),
                                html.Div(
                                    style={'display': 'flex', 'justifyContent': 'center'},
                                    children=[
                                        html.Button('+1', id='timer-1-add-1', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('+5', id='timer-1-add-5', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('-1', id='timer-1-sub-1', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('-5', id='timer-1-sub-5', n_clicks=0, style={'margin': '5px'}),
                                    ]
                                ),
                                html.Div(
                                    style={'display': 'flex', 'justifyContent': 'center'},
                                    children=[
                                        html.Button('Start', id='timer-1-start', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('Stop', id='timer-1-stop', n_clicks=0, style={'margin': '5px'}),
                                    ]
                                ),
                            ]
                        ),

                        # Timer 2
                        html.Div(
                            children=[
                                html.H3("Timer 2", style={'display': 'flex', 'justify-content': 'center'}),
                                html.Div(id='timer-display-2', style={'fontSize': '2em', 'display': 'flex', 'justify-content': 'center'}),
                                html.Div(
                                    style={'display': 'flex', 'justifyContent': 'center'},
                                    children=[
                                        html.Button('+1', id='timer-2-add-1', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('+5', id='timer-2-add-5', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('-1', id='timer-2-sub-1', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('-5', id='timer-2-sub-5', n_clicks=0, style={'margin': '5px'}),
                                    ]
                                ),
                                html.Div(
                                    style={'display': 'flex', 'justifyContent': 'center'},
                                    children=[
                                        html.Button('Start', id='timer-2-start', n_clicks=0, style={'margin': '5px'}),
                                        html.Button('Stop', id='timer-2-stop', n_clicks=0, style={'margin': '5px'}),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
                dcc.Interval(  # Aktualisiert die Timer-Anzeigen
                    id='timer-interval',
                    interval=1000,  # Aktualisiert jede Sekunde (1000 ms)
                    n_intervals=0,
                    disabled=True # Timer ist initial gestoppt
                ),
                dcc.Store(id='timer-1-value', data=0),  # Speichert den Timer-Wert in Sekunden
                dcc.Store(id='timer-2-value', data=0),
                dcc.Store(id='timer-1-running', data=False), # Speichert den Status des Timers (läuft oder nicht)
                dcc.Store(id='timer-2-running', data=False),
                dcc.Store(id='blinking', data=False)
            ]
        ),
        html.Button('Stop Blinking', id='stop-blinking', n_clicks=0, style={'display': 'none'})
    ]
)

# -- Callbacks --
#@callback(
#    Output('temp-thermometer-1', 'color'),
#    [Input('temp-thermometer-1', 'value')]
#)
#def update_therm_col(val):
#    if val >= 50:
#        return 'linear-gradient(red, yellow)'
#    elif val < 50:
#        return 'linear-gradient(green, yellow)'

#@callback(
#    Output('temp-thermometer-2', 'color'),
#    [Input('temp-thermometer-2', 'value')]
#)
#def update_therm_col(val):
#    if val >= 50:
#        return 'linear-gradient(green, yellow)'
#    elif val < 50:
#        return 'linear-gradient(red, yellow)'

# Temperatur-Thermometer-Update
@callback(
    [Output('temp-thermometer-1', 'value'),
     Output('temp-thermometer-2', 'value')],
    [Input('temp-interval', 'n_intervals')]
)
def update_temp_thermometers(n):
    """Aktualisiert die Thermometer mit simulierten Temperaturwerten und speichert die Historie."""
    global TEMP_HISTORY_1, TEMP_HISTORY_2

    temp1 = randint()
    temp2 = randint()
    #temp1 = random.randint(10, 40)  # Simulierter Temperaturwert
    #temp2 = random.randint(15, 45)

    # Speichern der historischen Daten (mit Zeitstempel)
    TEMP_HISTORY_1.append({'timestamp': datetime.datetime.now(), 'temperature': temp1})
    TEMP_HISTORY_2.append({'timestamp': datetime.datetime.now(), 'temperature': temp2})

    # Beschränken der Historie auf MAX_HISTORY_LENGTH
    TEMP_HISTORY_1 = TEMP_HISTORY_1[-MAX_HISTORY_LENGTH:]
    TEMP_HISTORY_2 = TEMP_HISTORY_2[-MAX_HISTORY_LENGTH:]

    return temp1, temp2

# Callbacks zum Öffnen/Schließen der Modals
@callback(
    Output("modal-1", "is_open"),
    [Input("thermometer-button-1", "n_clicks")],
    [State("modal-1", "is_open")],
)
def toggle_modal_1(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(
    Output("modal-2", "is_open"),
    [Input("thermometer-button-2", "n_clicks")],
    [State("modal-2", "is_open")],
)
def toggle_modal_2(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Callbacks zum Aktualisieren der Liniendiagramme in den Modals
@callback(
    Output('temp-history-chart-1', 'figure'),
    [Input('modal-1', 'is_open')],  # Auslösen, wenn das Modal geöffnet wird
    [State('temp-thermometer-1', 'value')]
)
def update_chart_1(is_open, current_temp):
    """Aktualisiert das Liniendiagramm für Thermometer 1."""
    if is_open:
        return create_line_chart(TEMP_HISTORY_1, "Historische Temperatur Sensor 1")
    return go.Figure() # Leeres Diagramm, wenn das Modal geschlossen ist

@callback(
    Output('temp-history-chart-2', 'figure'),
    [Input('modal-2', 'is_open')],  # Auslösen, wenn das Modal geöffnet wird
    [State('temp-thermometer-2', 'value')]
)
def update_chart_2(is_open, current_temp):
    """Aktualisiert das Liniendiagramm für Thermometer 2."""
    if is_open:
        return create_line_chart(TEMP_HISTORY_2,  "Historische Temperatur Sensor 2")
    return go.Figure() # Leeres Diagramm, wenn das Modal geschlossen ist


# Callback um die Farbe der Thermometer zu ändern
@callback(
    [Output('temp-thermometer-1', 'color'),
     Output('temp-thermometer-2', 'color')],
    [Input('temp-thermometer-1', 'value'),
     Input('temp-thermometer-2', 'value'),
     Input('temp-threshold-1', 'value'),
     Input('temp-threshold-2', 'value')]
)
def update_thermometer_color(temp1, temp2, threshold1, threshold2):
    """Ändert die Farbe der Thermometer, wenn die Temperatur den Schwellenwert erreicht."""
    #color1 = 'blue' if temp1 < threshold1 else 'red'
    #color2 = 'blue' if temp2 < threshold2 else 'red'

    if temp1 < threshold1 - 2:
        color1 = 'linear-gradient(yellow, blue)'
    elif temp1 > threshold1 + 2:
        color1 = 'linear-gradient(red, yellow)'
    else:
        color1 = 'linear-gradient(green, yellow)'

    if temp2 < threshold2 - 2:
        color2 = 'linear-gradient(yellow, blue)'
    elif temp2 > threshold2 + 2:
        color2 = 'linear-gradient(red, yellow)'
    else:
        color2 = 'linear-gradient(green, yellow)'

    return color1, color2

# Kombinierter Timer Callback
@callback(
    [Output('timer-1-value', 'data'),
     Output('timer-1-running', 'data'),
     Output('timer-2-value', 'data'),
     Output('timer-2-running', 'data'),
     Output('blinking','data')],
    [Input('timer-1-add-1', 'n_clicks'),
     Input('timer-1-add-5', 'n_clicks'),
     Input('timer-1-sub-1', 'n_clicks'),
     Input('timer-1-sub-5', 'n_clicks'),
     Input('timer-1-start', 'n_clicks'),
     Input('timer-1-stop', 'n_clicks'),
     Input('timer-2-add-1', 'n_clicks'),
     Input('timer-2-add-5', 'n_clicks'),
     Input('timer-2-sub-1', 'n_clicks'),
     Input('timer-2-sub-5', 'n_clicks'),
     Input('timer-2-start', 'n_clicks'),
     Input('timer-2-stop', 'n_clicks'),
     Input('timer-interval', 'n_intervals'),
     Input('stop-blinking','n_clicks')],
    [State('timer-1-value', 'data'),
     State('timer-1-running', 'data'),
     State('timer-2-value', 'data'),
     State('timer-2-running', 'data'),
     State('blinking', 'data')]
)
def update_timers(t1_add_1, t1_add_5, t1_sub_1, t1_sub_5, t1_start, t1_stop,
                   t2_add_1, t2_add_5, t2_sub_1, t2_sub_5, t2_start, t2_stop,
                   n_intervals, stop_blinking,
                   t1_current_value, t1_timer_running,
                   t2_current_value, t2_timer_running, blinking):
    """Aktualisiert alle Timer-Werte und -Status basierend auf Button-Klicks UND Interval."""
    ctx = dash.callback_context
    if not ctx.triggered:
        return t1_current_value, t1_timer_running, t2_current_value, t2_timer_running

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'timer-interval':
        # Timer-Logik für das Interval
        if t1_timer_running:
            if t1_current_value > 0:
                t1_current_value = t1_current_value - 1
            else:
                t1_current_value = 0
                t1_timer_running = False  # Timer 1 stoppt
                blinking = True

        if t2_timer_running:
            if t2_current_value > 0:
                t2_current_value = t2_current_value - 1
            else:
                t2_current_value = 0
                t2_timer_running = False  # Timer 2 stoppt
                blinking = True

    elif triggered_id == 'timer-1-add-1':
        t1_current_value = max(0, t1_current_value + 3)
    elif triggered_id == 'timer-1-add-5':
        t1_current_value = max(0, t1_current_value + 300)
    elif triggered_id == 'timer-1-sub-1':
        t1_current_value = max(0, t1_current_value - 60)
    elif triggered_id == 'timer-1-sub-5':
        t1_current_value = max(0, t1_current_value - 300)
    elif triggered_id == 'timer-1-start':
        t1_timer_running = True
    elif triggered_id == 'timer-1-stop':
        t1_timer_running = False
    elif triggered_id == 'stop-blinking':
        blinking = False

    elif triggered_id == 'timer-2-add-1':
        t2_current_value = max(0, t2_current_value + 60)
    elif triggered_id == 'timer-2-add-5':
        t2_current_value = max(0, t2_current_value + 300)
    elif triggered_id == 'timer-2-sub-1':
        t2_current_value = max(0, t2_current_value - 60)
    elif triggered_id == 'timer-2-sub-5':
        t2_current_value = max(0, t2_current_value - 300)
    elif triggered_id == 'timer-2-start':
        t2_timer_running = True
    elif triggered_id == 'timer-2-stop':
        t2_timer_running = False
    elif triggered_id == 'stop-blinking':
        blinking = False

    return t1_current_value, t1_timer_running, t2_current_value, t2_timer_running, blinking


# Timer Interval Steuerung
@callback(
    Output('timer-interval', 'disabled'),
    [Input('timer-1-running', 'data'),
     Input('timer-2-running', 'data')]
)
def enable_disable_interval(timer1_running, timer2_running):
  """Aktiviert oder Deaktiviert das Interval, wenn einer der Timer läuft."""
  return not (timer1_running or timer2_running) # Interval ist disabled, wenn KEIN Timer läuft

# Timer 1 Update
@callback(
    Output('timer-display-1', 'children'),
    Input('timer-1-value', 'data')
)
def update_timer_display_1(timer_value):
    """Aktualisiert die Anzeige von Timer 1."""
    minutes, seconds = divmod(timer_value, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"

# Timer 2 Update
@callback(
    Output('timer-display-2', 'children'),
    Input('timer-2-value', 'data')
)
def update_timer_display_2(timer_value):
    """Aktualisiert die Anzeige von Timer 2."""
    minutes, seconds = divmod(timer_value, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"

# Blinker Callback
@callback(
    Output('app-container', 'className'),
    Input('blinking', 'data')
)
def toggle_blinking(blinking):
    """Fügt die 'blink' Klasse dem Hauptcontainer hinzu oder entfernt sie"""
    if blinking:
        return 'blink'
    else:
        return ''

# Callback um den Button ein- oder auszublenden
@callback(
    Output('stop-blinking', 'style'),
    [Input('blinking', 'data')]
)
def show_hide_button(blinking):
    """Zeigt den Stop-Button nur dann an, wenn 'blinking' True ist."""
    if blinking:
        return {'display': 'block'}  # Zeige den Button
    else:
        return {'display': 'none'}  # Verstecke den Button

