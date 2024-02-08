from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import pandas as pd
import numpy as np 
import os
import re


def articleCorpusVectorizer(FolderDir, stemORlem = {'stemmer', 'lemmer', 'neither'}, maxFeatures = 30, max_df=1, min_df=1):
    filenameList = os.listdir(FolderDir)
    filenameList = [FolderDir+'/'+file for file in filenameList]
    #print(filenameList)
    if stemORlem == 'lemmer':
        LEMMER = WordNetLemmatizer()
        def lemFunc(str_input):
            words = re.sub(r'[^A-Za-z]',' ',str_input).lower().split()
            words= [LEMMER.lemmatize(word) for word in words]
            return words
        vectorizer = CountVectorizer(input = 'filename', 
                                     stop_words='english', 
                                     lowercase = True, 
                                     tokenizer = lemFunc,
                                     max_features = maxFeatures, 
                                     max_df=max_df,
                                     min_df=min_df )
    elif stemORlem == 'stemmer':
        STEMMER = PorterStemmer()
        def stemFunc(str_input):
            words = re.sub(r'[^A-Za-z]',' ',str_input).lower().split()
            words= [STEMMER.stem(word) for word in words]
            return words
        vectorizer = CountVectorizer(input = 'filename', 
                                     stop_words='english', 
                                     lowercase = True, 
                                     tokenizer = stemFunc,
                                     max_features = maxFeatures,
                                     max_df=max_df,
                                     min_df=min_df )
    else:
        vectorizer = CountVectorizer(input = 'filename', 
                                     stop_words='english', 
                                     lowercase = True, 
                                     max_features = maxFeatures, 
                                     max_df=max_df, 
                                     min_df=min_df )

    output = vectorizer.fit_transform(filenameList)
    vocab = vectorizer.get_feature_names_out()
    countVecDF = pd.DataFrame(output.toarray(), columns=vocab)
    for word in vocab:
        if any(char.isdigit() for char in word) | (len(word) <= 2):
            countVecDF= countVecDF.drop(columns= [word],)               
    
    return countVecDF, vectorizer


def contentVectorizer(filePath, maxFeatures = 30, inputOrigin = {'arXiv', 'newsAPI', 'scraped'}, stemORlem = {'stemmer', 'lemmer', 'neither'}, max_df=1, min_df=1):
    if inputOrigin == 'arXiv':
        contentDF = pd.read_csv (filePath)
        content = contentDF['summary'].values[1:]
    elif inputOrigin == 'newsAPI':
        with open(filePath) as file:
            content = [line.strip() for line in file]
    elif inputOrigin == 'scraped':
        with open(filePath) as file:
            content = [line.strip() for line in file]
    else:
        print("enter valid input origin")
        return None    

    if stemORlem == 'lemmer':
        LEMMER = WordNetLemmatizer()
        def lemFunc(str_input):
            words = re.sub(r'[^A-Za-z]',' ',str_input).lower().split()
            words= [LEMMER.lemmatize(word) for word in words]
            return words
        vectorizer = CountVectorizer(input = 'content', 
                                     stop_words='english', 
                                     lowercase = True, 
                                     tokenizer = lemFunc, 
                                     max_features = maxFeatures, 
                                     max_df=max_df, 
                                     min_df=min_df )
    elif stemORlem == 'stemmer':
        STEMMER = PorterStemmer()
        def stemFunc(str_input):
            words = re.sub(r'[^A-Za-z]',' ',str_input).lower().split()
            words= [STEMMER.stem(word) for word in words]
            return words
        vectorizer = CountVectorizer(input = 'content', 
                                     stop_words='english', 
                                     lowercase = True, 
                                     tokenizer = stemFunc, 
                                     max_features = maxFeatures, 
                                     max_df=max_df, 
                                     min_df=min_df )
    else:
        vectorizer = CountVectorizer(input = 'content', 
                                     stop_words='english', 
                                     lowercase = True, 
                                     max_features = maxFeatures, 
                                     max_df=max_df, 
                                     min_df=min_df )

    output = vectorizer.fit_transform(content)
    vocab = vectorizer.get_feature_names_out()
    countVecDF = pd.DataFrame(output.toarray(), columns=vocab)
    print(len(countVecDF.columns))
    for word in vocab:
        if any(char.isdigit() for char in word)| (len(word) <= 2):
            countVecDF= countVecDF.drop(columns= [word],)
               
    print(len(countVecDF.columns))
    
    return countVecDF, vectorizer

