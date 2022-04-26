import json, requests
from ..resources import User_Coverages
import plotly
from flask import jsonify
from flask_login import current_user
BASE_URL = 'http://localhost:80/api/'

def get_coverages_by_user():
    #print(jsonify(current_user))
    #s = requests.Session()
    #coverages_by_current_user_id = s.get(BASE_URL+'users/coverages').json()
    #coverage_list = []
    #for coverage in coverages_by_current_user_id:
    #    coverage_list.append({'label': coverage['coverage_name'], 'value': coverage['coverage_name']})
    return [('district 1', 1),('district 2', 2),('district 5', 5)]

def get_regions_by_coverage(id):
    regions_by_coverage_id = requests.get(BASE_URL+'coverages/regions'+str(id)).json()
    regions_list = []
    for region in regions_by_coverage_id:
        regions_list.append({'label': region[id], 'value': region[id]})
    return regions_list    

def get_signals_by_region(id):
    signals_by_region_id = requests.get(BASE_URL+'regions/signals/'+str(id)).json()
    signal_list = []
    for signal in signals_by_region_id:
        signal_list.append({'label': signal[id], 'value': signal[id]})
    return signal_list    

def get_arrivalPieChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'/dashboard/arrivalPieChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        }).json()
    if data == 0:
        return(0,0,0)
    p = plotly.io.from_json(data['plot'])
    return p, data['greenArrivalRate'], data['arrivalCrossings']

def get_peakScatterPlot(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'/dashboard/peakScatterPlot',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        }).json()
    if data == 0:
        return(0)
    p = plotly.io.from_json(data['plot'])
    return p

def get_totalDelayChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'/dashboard/totalDelayChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        }).json()
    if data == 0:
        return(0,0,0,0)
    p = plotly.io.from_json(data['plot'])
    return p, data['delayCrossingsStr'], data['avgDelayStr'], data['totalDelayStr']

def get_splitPieChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'/dashboard/splitPieChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        }).json()
    if data == 0:
        return(0,0,0,0)
    p = plotly.io.from_json(data['plot'])
    return p, data['splitCrossings'], data['totalSplitFailure'], data['splitRate']

def get_movementBarChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'/dashboard/movementBarChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        }).json()
    if data == 0:
        return(0)
    p = plotly.io.from_json(data['plot'])
    return p
