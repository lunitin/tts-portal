from re import L
from shutil import move
import dash
import requests, json
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#from sklearn.metrics import coverage_error
from flask_login import current_user
from app import strings
import time


from .server_calls import get_coverages_by_user, get_signals_by_region, get_regions_by_coverage, get_arrivalPieChart, get_movementBarChart, get_peakScatterPlot, get_splitPieChart, get_totalDelayChart

base_url = "/dash/app/"


def init_dashboard(server):
    dash_app = dash.Dash(__name__,server=server,routes_pathname_prefix=base_url,external_stylesheets=['/css/bootstrap.css', '/css/dash.css'],)
    print("== init current user:", current_user)
    # This defines the app layout
    dash_app.layout = html.Div(id="dash-row", children = [
        dcc.Location(id="url"),
        dbc.Spinner(
            fullscreen= True,
            color="primary",
            size="md",
            delay_hide=10,
            fullscreen_style={'background-color': 'rgba(255, 255, 255, 0.60)'},
            children=[
                html.Div(id='dashboard-wrapper')
            ],
        ),
    ], className='loading-wrapper')

    # Eliminate callback errors for dynamic elements
    dash_app.config.suppress_callback_exceptions=True

    init(dash_app)
    return dash_app.server

"""
# Random pull down data generation function

import random
def rand_opt(fake):
    o = []
    for i in range(0, 1000):
        if i % int(fake) == 0:
            o.append({"label": i , "value": i })

    return o
"""