def ArticleTfidfVectorizer(FolderDir, maxFeatures = 30):
    filenameList = os.listdir(FolderDir)
    filenameList = [FolderDir+'/'+file for file in filenameList]
    tfidfVect = TfidfVectorizer(input='filename', stop_words="english", max_features=maxFeatures)
    Vect = tfidfVect.fit_transform(filenameList)
    vocab = tfidfVect.get_feature_names_out()
    tfidfVecDF = pd.DataFrame(Vect.toarray(),columns=vocab)
    for word in vocab:
        if any(char.isdigit() for char in word) | (len(word) <= 2):
            countVecDF= countVecDF.drop(columns= [word],)               
    
    return tfidfVecDF, tfidfVect


def textProcessor(filepath,
                   textType={'content', 'corpus'},
                   contentOrigin = {'arXiv', 'newsAPI', 'scraped'}, 
                   stemORlem = {'stemmer', 'lemmer'}, 
                   countORtfidf = {'count', 'tfidf'}, maxFeatures = 30, max_df=1, min_df=1  ):
    if textType == 'content':
        output, vectorizer = contentVectorizer(filepath,maxFeatures,contentOrigin,stemORlem,max_df,min_df)
    elif textType == 'corpus':
        if countORtfidf == 'count':
            output, vectorizer = articleCorpusVectorizer(filepath, stemORlem, maxFeatures, max_df, min_df)
        elif countORtfidf == 'tfidf':
            output, vectorizer = ArticleTfidfVectorizer(filepath, maxFeatures)
        else:
            print('Select valid vectorization type. (count or tfidf)')
            output = None
            vectorizer = None
    else:
        print('Select valid text processing type.')
        output = None
        vectorizer = None
    return output, vectorizer

def main():
    print('Text Processing Start')
    # outputArtCorpus, _ = textProcessor('./resourceFiles/corpus1(manual)', textType='corpus', countORtfidf='count', stemORlem='lemmer')
    # print(outputArtCorpus)

    # outputarXiv, _ = textProcessor('./resourceFiles/corpus2(arXiv)/arXivData(query=nuclear energy)2024-01-30.csv', textType='content', contentOrigin= 'arXiv', stemORlem='stemmer', maxFeatures=20)
    # print(outputarXiv)

    # outputNewsAPI, _ = textProcessor('./resourceFiles/corpus3(newsAPI)/newsapiData(query=nuclear energy)2024-01-30.csv', textType='content', contentOrigin= 'newsAPI', stemORlem='lemmer', maxFeatures=20)
    # print(outputNewsAPI)

    outputScrape, _ = textProcessor('./resourceFiles/corpus4(bs4)/webScraped(query=nuclear energy)2024-02-06.csv', textType='content', contentOrigin= 'scraped', stemORlem='stemmer', maxFeatures=20, max_df = 5, min_df = 2)
    print(outputScrape)


    # outputSt, dirVectorizer = articleCorpusVectorizer('./resourceFiles/corpus1(manual)', stemORlem='stemmer')
    # outputL, dirVectorizer = articleCorpusVectorizer('./resourceFiles/corpus1(manual)', stemORlem='lemmer')
    # print(outputSt.columns)
    # print(outputL.columns)

    
    # output2St, contVectorizer = contentVectorizer('./resourceFiles/corpus2(arXiv)/arXivData(query=nuclear energy)2024-01-30.csv', inputOrigin = 'arXiv', stemORlem='stemmer')
    # output2L, contVectorizer = contentVectorizer('./resourceFiles/corpus2(arXiv)/arXivData(query=nuclear energy)2024-01-30.csv', inputOrigin = 'arXiv', stemORlem='lemmer')
    # print(output2St.columns)
    # print(output2L.columns)

    # output3St, contVectorizer = contentVectorizer('./resourceFiles/corpus3(newsAPI)/newsapiData(query=nuclear energy)2024-01-30.csv', inputOrigin = 'newsAPI', stemORlem='stemmer')
    # output3L, contVectorizer = contentVectorizer('./resourceFiles/corpus3(newsAPI)/newsapiData(query=nuclear energy)2024-01-30.csv', inputOrigin = 'newsAPI', stemORlem='lemmer')
    # print(output3St.columns)
    # print(output3L.columns)

    # output = ArticleTfidfVectorizer('./resourceFiles/corpus1(manual)')
    # print(output)

if __name__ == "__main__":
    main()
    
    

    