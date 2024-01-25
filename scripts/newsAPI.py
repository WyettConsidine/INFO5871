import requests  #to query the API 
import re  #regular expressions
import pandas as pd   # for dataframes

from datetime import date
from dateutil.relativedelta import relativedelta

#Addapted from https://newsapi.org/docs/client-libraries/python

# Init
api_key='efa4bfad3e8749d19ffd8298771cbfdb'
endpointAr='https://newsapi.org/v1/articles'

def basicNewsAPICall(endpoint, key, subject, source):
    URLPost = {'apiKey': key,
                    'source': source, 
                    'pageSize': 85,
                    'sortBy' : 'top',
                    'totalRequests': 75,
                    'q':subject}
    resp1 = requests.get(endpoint,URLPost)
    print(resp1.json()['articles'][0]['authors'])


basicNewsAPICall(endpointAr,api_key,'Nuclear Energy', 'bbc-news')
