from re import L
from shutil import move
import dash
import requests, json
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
#from sklearn.metrics import coverage_error
from flask_login import current_user
from app import strings
import time


from .server_calls import get_coverages_by_user, get_signals_by_region, get_regions_by_coverage, get_arrivalPieChart, get_movementBarChart, get_peakScatterPlot, get_splitPieChart, get_totalDelayChart

base_url = "/dash/app/"


def init_dashboard(server):
    dash_app = dash.Dash(__name__,server=server,routes_pathname_prefix=base_url,external_stylesheets=['/css/bootstrap.css'])
    print("== init current user:", current_user)
    # This defines the app layout
    dash_app.layout = html.Div([
        dcc.Location(id="url"),
        dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1")
        ),
        html.Div(id='dashboard-wrapper')
    ])
    # Eliminate callback errors for dynamic elements
    dash_app.config.suppress_callback_exceptions=True

    init(dash_app)
    return dash_app.server


import random
def rand_opt(fake):
    o = []
    for i in range(0, 1000):
        if i % int(fake) == 0:
            o.append({"label": i , "value": i })

    return o

##############
# App Layout #
##############


def set_layout():
    coverage = []
    print("-- setting layout", flush=True)

    print("== layout current user:", current_user)
    print("= Coverages", coverage, flush=True)
    coverage = get_coverages_by_user();
    print("= Coverages", coverage, flush=True)

    content = html.Div(id="dash-wrapper", className="container-fluid", children=[
                # Identifier
                html.Div(className="dash-wrapper__fields row",children=[
                    html.Div( className="col-12", children=[
                        html.H1('Coverage : Region : Signal')
                    ])
                ]),
                # Zone
                html.Div(className="dash-wrapper__fields row",children=[
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Coverage'),
                        dcc.Dropdown(
                            id='coverage',
                            options = coverage
                        )
                    ]),
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Region'),
                        dcc.Dropdown(
                            id='region',
                            options = []
                        )
                    ]),
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Signal'),
                        dcc.Dropdown(
                            id='signal',
                            options = []
                        )
                    ])
                ]),
                # Details
                html.Div(className="dash-wrapper__fields-detail row",children=[
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Day'),
                        dcc.Dropdown(
                            id='day',
                            options = [{'label': 'Sunday', 'value': 1},
                                {'label': 'Monday', 'value': 2},
                                {'label': 'Tuesday', 'value': 3},
                                {'label': 'Wednesday', 'value': 4},
                                {'label': 'Thursday', 'value': 5},
                                {'label': 'Friday', 'value': 6},
                                {'label': 'Saturday', 'value': 7},
                            ],
                            value='2'
                        )
                    ]),
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Approach'),
                        dcc.Dropdown(
                            id='approach',
                            options=[{'label': 'ALL', 'value': 'ALL'},
                                {'label': 'Northbound', 'value': 'Northbound'},
                                {'label': 'Eastbound', 'value': 'Eastbound'},
                                {'label': 'Southbound', 'value': 'Southbound'},
                                {'label': 'Westbound', 'value': 'Westbound'},
                            ],
                            value='ALL'
                        )
                    ]),
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Travel Direction'),
                        dcc.Dropdown(
                            id='direction',
                            options=[{'label': 'ALL', 'value': 'ALL'},
                                {'label': 'Straight', 'value': 'Straight'},
                                {'label': 'Left', 'value': 'Left'},
                                {'label': 'Right', 'value': 'Right'},
                            ],
                            value='ALL'
                        )
                    ])
                ]),

                # Pies
                html.Div(className="dash-wrapper__pie row",children=[
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Total Delay'),
                        html.Div(id="dash-wrapper__pie--delay", children=[
                            dcc.Graph(id="dash-wrapper__pie--delay-chart"),
                        ]),
                    ]),
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Arrival Rates'),
                        html.Div(id="dash-wrapper__pie--arrival", children=[
                            dcc.Graph(id="dash-wrapper__pie--arrival-chart"),
                        ]),
                    ]),
                    html.Div( className="col-12 col-md-6 col-xl-4", children=[
                        html.H1('Split Failure'),
                        html.Div(id="dash-wrapper__pie--splitfail", children=[
                            dcc.Graph(id="dash-wrapper__pie--splitfail-chart"),
                        ]),
                    ])
                ]),
                # Movement
                html.Div(className="dash-wrapper__bar row",children=[
                    html.Div( className="col-12", children=[
                        html.H1('Movement'),
                        html.Div(id="dash-wrapper__bar--movement", children=[
                            dcc.Graph(id="dash-wrapper__bar--movement-chart"),
                        ]),
                    ]),
                # Delay
                html.Div(className="dash-wrapper__scatter row",children=[
                    html.Div( className="col", children=[
                        html.H1('Delay by Hour'),
                        html.Div(id="dash-wrapper__scatter", children=[
                            dcc.Graph(id="dash-wrapper__scatter--delay-chart"),
                        ]),
                    ]),
                ]),
            ]),
        ])
    return content