# Default Plotly Graph options
graph_config = {
    'displaylogo': False,
    'margin': { 'autoexpand': False,
                't': 0,
                'r': 0,
                'b': 0,
                'l': 0,
    },

}


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

    content = dbc.Container(id="dash-wrapper", fluid=True, children=[

                # Area Selection Fields
                dbc.Row(id="dash-wrapper__fields", children=[
                    dbc.Col(width=12, md=4, xl=4, children=[
                        dbc.Label('Coverage Area'),
                        dcc.Dropdown(
                            id='coverage',
                            options = coverage,
                            placeholder = 'Select a Coverage Area'
                        )
                    ]),

                    dbc.Col(width=12, md=4, xl=4, children=[
                        dbc.Fade(id='dash-wrapper__fields--region--fade',
                            is_in=False,
                            appear=False,
                            children= [
                                dbc.Label('Region'),
                                dcc.Dropdown(
                                    id='region',
                                    options = [],
                                    placeholder='Select a Region'
                                )
                            ],
                        ),
                    ]),

                    dbc.Col(width=12, md=4, xl=4, children=[
                        dbc.Fade(id='dash-wrapper__fields--signal--fade',
                            is_in=False,
                            appear=False,
                            children = [
                                dbc.Label('Signal'),
                                dcc.Dropdown(
                                    id='signal',
                                    options = [],
                                    placeholder='Select a Signal'
                                )
                            ],

                        ),
                    ]),
                ]),

                # Filter Fields and Graphs
                dbc.Fade(id='dash-wrapper__fields--graphs--fade',
                    is_in=False,
                    appear=False,
                    children = [
                        # Should we have an Area/Region/Signal Title here?
                        # dbc.Row(id="dash-wrapper__title", children=[
                        #     dbc.Col(width=12, children=[
                        #         html.Span([html.H3(id="dash-wrapper__title--coverage")]),
                        #         html.Span([html.H3(id="dash-wrapper__title--region")]),
                        #         html.Span([html.H3(id="dash-wrapper__title--signal")]),
                        #     ]),
                        # ]),

                        # Detail Filter Fields
                        dbc.Row(id="dash-wrapper__fields-detail", className='mt-3 mb-4', children=[
                            dbc.Col(width=12, md=4, xl=4, children=[
                                dbc.Label('Day'),
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
                                    value='2',
                                    placeholder='Day',
                                    clearable=False,
                                )
                            ]),
                            dbc.Col(width=12, md=4, xl=4, children=[
                                dbc.Label('Approach'),
                                dcc.Dropdown(
                                    id='approach',
                                    options=[{'label': 'ALL', 'value': 'ALL'},
                                        {'label': 'Northbound', 'value': 'Northbound'},
                                        {'label': 'Eastbound', 'value': 'Eastbound'},
                                        {'label': 'Southbound', 'value': 'Southbound'},
                                        {'label': 'Westbound', 'value': 'Westbound'},
                                    ],
                                    value='ALL',
                                    placeholder='Approach',
                                    clearable=False,
                                )
                            ]),
                            dbc.Col(width=12, md=4, xl=4, children=[
                                dbc.Label('Travel Direction'),
                                dcc.Dropdown(
                                    id='direction',
                                    options=[{'label': 'ALL', 'value': 'ALL'},
                                        {'label': 'Straight', 'value': 'Straight'},
                                        {'label': 'Left', 'value': 'Left'},
                                        {'label': 'Right', 'value': 'Right'},
                                    ],
                                    value='ALL',
                                    placeholder='Direction',
                                    clearable=False,
                                )
                            ])
                        ]),
                        # Pie Charts
                        dbc.Row(id="dash-wrapper__pie row",children=[
                            dbc.Col(width=12, md=4, xl=4, className='', children=[
                                #dbc.Label('Total Delay'),
                                dbc.Row([
                                    dbc.Col(id="dash-wrapper__pie--delay", children=[
                                        dcc.Graph(id="dash-wrapper__pie--delay-chart", config=graph_config),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div(['Total Crossings:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--delay-label1")]),
                                    ]),
                                    dbc.Col([
                                        html.Div(['Average Delay:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--delay-label2"),' sec/vehicle'],),
                                    ]),
                                    dbc.Col([
                                        html.Div(['Total Delay:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--delay-label3"), ' hours']),
                                    ]),
                                ]),
                            ]),
                            dbc.Col(width=12, md=4, xl=4,  className='border-start border-light', children=[
                                #dbc.Label('Arrival Rates'),
                                dbc.Row([
                                    html.Div(id="dash-wrapper__pie--arrival", children=[
                                        dcc.Graph(id="dash-wrapper__pie--arrival-chart", config=graph_config),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div(['Green Arrival Rate:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--arrival-label1"), '%']),
                                    ]),
                                    dbc.Col([
                                        html.Div(['Arrival Crossings:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--arrival-label2")]),
                                    ]),
                                ]),
                            ]),
                            dbc.Col(width=12, md=4, xl=4,  className='border-start border-light', children=[
                                #dbc.Label('Split Failure'),
                                dbc.Row([
                                    dbc.Col(id="dash-wrapper__pie--splitfail", children=[
                                        dcc.Graph(id="dash-wrapper__pie--splitfail-chart", config=graph_config),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div(['Split Failure Crossings:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--splitfail-label1")]),
                                    ]),
                                    dbc.Col([
                                        html.Div(['Total Split Failures:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--splitfail-label2")]),
                                    ]),
                                    dbc.Col([
                                        html.Div(['Split Failure Rate:']),
                                        html.Div([dbc.Label(id="dash-wrapper__pie--splitfail-label3"), '%']),
                                    ]),
                                ]),
                            ])
                        ]),
                        # Movement charts
                        dbc.Row(id="dash-wrapper__bar", children=[
                                #dbc.Label('Movement'),
                                dbc.Col(id="dash-wrapper__bar--movement",  className='', children=[
                                    dcc.Graph(id="dash-wrapper__bar--movement-chart", config=graph_config),
                                ]),
                            ]),

                        # Delay Chart
                        dbc.Row(id="dash-wrapper__scatter",children=[

                            #dbc.Label('Delay by Hour'),
                            dbc.Col(id="dash-wrapper__scatter",  className='', children=[
                                dcc.Graph(id="dash-wrapper__scatter--delay-chart", config=graph_config),
                            ]),

                        ]),
                    ]),
                ],
            )


    return content

# Field callbacks are automatically called once
def init(app):

    print("== app current user:", current_user)

    #
    @app.callback(
        Output(component_id='dashboard-wrapper', component_property='children'),
        Input('url', 'pathname')
    )
    def page(url):

        # Ensure we're an authenticated user before rendering any content
        if not current_user or not current_user.is_authenticated:
            return html.Div(strings.ERROR_PAGE_PERMISSION_DENIED)

        print("- page callback", flush=True)
        return set_layout()



    # Update Regions
    @app.callback(
        Output(component_id='region', component_property='options'),
        Output(component_id='dash-wrapper__fields--region--fade', component_property='is_in'),

        Input(component_id='coverage', component_property='value'),
        Input(component_id='coverage', component_property='options'),
    )

    def cb_coverage(coverage, options):
        print("== cb_coverage callback, triggered by ",  ctx.triggered_id)

        if ctx.triggered_id == "coverage":
            print("==COVERAGE CHANGED ",flush=True)
            print("==coverage input ", coverage, flush=True)
            print("=== load regions()", flush=True)

            #region = rand_opt(coverage)
            regions = get_regions_by_coverage(coverage)

            print("== regions", regions, flush=True)

            return regions, True
        else:
            print("--skipping coverage\n", flush=True)
            raise PreventUpdate



    @app.callback(
        Output(component_id='signal', component_property='options'),

        Input(component_id='coverage', component_property='value'),
        Input(component_id='region', component_property='value')

    )
    # Update Regions
    def cb_region(coverage, region):
        print("== cb_region callback, triggered by ",  ctx.triggered_id)

        # Fetch signals when a region is selected
        if ctx.triggered_id == "region" and region != None:
            print("==REGION CHANGED ",flush=True)
            print("==region input ", coverage, region, flush=True)
            print("=== load signals()", flush=True)

            #signal = rand_opt(region)
            signals = get_signals_by_region(region)

            print("=== signals", signals, flush=True)

            return signals #, True
        # Fade in when a coverage is selected
        # elif ctx.triggered_id == "coverage":
        #     return [], True

        else:
            print("-- skipping region\n", flush=True)
            raise PreventUpdate


    # Update Signals
    @app.callback(
        Output(component_id='day', component_property='value'),
        Output(component_id='direction', component_property='value'),
        Output(component_id='approach', component_property='value'),
        Output(component_id='dash-wrapper__fields--signal--fade', component_property='is_in'),

        Input(component_id='coverage', component_property='value'),
        Input(component_id='region', component_property='value'),
        Input(component_id='signal', component_property='value'),
    )
    def cb_signal(coverage, region, signal):

        print("== cb_region callback, triggered by ",  ctx.triggered_id)

        # Fade out if there is no region i.e. coverage area changed
        if region == None:
            return '2', 'ALL', 'ALL', False
        # Update graphs if a signal is selected
        elif ctx.triggered_id == "signal" and signal != None:
            print("==SIGNAL CHANGED ", flush=True)

            print("==signal input ", coverage, region, signal, flush=True)
            print("== set filter dropdowns, load graphs", flush=True)

            # Reset day/dir/approach to defaults and fade graphs in
            return '2', 'ALL', 'ALL', True
        # Fade in if triggered from a region selection
        elif ctx.triggered_id == "region":
            return '2', 'ALL', 'ALL', True
        # Reset day/dir/approach to defaults and fade graphs out
        elif ctx.triggered_id == "coverage":
            return '2', 'ALL', 'ALL', False

        else:
            print("--skipping cb_signals\n", flush=True)
            raise PreventUpdate



    # Update tier 3 filters and graphs
    @app.callback(
        Output(component_id='dash-wrapper__fields--graphs--fade', component_property='is_in'),

        Output(component_id='dash-wrapper__pie--delay-chart', component_property='figure'),
        Output(component_id='dash-wrapper__pie--delay-label1', component_property='children'),
        Output(component_id='dash-wrapper__pie--delay-label2', component_property='children'),
        Output(component_id='dash-wrapper__pie--delay-label3', component_property='children'),

        Output(component_id='dash-wrapper__pie--arrival-chart', component_property='figure'),
        Output(component_id='dash-wrapper__pie--arrival-label1', component_property='children'),
        Output(component_id='dash-wrapper__pie--arrival-label2', component_property='children'),

        Output(component_id='dash-wrapper__pie--splitfail-chart', component_property='figure'),
        Output(component_id='dash-wrapper__pie--splitfail-label1', component_property='children'),
        Output(component_id='dash-wrapper__pie--splitfail-label2', component_property='children'),
        Output(component_id='dash-wrapper__pie--splitfail-label3', component_property='children'),

        Output(component_id='dash-wrapper__bar--movement-chart', component_property='figure'),
        Output(component_id='dash-wrapper__scatter--delay-chart', component_property='figure'),

        State(component_id='region', component_property='value'),
        Input(component_id='signal', component_property='value'),
        Input(component_id='day', component_property='value'),
        Input(component_id='approach', component_property='value'),
        Input(component_id='direction', component_property='value'),

    )
    def cb_update_graphs(region, signal, day, approach, direction):

        print("== cb_update_graphs callback, triggered by ",  ctx.triggered_id)
        print("== Updating graphs", signal, day, approach, direction, flush=True)

        # Fetch charts and labels
        if (region != None and signal != None):


            fig_td, lbl_td1, lbl_td2, lbl_td3 = get_totalDelayChart(signal, day, approach, direction)


            fig_ar, lbl_ar1, lbl_ar2 = get_arrivalPieChart(signal, day, approach, direction)

            fig_sf, lbl_sf1, lbl_sf2, lbl_sf3 = get_splitPieChart(signal, day, approach, direction)

            fig_mv = get_movementBarChart(signal, day, approach, direction)

            fig_dl = get_peakScatterPlot(signal, day, approach, direction)

            return (True,
                fig_td, lbl_td1, lbl_td2, lbl_td3,
                fig_ar, lbl_ar1, lbl_ar2,
                fig_sf, lbl_sf1, lbl_sf2, lbl_sf3,
                fig_mv, fig_dl)
        # Clear charts and labels and fade out
        else:
            return (False,
                [], '','','',
                [], '','',
                [], '','','',
                [], []
             )




# def init_callbacks(dash_app):
#     return

#content = html.Div([], id="page-content")
#
# # Defines the page content for any given light
# def pageContent():
#
#     return [
#         # Create Title And Dropdown
#         dbc.Label("Broward " + str(light) + " Light", style={"text-align": 'center'}),
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
