import pandas as pd
import os
import json

dir_path = '/home/carlos/Escritorio/PERSONAL_PLUGIN_PROJECT/Plugins_Project/statistics_plugin/csvs_files/'

def list_csvs():
    absolute_csvs = []
    csvs = []
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            absolute_csv_route = dir_path + path
            absolute_csvs.append(absolute_csv_route)
            csvs.append(path)

    return csvs

def csv_information(csv):
    df = pd.read_csv(dir_path + csv)
    headers = list(df.columns)
    row_number = len(df)

    json_info = {
        "headers" : headers,
        "row number" : row_number
    }

    return json_info

def column_description(csv, column):
    df = pd.read_csv(dir_path + csv)
    description = df[column].describe().to_dict()
    json_data = json.dumps(description)
    return json_data




# someth = csv_information('wind-power-production-us.csv')
# print(someth)

