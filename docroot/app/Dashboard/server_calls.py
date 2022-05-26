import json, requests
from ..resources import User_Coverages
import plotly
from flask import jsonify, request
from flask_login import current_user
BASE_URL = 'http://localhost/api/'


# request coverages that belong to the current user for drop down selector
def get_coverages_by_user():

    url = BASE_URL+'users/coverages/' + str(current_user.id)
    res = requests.get(url, cookies=request.cookies)

    if res.status_code == 200:
        coverage_list = []
        for coverage in json.loads(res.json()):
            coverage_list.append({'label': coverage['coverage_name'], 'value': coverage['id']})
        return coverage_list
    else:
        return 0

# request regions that belong to a given coverage id for drop down selector
def get_regions_by_coverage(id):
    res = requests.get(BASE_URL+'coverages/regions/'+str(id), cookies=request.cookies)
    if res.status_code == 200:
        regions_list = []
        for region in json.loads(res.json()):
            regions_list.append({'label': region['region_name'], 'value': region['id']})
        return regions_list
    else:
        return 0

# request signals based on region id for drop down selector
def get_signals_by_region(id):
    res = requests.get(BASE_URL+'regions/signals/'+str(id), cookies=request.cookies)
    if res.status_code == 200:
        signal_list = []
        for signal in json.loads(res.json()):
            signal_list.append({'label': signal['id'], 'value': signal['id']})
        return signal_list
    else:
        return 0

# request the arrivalPieChart plotly plot with the given parameters
def get_arrivalPieChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'dashboard/arrivalPieChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        },
        cookies=request.cookies).json()

    if data == 0:
        return(0,0,0)
    p = plotly.io.from_json(data['plot'])
    return p, data['greenArrivalRate'], data['arrivalCrossings']

# request the peakScatterPlot plotly plot with the given parameters
def get_peakScatterPlot(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'dashboard/peakScatterPlot',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        },
        cookies=request.cookies).json()
    if data == 0:
        return(0)
    p = plotly.io.from_json(data['plot'])
    return p

# request the totalDelayChart plotly plot given the parameters
def get_totalDelayChart(signal, day, approach, tdirection):

    data = requests.get(
        url=BASE_URL+'dashboard/totalDelayChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        },
        cookies=request.cookies).json()

    if data == 0:
        return(0,0,0,0)
    p = plotly.io.from_json(data['plot'])
    return p, data['delayCrossings'], data['avgDelay'], data['totalDelay']

# request the splitPieChart plotly plot given the parameters
def get_splitPieChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'dashboard/splitPieChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        },
        cookies=request.cookies).json()
    if data == 0:
        return(0,0,0,0)
    p = plotly.io.from_json(data['plot'])
    return p, data['splitCrossings'], data['totalSplitFailure'], data['splitRate']

# request the movementBarChart plotly plot given the parameters
def get_movementBarChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'dashboard/movementBarChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        },
        cookies=request.cookies).json()
    if data == 0:
        return(0)
    p = plotly.io.from_json(data['plot'])
    return p
