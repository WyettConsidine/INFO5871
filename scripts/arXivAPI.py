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
                    txt = child.text
                    if txt is not None:
                        txt = txt.replace(',','')
                    dictionary[tag] = txt

            print(entries)        
            df = pd.DataFrame(entries)
            #print(df.columns)
            df['summary'] = df['summary'].apply(lambda x: str(x).replace('\n',' '))
            df['summary'] = df['summary'].apply(lambda x: str(x).replace('\t',' '))
            #df['label'] = label
            return df
            #df.to_csv(path+'/arXiv_AI.txt',sep = '\t',index = False)

            #df = pd.read_csv(path+'/arXiv_AI.txt',sep = '\t')        

def loadIntoFile(summaryDF, subject, label):
    today = date.today()
    summaryDF.to_csv(f'./resourceFiles/corpus2(arXiv)/arXivData(query={subject + " " +label}){today}.csv', index=False) 

def joinLabeledData(filePath1, l1, filePath2, l2, newFilePath):
    contentDF = pd.read_csv(filePath1)
    contentDF['Label'] = l1

    contentDF2 = pd.read_csv(filePath2)
    contentDF2['Label'] = l2

       
    frames = [contentDF, contentDF2]
    totalContent = pd.concat(frames)
    totalContent.to_csv(newFilePath, index=True)

def main():
    #  subject = '\"nuclear energy\"'
    #  datadf = basicArXivCall(subject, 'risk')
    #  loadIntoFile(datadf, subject.replace('\"',''), 'risk')

    joinLabeledData('resourceFiles\\corpus2(arXiv)\\arXivData(query=nuclear energy risk)2024-02-08.csv', 'risk',
                    'resourceFiles\\corpus2(arXiv)\\arXivData(query=nuclear energy safe)2024-02-08.csv', 'safe',
                    'resourceFiles\\corpus3(newsAPI)\\arXivDataLabeled(query=Nuclear Energy).csv')

if __name__ == "__main__":
    main()