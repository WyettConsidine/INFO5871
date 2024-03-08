
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from textProcessing import textProcessor

#######

#MyVectLDA_DH=CountVectorizer(input='filename')
##path="C:\\Users\\profa\\Documents\\Python Scripts\\TextMining\\DATA\\SmallTextDocs"
#Vect_DH = MyVectLDA_DH.fit_transform(ListOfCompleteFiles)
#ColumnNamesLDA_DH=MyVectLDA_DH.get_feature_names()
#CorpusDF_DH=pd.DataFrame(Vect_DH.toarray(),columns=ColumnNamesLDA_DH)
#print(CorpusDF_DH)

######


def readInAndProcessText(filepath):
    print(f"Reading in {filepath}")
    
    vectPD, vectorizer = textProcessor(filepath,
                                     textType='content', contentOrigin= 'newsAPI', stemORlem='lem', 
                                     countORtfidf='tfidf', sources = False, labeled=True, maxFeatures=100, max_df = 100, min_df = 10)
    print(f"From File: {vectPD}")
    return vectPD, vectorizer


def LDA(num_topics, countVectDF):
    lda_model_DH = LatentDirichletAllocation(n_components=num_topics, 
                                         max_iter=100, learning_method='online')
    LDA_DH_Model = lda_model_DH.fit_transform(countVectDF)
    print("SIZE: ", LDA_DH_Model.shape)  # (NO_DOCUMENTS, NO_TOPICS)
    # Let's see how the first document in the corpus looks like in
    ## different topic spaces
    print("First headline...")
    print(LDA_DH_Model[0])
    print("Sixth headline...")
    print(LDA_DH_Model[5])
    #print(lda_model_DH.components_)
    print(type(LDA_DH_Model))
    return LDA_DH_Model, lda_model_DH

## implement a print function 
## REF: https://nlpforhackers.io/topic-modeling/
def print_topics(model, vectorizer, top_n=10):
    for idx, topic in enumerate(model.components_):
        print("Topic:  ", idx)    
        print([(vectorizer.get_feature_names_out()[i], topic[i])
                        for i in topic.argsort()[:-top_n - 1:-1]])
                        ## gets top n elements in decreasing order


## Print LDA using print function from above
########## Other Notes ####################
#import pyLDAvis.sklearn as LDAvis
#import pyLDAvis
#import pyLDAvis.gensim 
## conda install -c conda-forge pyldavis
#pyLDAvis.enable_notebook() ## not using notebook
#panel = LDAvis.prepare(lda_model_DH, MyDTM_DF, MyCountV, mds='tsne')
#pyLDAvis.show(panel)
#panel = pyLDAvis.gensim.prepare(lda_model_DH, MyDTM, MyCountV, mds='tsne')
#pyLDAvis.show(panel)
##########################################################################

import matplotlib.pyplot as plt
import numpy as np

def plotLDA(lda_model_DH, vocab, num_topics):
    word_topic = np.array(lda_model_DH.components_)
    #print(word_topic)
    word_topic = word_topic.transpose()

    num_top_words = 15
    vocab_array = np.asarray(vocab)

    #fontsize_base = 70 / np.max(word_topic) # font size for word with largest share in corpus
    fontsize_base = 20
    
    for t in range(num_topics):
        plt.subplot(1, num_topics, t + 1)  # plot numbering starts with 1
        plt.ylim(0, num_top_words + 0.5)  # stretch the y-axis to accommodate the words
        plt.xticks([])  # remove x-axis markings ('ticks')
        plt.yticks([]) # remove y-axis markings ('ticks')
        plt.title('Topic #{}'.format(t))
        top_words_idx = np.argsort(word_topic[:,t])[::-1]  # descending order
        top_words_idx = top_words_idx[:num_top_words]
        top_words = vocab_array[top_words_idx]
        top_words_shares = word_topic[top_words_idx, t]
        for i, (word, share) in enumerate(zip(top_words, top_words_shares)):
            plt.text(0.3, num_top_words-i-0.5, word, fontsize=fontsize_base)
                    ##fontsize_base*share)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # num_topics = 5
    # countVectDF, MyCountV = readInAndProcessText('testDataLabeled.csv')
    # lda_model_DH, lda_mod = LDA(num_topics,countVectDF.drop(['Label'], axis = 1).drop(['Source'], axis = 1))
    # print_topics(lda_mod, MyCountV, 15)
    # plotLDA(lda_mod, MyCountV.get_feature_names_out(), num_topics)

    num_topics = 3
    countVectDF, MyCountV = readInAndProcessText('testDataLabeled.csv')
    lda_model_DH, lda_mod = LDA(num_topics,countVectDF.drop(['Label'], axis = 1))
    print_topics(lda_mod, MyCountV, 15)
    plotLDA(lda_mod, MyCountV.get_feature_names_out(), num_topics)