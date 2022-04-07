#!/usr/bin/env python3
# import pandas as pd
import glob, itertools, os, re, csv
import mysql.connector

connection = mysql.connector.connect(
    user='root',
    password='beastm0de',
    host='db',
    database='tts_portal'         
)

file_path = '../../data/raw/'

#Dictionary to store each file and separate by common substring. 
def groupData(files):
    dictionary = {}  
    for x in files:  
        key = x[:-12] #common County and signal number. 
        group = dictionary.get(key,[])
        group.append(x)  
        dictionary[key] = group

    return dictionary

#Merge Vehicles and Journey CSV Files takes dict of file names. 
def mergeFiles():
    filelist = [f for f in os.listdir(file_path) if "Vehicles.csv" in f or "Journeys.csv" in f]
    grouped_data = groupData(sorted(filelist, reverse=True))

    li = []
    for key in grouped_data.keys():
        first_file = pd.read_csv(file_path + grouped_data.get(key)[0], sep=',')
        result = first_file
        for x in range(1, len(grouped_data.get(key))):
            second_file = pd.read_csv(file_path + grouped_data.get(key)[x])
            merged = first_file.merge(second_file, on='vehID')
            result = merged
        result.to_csv(file_path + key.strip()+'.csv', index=False)
        li.append(file_path + key.strip()+'.csv')
    
    df_from_each_file = (pd.read_csv(f, low_memory=False) for f in li)
    merge_results = pd.concat(df_from_each_file, ignore_index=True)
    merge_results = merge_results.drop(merge_results.columns[0], axis=1)
    merge_results.to_csv(file_path + key.strip()[:-5]+'.csv', index=True)

def nullify(L):
    """Convert empty strings in the given list to None."""

    # helper function
    def f(x):
        if(x == ''):
            return None
        else:
            return x
        
    return [f(x) for x in L]       

if __name__ == "__main__":
    cursor = connection.cursor()
    
    sql3 = "INSERT INTO coverages (id, coverage_name) VALUES (%s, %s)"
    cursor.execute(sql3, [1, "District 1"])
    cursor.execute(sql3, [2, "District 2"])
    cursor.execute(sql3, [3, "District 3"])
    cursor.execute(sql3, [4, "District 4"])
    cursor.execute(sql3, [5, "District 5"])
    cursor.execute(sql3, [6, "District 6"])
    cursor.execute(sql3, [7, "District 7"])

    sql4 = "INSERT INTO region (id, region_name, coverage_id) VALUES (%s, %s, %s)"
    cursor.execute(sql4, [1, "Indian River", 5])
    cursor.execute(sql4, [2, "St Lucie", 5])
    cursor.execute(sql4, [3, "Martin", 5])
    cursor.execute(sql4, [4, "Palm Beach", 5])
    cursor.execute(sql4, [5, "Broward", 5])
    cursor.execute(sql4, [6, "Monroe", None])
    cursor.execute(sql4, [7, "Miami-Dade", None])

    sql2 = "INSERT INTO signals (id, region_id) VALUES (%s, %s)"
    cursor.execute(sql2, [1037, 5])
    cursor.execute(sql2, [1113, 5])
    cursor.execute(sql2, [3084, 5])

    csv_data = csv.reader(open('./Broward.csv'))
    header = next(csv_data)
    sql = "INSERT INTO vehicles (id,veh_id,delay,red_arrival,split_failure,signal_id,approach_direction,travel_direction,ett,travel_time,exit_status,day,entry_time,exit_time,stops,uturn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for row in csv_data:
        row = nullify(row)
        #print(row)
        cursor.execute(sql, row)

    connection.commit()
    cursor.close()
    print('Done')