# Field callbacks are automatically called once
def init(app):
    # Load Regions for the User
    coverage = []
    region = []
    signal = []
    day = []

    print("== app current user:", current_user)

    # If authorized, load dash elements
    @app.callback(
        Output(component_id='dashboard-wrapper', component_property='children'),
        Input('url', 'pathname')
    )
    def page(url):
        print("- page callback", flush=True)
        return set_layout()

    @app.callback(
        Output(component_id='region', component_property='options'),
        Input(component_id='coverage', component_property='value')

    )
    # Update Regions
    def cb_coverage(input):
        coverage = []
        print("== cb_coverage current user:", current_user)


        region = []
        if dash.callback_context.triggered[0]['prop_id'].split('.')[0] == "coverage":
            print("==COVERAGE CHANGED ",flush=True)
            print("==coverage input ", input, flush=True)
            print("=== load regions()", flush=True)
            coverage = input
            #region = rand_opt(coverage)
            region = get_regions_by_coverage(input)
            print("== rand regions", region, flush=True)
        else:
            print("--skipping coverage\n", flush=True)
            raise PreventUpdate

        return region

    @app.callback(
        Output(component_id='signal', component_property='options'),
        Input(component_id='region', component_property='value')

    )
    # Update Regions
    def cb_region(input):
        signal = []
        if dash.callback_context.triggered[0]['prop_id'].split('.')[0] == "region":
            print("==REGION CHANGED ",flush=True)
            print("==region input ", input, flush=True)
            print("=== load signals()", flush=True)
            region = input
            #signal = rand_opt(region)
            signal = get_signals_by_region(input)
            print("=== signals", signal, flush=True)
        else:
            print("-- skipping region\n", flush=True)
            raise PreventUpdate


        return signal


    # Update Signals
    @app.callback(
        # Graph Output
        # Output(component_id='direction', component_property='children'),
        # Output(component_id='day', component_property='children'),
        # Output(component_id='approach', component_property='children'),
        # Filter Fields
        Output(component_id='day', component_property='value'),
        Output(component_id='direction', component_property='value'),
        Output(component_id='approach', component_property='value'),
        Input(component_id='signal', component_property='value'),
    )
    def cb_signal(input):
        day = []
        if dash.callback_context.triggered[0]['prop_id'].split('.')[0] == "signal":
            print("==SIGNAL CHANGED ", flush=True)
            #reply = 'true'
            print("==signal input ", input, flush=True)
            print("== load day()", flush=True)
            signal = input
            #day = rand_opt(signal)
            print("=== day", day, flush=True)
        else:
            print("--skipping cb_signals\n", flush=True)
            raise PreventUpdate

        # Reset day/dir/approach to defaults
        return '2', 'ALL', 'ALL'

    # Update tier 3 filters and graphs
    @app.callback(
        Output(component_id='dash-wrapper__pie--delay-chart', component_property='figure'),
        Output(component_id='dash-wrapper__pie--arrival-chart', component_property='figure'),
        Output(component_id='dash-wrapper__pie--splitfail-chart', component_property='figure'),
        Output(component_id='dash-wrapper__bar--movement-chart', component_property='figure'),
        Output(component_id='dash-wrapper__scatter--delay-chart', component_property='figure'),
        #Output(component_id='dash-wrapper__pie--splitfail', component_property='children'),
        #Output(component_id='dash-wrapper__delay--chart', component_property='children'),
        #Output(component_id='dash-wrapper__movement--chart', component_property='children'),
        Input(component_id='signal', component_property='value'),
        Input(component_id='day', component_property='value'),
        Input(component_id='approach', component_property='value'),
        Input(component_id='direction', component_property='value'),
    )
    def update_graphs(signal, day, approach, direction):
        td=[]
        ar=[]
        sf = []
        mv = []
        dl = []
        print("== Updating graphs", signal, day, approach, direction, flush=True)

        if (signal != None):

            # Total Delay
            td, tds, tdl, sdf = get_totalDelayChart(signal, day, approach, direction)
            #print("== total delay retry", td)
            # Arrival Pie Chart
            ar, ar1, ar2 = get_arrivalPieChart(signal, day, approach, direction)
            #print("== arrival", ar)
            # Split Failure
            sf, sf1, sf2, sf3 = get_splitPieChart(signal, day, approach, direction)
            # Movement
            mv = get_movementBarChart(signal, day, approach, direction)

            # Scatter
            dl = get_peakScatterPlot(signal, day, approach, direction)
        else:
            print("-- Skipping update_graphs", flush=True)

        return td, ar, sf, mv, dl


