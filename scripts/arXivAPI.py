import pandas as pd 
import requests
import pandas_read_xml as pdx
import xml.etree.ElementTree as ET
import re
from datetime import date

def basicArXivCall(subject, label, max_results=50):
    #path = "C:/Users/wyett/OneDrive/Documents/INFO5871/"
    endpoint = "http://export.arxiv.org/api/query?"
    subject = subject.replace(" ", "+")
    print(subject)
    url = endpoint+"search_query=abs:"+subject+f'+AND+all:{label}'+f'&max_results={max_results}'
    # f'+AND+all:{label}' +
    #url = endpoint+"search_query=all:"+subject+f'&max_results={max_results}'
    print(url)
    try:
        requests.get(url)
    except requests.ConnectionError as e:
        print(e)
    else:
        print('API status: 200')
        with requests.get(url) as response:             

            root = ET.fromstring(response.content)
            entries = []
            dictionary = {}
            for child in root.iter('*'):
                tag = re.sub("\{.*?\}","",child.tag)
                print(tag)
                if tag == 'entry':
                    entries.append(dictionary)
                    print("dictionary " + str(dictionary))
                    dictionary = {}
                if tag in ['title','summary','primary_category']:
                    print(tag)
                    dictionary[tag] = child.text

            print(entries)        
            df = pd.DataFrame(entries)
            #print(df.columns)
            df['summary'] = df['summary'].apply(lambda x: str(x).replace('\n',' '))
            df['summary'] = df['summary'].apply(lambda x: str(x).replace('\t',' '))
            #df['label'] = label
            print(df.columns)
            print(df.title.values)
            return df
            #df.to_csv(path+'/arXiv_AI.txt',sep = '\t',index = False)

            #df = pd.read_csv(path+'/arXiv_AI.txt',sep = '\t')        

def loadIntoFile(summaryDF, subject, label):
    today = date.today()
    summaryDF.to_csv(f'./resourceFiles/corpus2(arXiv)/arXivData(query={subject + " " +label}){today}.csv', index=False) 

def main():
    subject = '\"nuclear energy\"'
    datadf = basicArXivCall(subject, 'safe')
    loadIntoFile(datadf, subject.replace('\"',''), 'safe')


if __name__ == "__main__":
    main()