import pandas as pd
import requests
import json

def addHour(df):
    dff = df.copy()
    dff = df['EntryTime']
    tempList = []

    for i in range(0, dff.size):
        string = dff[i]
        c1 = string[11]
        c2 = string[12]
        hour = c1 + c2
        hour = int(hour)
        tempList.append(hour)

    return tempList

def addTimeOfDay(df):
    dff = df.copy()
    dff = df['EntryTime']
    tempList = []
    # Go through each entry in the dataframe to find the hour
    for i in range(0, dff.size):
        string = dff[i]
        c1 = string[11]
        c2 = string[12]
        hour = c1 + c2
        hour = int(hour)
        if (hour >= 11 and hour <= 13):
            tempList.append('Midday')
        elif (hour >= 6 and hour <= 9):
            tempList.append('Morning')
        elif (hour >= 15 and hour <= 19):
            tempList.append('Evening')
        else:
            tempList.append('Other')
    return tempList

vehiclesDf3084 = pd.read_csv("./Dashboard/data/Broward 3084 Vehicles.csv", delimiter=",")
journeyDf3084 = pd.read_csv("./Dashboard/data/Broward 3084 Journeys.csv")

#Merge the journey and vehicle files
vehiclesDf3084 = pd.merge(vehiclesDf3084, journeyDf3084)
vehiclesDf3084['Hour'] = addHour(vehiclesDf3084)

# Add a peak column to keep track of the time of day
vehiclesDf3084['Peak'] = addTimeOfDay(vehiclesDf3084)
vehiclesDf3084.rename(columns = {'ID': 'id',
                     'vehID': 'veh_id',
                     'Delay': 'delay',
                     'RedArrival': 'red_arrival',
                     'SplitFailure': 'split_failure',
                     'SignalID': 'signal_id',
                     'ApproachDirection': 'approach_direction',
                     'TravelDirection': 'travel_direction',
                     'ETT': 'ett',
                     'TravelTime': 'travel_time',
                     'ExitStatus': 'exit_status',
                     'Day': 'day',
                     'EntryTime': 'entry_time',
                     'ExitTime': 'exit_time'}, inplace = True)

for index, vehicle in vehiclesDf3084.iterrows():
    requests.post(
        url='http://localhost:8080/api/vehicles',
        params={
            'id': vehicle['id'],
            'veh_id': vehicle['veh_id'],
            'delay': vehicle['delay'],
            'red_arrival': vehicle['red_arrival'],
            'split_failure': vehicle['split_failure'],
            'approach_direction': vehicle['approach_direction'],
            'ett': vehicle['ett'],
            'travel_time': vehicle['travel_time'],
            'exit_status': vehicle['exit_status'],
            'day': vehicle['day'],
            'entry_time': vehicle['entry_time'],
            'exit_time': vehicle['exit_time'],
            'travel_direction': vehicle['travel_direction'],
            'signal_id': vehicle['signal_id']
        }).json()
#'stops': vehicle['stops'], t3mporary out
#'uturn': vehicle['uturn'],
#'coverage_id': vehicle['coverage_id'],