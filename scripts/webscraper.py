from bs4 import BeautifulSoup
import newsAPI
import requests
from datetime import date

def urlToText(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soup.prettify())
    content = ""
    paragraphs = soup.find_all('p')
    #print(len(paragraphs))
    for p in paragraphs:
        for line in p.text.strip().split('\n'):
            #print(line)
            if (len(line) > 200) & ('©' not in line):
                content += line
    #print(content)
    return content

def urlsToTxt(urls, num_urls = 10):
    corpus = []
    count = 0
    for url in urls:
        count += 1 
        text = urlToText(url)
        #print(text)
        corpus.append(text)
        if count > num_urls:
            break
    return corpus
        
def strip_ascii(text):
    return "".join(
        char for char
        in text
        if 31 < ord(char) < 127
    )

def writeToFile(contList, subject):
    today = date.today()
    with open(f'./resourceFiles/corpus4(bs4)/webScraped(query={subject}){today}.csv', 'a') as f:
        for line in contList:
            f.write(f"{strip_ascii(line)}\n") 
    return 'Complete'



def main():
    print('WebScraping Start')
    subject = '\"Nuclear Energy\" safe'
    api_key, endpoint = newsAPI.getArticleURLsParams()
    urls = newsAPI.getArticleURLs(api_key, endpoint, subject)
    cont = urlsToTxt(urls, 20)
    writeToFile(cont, subject.replace('\"',''))
    print(cont)
    #content=urlToText('https://www.wired.com/story/global-emissions-could-peak-sooner-than-you-think/')

    #content2 = urlToText('https://www.androidcentral.com/phones/betavolt-technology-developing-radionuclide-battery')

    print("-------------------------")
    #print(content)
    #print(content2)

if __name__ == "__main__":
    main()