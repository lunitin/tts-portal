#import json, requests
from ..resources import User_Coverages
import plotly
BASE_URL = 'http://localhost:80/api/'

def get_coverages(id):
    coverages_by_current_user_id = requests.get(BASE_URL+'users/'+str(id)+'/coverages').json()
    coverage_list = []
    for coverage in coverages_by_current_user_id:
        coverage_list.append({'label': coverage['coverage_name'], 'value': coverage['coverage_name']})
    return coverage_list

def get_coverages_not_http(id):
    coverages_by_current_user_id = User_Coverages.get(User(),id=1).json()
    coverage_list = []
    for coverage in coverages_by_current_user_id:
        coverage_list.append({'label': coverage['coverage_name'], 'value': coverage['coverage_name']})
    return coverage_list

def get_arrivalPieChart(signal, day, approach, tdirection):
    data = requests.get(
        url=BASE_URL+'/dashboard/arrivalPieChart',
        params={
            'day': str(day),
            'approach': str(approach),
            'signal': str(signal),
            'tdirection': str(tdirection)
        }).json()
    p = plotly.io.from_json(data['plot'])
    return p, data['greenArrivalRate'], data['arrivalCrossings']
