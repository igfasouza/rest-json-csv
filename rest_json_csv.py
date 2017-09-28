import json
import pandas as pd
from pandas.io.json import json_normalize
import requests


def to_string(s):
    try:
        return str(s)
    except:
        #Change the encoding type if needed
        return s.encode('utf-8')
    
    
def reduce_item(key, value):
    global reduced_item
    
    #Reduction Condition 1
    if type(value) is list:
        i=0
        for sub_item in value:
            reduce_item(key+'_'+to_string(i), sub_item)
            i=i+1

    #Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key+'_'+to_string(sub_key), value[sub_key])
    
    #Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)


url = 'https://data.dublinked.ie/cgi-bin/rtpi/routeinformation?routeid=1&operator=BE&format=json'


        
response = requests.get(url)

data = response.json()
data = [data]


processed_data = []
header = []
for item in data:
    reduced_item = {}
    reduce_item('', item)
    header += reduced_item.keys()
    processed_data.append(reduced_item)


df = pd.DataFrame.from_dict(json_normalize(processed_data), orient='columns')

df
