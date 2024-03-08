from bs4 import BeautifulSoup
import newsAPI
import requests
from datetime import date

def urlToText(url):
    #Use requests library to pull in HTML response
    page = requests.get(url)
    #Use Beautiful Soup library to parse HTML
    #print(page.content)
    soup = BeautifulSoup(page.content, "html.parser")
    content = ""
    paragraphs = soup.find_all('p')
    #Itterate through all 'paragraph' type divisions/tags
    for p in paragraphs:
        for line in p.text.strip().split('\n'):
            #Add line if it is long enough,
            #And does not contain the copywrite character
            if (len(line) > 200) & ('©' not in line):
                content += line
    #return scraped text data
    return content

def urlsToTxt(urls, num_urls = 10):
    corpus = []
    count = 0
    #Itterate through the list of URLS
    for url in urls:
        count += 1 
        #Use webscraping function on URL
        text = urlToText(url)
        #add extracte text to corpus
        corpus.append(text)
        if count > num_urls:
            break
    #Return list of scraped website text
    return corpus
        
def strip_ascii(text):
    return "".join(
        char for char
        in text
        if 31 < ord(char) < 127
    )

def joinLabeledData(filePath1, l1, filePath2, l2, newFilePath,sources = None):
    if sources is not None:
        sources1 = sources[0]
        sources2 = sources[1]
        with (open(filePath1, 'r')) as f1:
            lines1 = [[l1, line[1], line[0].strip()] for line in list(zip(f1, sources1))]
            f1.close()
        with (open(filePath2, 'r')) as f2:
            lines2 = [[l2, line[1], line[0].strip()] for line in list(zip(f2, sources2))]
            f2.close()
        fullLines = lines1 + lines2
        with(open(newFilePath, 'w')) as newF:
            for line in fullLines:
                newF.write(line[0] + "," + line[1] + "," + line[2] + "\n")
    else:
        with (open(filePath1, 'r')) as f1:
            lines1 = [[l1, line.strip()] for line in f1]
            f1.close()
        with (open(filePath2, 'r')) as f2:
            lines2 = [[l2, line.strip()] for line in f2]
            f2.close()
        fullLines = lines1 + lines2
        with(open(newFilePath, 'w')) as newF:
            for line in fullLines:
                newF.write(line[0] + "," + line[1] + "\n")
    

def writeToFile(contList, subject):
    today = date.today()
    print(f"######{subject}######")
    with open(f'./Assignment1/resourceFiles/corpus4(bs4)/webScraped(query={subject}){today}.csv', 'a') as f:
        for line in contList:
            f.write(f"{strip_ascii(line)}\n") 
    return 'Complete'



def main():
    print('WebScraping Start')
    subject = '\"Nuclear Energy\" risk'
    api_key, endpoint = newsAPI.getArticleURLsParams()
    urls = newsAPI.getArticleURLs(api_key, endpoint, subject, retSources=True)
    sources1 = [x[0] for x in urls]
    urls = [x[1] for x in urls]   
    cont = urlsToTxt(urls, 50)
    writeToFile(cont, subject.replace('\"',''))

    print('WebScraping Start')
    subject = '\"Nuclear Energy\" safe'
    api_key, endpoint = newsAPI.getArticleURLsParams()
    urls = newsAPI.getArticleURLs(api_key, endpoint, subject, retSources=True)
    sources2 = [x[0] for x in urls]
    urls = [x[1] for x in urls]   
    cont = urlsToTxt(urls, 50)
    writeToFile(cont, subject.replace('\"',''))

    # print(cont)
    joinLabeledData('Assignment1\\resourceFiles\\corpus4(bs4)\\webScraped(query=Nuclear Energy risk)2024-03-01.csv', 'risk',
                    'Assignment1\\resourceFiles\\corpus4(bs4)\\webScraped(query=Nuclear Energy safe)2024-03-01.csv', 'safe',
                     'Assignment1\\resourceFiles\\corpus4(bs4)\\webScrapedLabeledSources(query=Nuclear Energy)risk.csv', sources = [sources1,sources2])
    #content=urlToText('https://www.wired.com/story/global-emissions-could-peak-sooner-than-you-think/')

    #content2 = urlToText('https://www.androidcentral.com/phones/betavolt-technology-developing-radionuclide-battery')

    print("-------------------------")
    #print(content)
    #print(content2)

if __name__ == "__main__":
    main()