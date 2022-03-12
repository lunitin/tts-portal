import json, requests
from ..resources import User_Coverages

def get_coverages(id):
    coverages_by_current_user_id = requests.get('http://localhost:80/api/users/'+str(id)+'/coverages').json()
    coverage_list = []
    for coverage in coverages_by_current_user_id:
        coverage_list.append({'label': coverage['coverage_name'], 'value': coverage['coverage_name']})
    return coverage_list

def get_coverages_not_http(id):
    coverages_by_current_user_id = User_Coverages.get(User(),id=1).json()
    print(coverages_by_current_user_id)
    coverage_list = []
    for coverage in coverages_by_current_user_id:
        coverage_list.append({'label': coverage['coverage_name'], 'value': coverage['coverage_name']})
    return coverage_list
