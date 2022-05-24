
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
from app import strings
import json
from .server_calls import get_coverages_by_user, get_signals_by_region, get_regions_by_coverage, get_arrivalPieChart, get_movementBarChart, get_peakScatterPlot, get_splitPieChart, get_totalDelayChart

base_url = "/dash/app/"

# Connect Dash up to Flask
def init_dashboard(server):
    dash_app = dash.Dash(__name__,server=server,routes_pathname_prefix=base_url,external_stylesheets=['/css/bootstrap.css', '/css/dash.css'],)

    # This defines the app container within the DOM
    # loading-wrapper class is used to override visibility of fullscreen parent div
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

    # API
    # We use the API here so that admins can fetch all coverage areas since
    # user relationships will only return explicit coverage memberships
    # This delays page loading a bit

    # @TODO - Swap when User model relatonships are fixed for admins
    coverage = get_coverages_by_user();

    # User Relationships
    #for c in current_user.coverages:
    #   coverage.append({'label': c.coverage_name, 'value': c.id})

    return dbc.Container(id="dash-wrapper", fluid=True, children=[

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


# Field callbacks are initialized on page load and will contain current_user data
def init(app):

    # Page generation callback
    @app.callback(
        Output(component_id='dashboard-wrapper', component_property='children'),
        Input('url', 'pathname')
    )
    def page(url):

        # Ensure we're an authenticated user before rendering any content
        if not current_user or not current_user.is_authenticated:
            return html.Div(strings.ERROR_PAGE_PERMISSION_DENIED)

        #print("- page callback", flush=True)
        return set_layout()


    @app.callback(
        Output(component_id='region', component_property='options'),
        Output(component_id='dash-wrapper__fields--region--fade', component_property='is_in'),

        Input(component_id='coverage', component_property='value'),
        Input(component_id='coverage', component_property='options'),
    )
    def cb_coverage(coverage, options):

        if ctx.triggered_id == "coverage":
            regions = []
            #regions = rand_opt(coverage)
            # API
            regions = get_regions_by_coverage(coverage)

            # User Relationships
            # for c in current_user.coverages:
            #     if c.id == coverage:
            #         for r in c.regions:
            #             regions.append({'label': r.region_name, 'value': r.id})
            #         break

            return regions, True
        else:
            raise PreventUpdate


    @app.callback(
        Output(component_id='signal', component_property='options'),

        Input(component_id='coverage', component_property='value'),
        Input(component_id='region', component_property='value')

    )
    def cb_region(coverage, region):

        # Fetch signals when a region is selected
        if ctx.triggered_id == "region" and region != None:
            signals = []

            #signals = rand_opt(region)
            # API
            signals = get_signals_by_region(region)

            # User Relationships
            # for c in current_user.coverages:
            #     if c.id == coverage:
            #         for r in c.regions:
            #             if r.id == region:
            #                 for s in r.signals:
            #                     signals.append({'label': s.id, 'value': s.id})
            #                 break

            return signals
        else:
            raise PreventUpdate


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

        # Fade out if there is no region i.e. coverage area changed
        if region == None:
            return '2', 'ALL', 'ALL', False

        # Update graphs if a signal is selected
        elif ctx.triggered_id == "signal" and signal != None:
            # Reset day/dir/approach to defaults and fade graphs in
            return '2', 'ALL', 'ALL', True

        # Fade in if triggered from a region selection
        elif ctx.triggered_id == "region":
            return '2', 'ALL', 'ALL', True

        # Reset day/dir/approach to defaults and fade graphs out
        elif ctx.triggered_id == "coverage":
            return '2', 'ALL', 'ALL', False

        else:
            raise PreventUpdate


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