# def init_callbacks(dash_app):
#     return

#content = html.Div([], id="page-content")
#
# # Defines the page content for any given light
# def pageContent():
#
#     return [
#         # Create Title And Dropdown
#         html.H1("Broward " + str(light) + " Light", style={"text-align": 'center'}),
#
#         # Create Coverage Dropdown
#         html.Div([
#             html.H2("Coverage"),
#             dcc.Dropdown(
#                 id='coverage',
#                 options=get_coverages_by_user()
#             )
#         ],
#         style={"width": "10%"}),
#
#         # Create Region Dropdown
#         html.Div(id='region-dropdown'),
#
#         # Create Signal Dropdown
#         html.Div(id='signal-dropdown'),
#
#         # Create Day Dropdown
#         html.Div([
#             html.H2("Day"),
#             dcc.Dropdown(
#                 id='day',
#                 options=[
#                         {'label': 'Sunday', 'value': 1},
#                         {'label': 'Monday', 'value': 2},
#                         {'label': 'Tuesday', 'value': 3},
#                         {'label': 'Wednesday', 'value': 4},
#                         {'label': 'Thursday', 'value': 5},
#                         {'label': 'Friday', 'value': 6},
#                         {'label': 'Saturday', 'value': 7},
#                 ],
#                 value=1
#             )
#         ],
#         style={"width": "10%"}),
#
#         # options=get_coverages(1) # replace with list to get user '1's coverages
#
#         # Create Dropdown for Approach
#         html.Div([
#             html.H2("Approach"),
#             dcc.Dropdown(
#                 id='approach',
#                 options=[
#                     {'label': 'Northbound', 'value': 'Northbound'},
#                     {'label': 'Eastbound', 'value': 'Eastbound'},
#                     {'label': 'Southbound', 'value': 'Southbound'},
#                     {'label': 'Westbound', 'value': 'Westbound'},
#                     {'label': 'ALL', 'value': 'ALL'},
#                 ],
#                 value='ALL'
#             )
#         ],
#         style={"width": "10%"}),
#
#         # Create dropdwon for travel direction
#         html.H2("Travel Direction"),
#         html.Div([
#             dcc.Dropdown(
#                 id='tdirection',
#                 options=[
#                     {'label': 'Straight', 'value': 'Straight'},
#                     {'label': 'Left', 'value': 'Left'},
#                     {'label': 'Right', 'value': 'Right'},
#                     {'label': 'ALL', 'value': 'ALL'},
#                 ],
#                 value='ALL'
#             )
#         ],
#         style={'width': '10%'}),
#
#         # Create Total Delay Chart
#         html.Div([
#             dcc.Graph(id='total-delay-chart'),
#             html.H5(id="avg-delay", style={'padding-left': '150px'}),
#             html.H5(id="total-delay", style={'padding-left': '150px'}),
#             html.H5(id="total-delay-crossings", style={'padding-left': '150px'}),
#         ], style={"display": "inline-block", "width": "30%", "vertical-align": "top"}),
#
#         # Create Arrivals Chart
#         html.Div([
#             dcc.Graph(id='arrival-chart'),
#             html.H5(id='green-Arrival-Rate', style={'padding-left': '150px'}),
#             html.H5(id='arrival-Crossings', style={'padding-left': '150px'})
#         ], style={"width": "30%", "display": "inline-block"}),
#
#         # Create Split Failure Chart
#         html.Div([
#             dcc.Graph(id='split-fail'),
#             html.H5(id='Split-Rate', style={'padding-left': '150px'}),
#             html.H5(id='Total-Split-Fail', style={'padding-left': '150px'}),
#             html.H5(id='Split-Crossing', style={'padding-left': '150px'})
#         ], style={"display": "inline-block", "width": "30%", "vertical-align": "top"}),
#
#         # movement and approachDirection bar chart
#         html.Div([
#             dcc.Graph(id='movement'),
#         ]),
#
#         html.Div([
#             dcc.Graph(id='delayScatter'),
#         ])
#     ]
#
#
# # Makes a pie chart for any given light
# def arrivalPieChart(light, day, approach, tdirection):
#     arrivalRates, greenArrivalRate, arrivalCrossings = get_arrivalPieChart(light, day, approach, tdirection)
#     greenArrivalRateStr = "Green Arrival Rate: {}%".format(greenArrivalRate)
#     arrivalCrossingsStr = "Arrival Crossings: {}".format(arrivalCrossings)
#     return arrivalRates, greenArrivalRateStr, arrivalCrossingsStr
#
# # Makes a split failure pie chart for any given light
# def splitPieChart(light, day, approach, tdirection):
#     splitFailure, splitCrossing, totalSplitFailure, SplitRate = get_splitPieChart(light, day, approach, tdirection)
#     splitCrossingStr = "Split Failure Crossings: {}".format(splitCrossing)
#     totalSplitFailureStr = "Total Split Failures: {}".format(totalSplitFailure)
#     SplitRateStr = "Split Failure Rate: {}%".format(SplitRate)
#
#     return splitFailure, splitCrossingStr, totalSplitFailureStr, SplitRateStr
#
# def totalDelayChart(light, day, approach, tdirection):
#     fig, delayCrossingsStr, avgDelayStr, totalDelayStr = get_totalDelayChart(light, day, approach, tdirection)
#     return fig, delayCrossingsStr, avgDelayStr, totalDelayStr
#
# #subplots scatterPlot? with histogram
# #dropdown with different variable types, delay, splitfailure, arrival
# #hour and delay in a scatter, by movement
# #stacked bar chart with different movements in each bar for approach direction
# #hours, minutes, seconds columns? for df
# def movementBarChart(light, day, approach, tdirection):
#     moveM = get_movementBarChart(light, day, approach, tdirection)
#     return moveM
#
# def scatterPlot(light, day, approach, tdirection):
#     peakScatter = get_peakScatterPlot(light, day, approach, tdirection)
#     return peakScatter
#
# def init_callbacks(dash_app):
#     # Callback for 3084 charts
#     @dash_app.callback(
#         [Output(component_id='arrival-chart', component_property='figure'),
#         Output(component_id='split-fail', component_property='figure'),
#         Output(component_id='green-Arrival-Rate', component_property='children'),
#         Output(component_id='arrival-Crossings', component_property='children'),
#         Output(component_id='Split-Crossing', component_property='children'),
#         Output(component_id='Total-Split-Fail', component_property='children'),
#         Output(component_id='Split-Rate', component_property='children'),
#         Output(component_id='total-delay-chart', component_property='figure'),
#         Output(component_id='avg-delay', component_property='children'),
#         Output(component_id='total-delay', component_property='children'),
#         Output(component_id='total-delay-crossings', component_property='children'),
#         Output(component_id='delayScatter', component_property='figure'),
#         Output(component_id='movement', component_property='figure')],
#         [Input(component_id='day', component_property='value'),
#         Input(component_id='approach', component_property='value'),
#         Input(component_id='tdirection', component_property='value'),
#         Input(component_id='coverage', component_property='value'),
#         Input(component_id='region-dropdown', component_property='value'),
#         Input(component_id='signal-dropdown', component_property='value')]
#     )
#     def generate_chart(day, approach, tdirection, coverage, region, signal):
#
#         arrivalRates = arrivalPieChart('3084', day, approach, tdirection)
#         splitFailure = splitPieChart('3084', day, approach, tdirection)
#         totalDelay = totalDelayChart('3084', day, approach, tdirection)
#         peakScatter = scatterPlot('3084', day, approach, tdirection)
#         movement = movementBarChart('3084', day, approach, tdirection)
#         return arrivalRates[0], splitFailure[0], arrivalRates[1], arrivalRates[2], splitFailure[1], splitFailure[2], splitFailure[3], totalDelay[0], totalDelay[2], totalDelay[3], totalDelay[1], peakScatter, movement
#
#     # This callback uses the above function to return what belongs on the page
#     @dash_app.callback(
#         Output("page-content", "children"),
#         [Input("url", "pathname")]
#     )
#     def page_content(pathname):
#
#         # Ensure we're an authenticated user before rendering any content
#         if not current_user or not current_user.is_authenticated:
#             return html.Div(strings.ERROR_PAGE_PERMISSION_DENIED)
#
#         # Check here to ensure that we have access to the requested coverage area
#
#         # Different page content depending on which page we are pn
#         #if pathname == "/dashboard/":
#         return pageContent()
#
#     # Callbacks for region
#     @dash_app.callback(
#         Output('region-dropdown', 'children'),
#         [Input('coverage', 'value')]
#     )
#     def render_region_dropdown(coverage):
#         return html.Div([
#             html.H2("Region"),
#             dcc.Dropdown(
#                 id='region',
#                 options=get_regions_by_coverage(coverage)
#             ),
#         ],style={"width": "10%"})
#
#     # Callbacks for signal
#     @dash_app.callback(
#         Output('signal-dropdown', 'children'),
#         [Input('region', 'value')]
#     )
#     def render_signal_dropdown(region):
#         return html.Div([
#             html.H2("Signal"),
#             dcc.Dropdown(
#                 id='signal',
#                 options=get_signals_by_region(region)
#             ),
#         ],style={"width": "10%"})
