import pandas as pd 
import requests
import pandas_read_xml as pdx
import xml.etree.ElementTree as ET
import re

def basicArXivCall(subject, max_results=10):
    #path = "C:/Users/wyett/OneDrive/Documents/INFO5871/"
    endpoint = "http://export.arxiv.org/api/query?"
    subject = subject.replace(" ", "+")
    print(subject)
    url = endpoint+"search_query=all:"+subject #+ f"&classification-physics_archives=nucl-ex&max_results={max_results+1}"
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
                if tag == 'entry':
                    entries.append(dictionary)
                    dictionary = {}
                if tag in ['id','updated','published','title','summary','primary_category']:
                    dictionary[tag] = child.text
                    
            df = pd.DataFrame(entries)

            df['summary'] = df['summary'].apply(lambda x: str(x).replace('\n',' '))
            df['summary'] = df['summary'].apply(lambda x: str(x).replace('\t',' '))
            print(df.columns)
            print(df.title.values)

            #df.to_csv(path+'/arXiv_AI.txt',sep = '\t',index = False)

            #df = pd.read_csv(path+'/arXiv_AI.txt',sep = '\t')        


def main():
    basicArXivCall('nuclear energy')


if __name__ == "__main__":
    main()