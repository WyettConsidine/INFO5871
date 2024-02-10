from bs4 import BeautifulSoup
import newsAPI
import requests
from datetime import date

def urlToText(url):
    #Use requests library to pull in HTML response
    page = requests.get(url)
    #Use Beautiful Soup library to parse HTML
    print(page.content)
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

def joinLabeledData(filePath1, l1, filePath2, l2, newFilePath):
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
    with open(f'./Assignment1/resourceFiles/corpus4(bs4)/webScraped(query={subject}){today}.csv', 'a') as f:
        for line in contList:
            f.write(f"{strip_ascii(line)}\n") 
    return 'Complete'



def main():
    # print('WebScraping Start')
    # subject = '\"Nuclear Energy\" sustainable'
    # api_key, endpoint = newsAPI.getArticleURLsParams()
    # urls = newsAPI.getArticleURLs(api_key, endpoint, subject)
    # cont = urlsToTxt(urls, 20)
    # writeToFile(cont, subject.replace('\"',''))

    # subject = '\"Nuclear Energy\" unsustainable'
    # api_key, endpoint = newsAPI.getArticleURLsParams()
    # urls = newsAPI.getArticleURLs(api_key, endpoint, subject)
    # cont = urlsToTxt(urls, 20)
    # writeToFile(cont, subject.replace('\"',''))
    # # print(cont)
    # joinLabeledData('Assignment1\\resourceFiles\\corpus4(bs4)\\webScraped(query=Nuclear Energy sustainable)2024-02-09.csv', 'sustainable',
    #                 'Assignment1\\resourceFiles\\corpus4(bs4)\\webScraped(query=Nuclear Energy unsustainable)2024-02-09.csv', 'unsustainble',
    #                  'Assignment1\\resourceFiles\\corpus4(bs4)\\webScrapedLabeled(query=Nuclear Energy)sustainability')
    content=urlToText('https://www.wired.com/story/global-emissions-could-peak-sooner-than-you-think/')

    #content2 = urlToText('https://www.androidcentral.com/phones/betavolt-technology-developing-radionuclide-battery')

    print("-------------------------")
    #print(content)
    #print(content2)

if __name__ == "__main__":
    main()