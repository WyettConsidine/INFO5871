import requests  #to query the API 
import re  #regular expressions
import pandas as pd   # for dataframes

import csv

#Addapted from https://newsapi.org/docs/client-libraries/python

#List of sources and their polititcal lean:
#goal: approximate normal curve between sources of politically Left, left learning, center, right leaning, and right


# Init
api_key='efa4bfad3e8749d19ffd8298771cbfdb'
endpointArticles='https://newsapi.org/v1/articles'
endpointSources = 'https://newsapi.org/v2/top-headlines/sources'


#political lean of soruces determined with https://www.allsides.com/media-bias/ and https://mediabiasfactcheck.com/
def getSources(endpoint=endpointSources, key=api_key, country = 'us'):
    URLPost = {'apiKey': key, 
                    #'category':'general',
                    'language': 'en',
                    'country':country,
                    }    
    respRaw = requests.get(endpoint,URLPost)
    resp = respRaw.json()
    print(resp['status'])
    if resp['status'] != 'ok':
        print("Non-Ok Status error from NewsApi. Status = " + resp['status'])
    else:
        sources = []
        for src in resp['sources']:
            if src['category'] in ('general', 'science', 'technology', 'health'):
                #print(src['name'] + ", " + src['category'])
                sources.append((src['name'] , src['category']))
        return sources

def getSourceBiasLists():   
    with open('C:/Users/wyett/OneDrive/Documents/INFO5871/resourceFiles/newsAPISourceLists.csv', newline='') as f:
        reader = csv.reader(f)
        sourceFile = list(reader)
        f.close()
    sources = []
    lean = ['left', 'leftLean', 'center', 'rightLean', 'right']
    for srclist in sourceFile:
        sources.append(srclist[1:])
    newsSourceDict = dict(zip(lean, sources))
    print(newsSourceDict)
    return newsSourceDict
        


def basicNewsAPICall(endpoint, key, subject, source):
    URLPost = {'apiKey': key,
                    'source': source, 
                    'pageSize': 85,
                    'sortBy' : 'top',
                    'totalRequests': 75,
                    'q':subject}
    resp1 = requests.get(endpoint,URLPost)
    print(resp1.json()['articles'])





#basicNewsAPICall(endpointArticles,api_key,'Nuclear Energy', 'bbc-news')
#sources = getSources()
#SNames = [source[0] for source in sources]
newsSourceDict = getSourceBiasLists()
print(newsSourceDict['leftLean'])