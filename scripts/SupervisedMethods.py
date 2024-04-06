import pandas as pd
import numpy as np
 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, auc, roc_curve
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.tree import export_graphviz
from sklearn.svm import SVC
import graphviz 

import matplotlib.pyplot as plt


#Get TFIDF data from file
def grabData(filePath):
    tfidf = pd.read_csv(filePath, index_col = 0)
    #tfidf = tfidf.drop('Source', axis = 1)
    return tfidf

#Remove, but keep lables. Separate into 2 lists
def splitLabels(trainDF1):
    trainLabs = trainDF1['Label']
    trainDF1 = trainDF1.drop('Label', axis = 1)
    return trainDF1, trainLabs


#Separate training and test data based on test_size.
#(test_size = .2 would separate 80% into the training set, and 20% into test set)
#Split the data into 4 parts:
#    Training data without labels  (noLabTrain)
#    Labels of training set  (LabTrain)
#    Test data without labels (noLabTest)
#    Labels of test set  (LabTest)
# Return 4 parts
def splitData(dataDF, test_size = .2):
    #Split data into train/test
    TrainDF1, TestDF1 = train_test_split(dataDF, test_size=test_size)
    #Split labels from train/test sets
    noLabTest, LabTest = splitLabels(TestDF1)
    noLabTrain, LabTrain = splitLabels(TrainDF1)
    #return lists
    return noLabTrain, LabTrain, noLabTest, LabTest


############  Naive Bayes Section ###################
#Train a NB model with trianing data, and predict the labels. 
def trainNB(noLabTrain, trainLabs, noLabTest):
    #intstantiate NB
    MyModelNB = MultinomialNB()
    #fit data to NB
    NB = MyModelNB.fit(noLabTrain, trainLabs)
    #predict labels
    Preds = MyModelNB.predict(noLabTest)
    return NB, Preds

#######################################


###### Descision Tree Section ################
#train a DT model. Fit with training data, and return predicted labels
def trainDT(noLabTrain, trainLabs, noLabTest):
    #instatiate a DT object with input parameters
    DT=DecisionTreeClassifier(criterion='entropy',
                            splitter='best',
                            max_depth=None, 
                            min_samples_split=2, 
                            min_samples_leaf=1, 
                            min_weight_fraction_leaf=0.0, 
                            max_features=None, 
                            random_state=None, 
                            max_leaf_nodes=None, 
                            class_weight=None)
    #fit DT obj to training data
    DT.fit(noLabTrain, trainLabs)
    #predict test labels
    Preds = DT.predict(noLabTest)
    return DT, Preds

#Create a Visualizetion of the DT given the DT model
def dispTree(DT, tfidf, figName, saveImg = False):
    tree.plot_tree(DT)
    if saveImg:
        plt.savefig(figName)
    #Create a tree object with the DT model, input data, and parameters 
    dot_data = tree.export_graphviz(DT, out_file=None,
                    #The following creates TrainDF.columns for each
                    #which are the feature names.
                      feature_names=tfidf.columns,  
                      #class_names=MyDT.class_names,  
                      filled=True, rounded=True,  
                      special_characters=True)
    #Use graphviz to plot the tree object                             
    graph = graphviz.Source(dot_data) 
    ## Create dynamic graph name
    tempname=str(figName)
    #render the tree
    graph.render(tempname) 
##############################################



#### Support Vector Machines ################
    
#create and train SVM. Use to predict test labels
def trainSVM(noLabTrain, trainLabs, noLabTest):
    #create SVM model with soft margins, cost = C
    clf = SVC(C=1, kernel="poly", degree = 2, verbose=False)
    #fit the model with the training data
    clf.fit(noLabTrain, trainLabs)
    #predict the test labels
    preds = clf.predict(noLabTest)
    return clf, preds

############################################


#Get the averaged accuracy of input Sup Learning Model
#training func is the specified supervised learning model, ie trainNB()
#Normalize accuracy results over n tests. (default 20)
def getAvgAcc(tfidf, trainingFunc, tests = 20):
    sumAcc = 0
    #sum accuracy over n tests, each time getting a different train/test set
    for i in range(tests):
        noLabTrain, LabTrain, noLabTest, LabTest = splitData(tfidf)
        #train specified model
        _, preds = trainingFunc(noLabTrain, LabTrain, noLabTest)
        #add acc to running sumation
        sumAcc += accuracy_score(LabTest,preds)
    #normalize by num tests and return
    return sumAcc/tests



def displayConfMat(tfidf, modelName, trainingFunction, tests = 1):
    accSum = 0
    for i in range(tests):
        noLabTrain, LabTrain, noLabTest, LabTest = splitData(tfidf)
        model, preds = trainingFunction(noLabTrain, LabTrain, noLabTest)
        cm = confusion_matrix(LabTest, preds, labels= model.classes_)
        if i == 0:
            cmSum = cm
        else:
            cmSum = np.add(cmSum,cm)
        accSum += accuracy_score(LabTest,preds)
    acc = accSum/tests
    cm = cmSum/tests
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                display_labels=model.classes_)
    disp.plot()
    plt.title(f'Confusion Matrix of {modelName} Model \n Accuracy = {np.round(acc,2)}')
    plt.show()

def compareSupLearnMods(modNames, trainingFunctions, tfidf, numTests = 20):
    predTrueLabLists = []
    for model in trainingFunctions:
        noLabTrain, LabTrain, noLabTest, LabTest = splitData(tfidf)
        _, preds = model(noLabTrain, LabTrain, noLabTest)
        predTrueLabLists.append([LabTest.values, preds])
    aucList = []
    labelDict = {'safe':1,'risk':0}
    for t in range(numTests):
        for i in range(len(modNames)):
            #print(predTrueLabLists[i][0],predTrueLabLists[i][1])
            y = [labelDict[l] for l in predTrueLabLists[i][0]]
            pred = [labelDict[l] for l in predTrueLabLists[i][1]]
            fpr, tpr, thresholds = roc_curve(y,pred)
            #print(auc(fpr, tpr))
            if t == 0:
                aucList.append((modNames[i], auc(fpr, tpr)))
            else:
                #print(aucList[i])
                aucList[i] = (aucList[i][0], aucList[i][1] + auc(fpr, tpr))
    aucList = [(aucVal[0],aucVal[1]/t) for aucVal in aucList]
    aucList.sort(key = lambda x: x[1],reverse = True)
    return aucList

if __name__ == '__main__' :
    tfidf = grabData('resourceFiles/tfidfData.csv')
    
    #os.environ["PATH"] += os.pathsep + 'C:\\Users\\wyett\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\graphviz'

    #NB model
    #displayConfMat(tfidf, 'Naive Bayes', trainNB)

    #DT Models:
    #displayConfMat(tfidf, 'Desicion Tree', trainDT)

    ###Run only on WSL!!
    # noLabTrain, LabTrain, noLabTest, LabTest = splitData(tfidf)
    # DT, preds = trainDT(noLabTrain, LabTrain, noLabTest)
    # dispTree(DT, noLabTrain, 'Descition Tree Model')

    #SVM Models:
    #displayConfMat(tfidf, "Support Vector Machine", trainSVM)

    #AUC:
    modelNames = ['Naive Bayes', 'Desicion Tree', 'Support Vector Machine']
    trainingFunctions = [trainNB,trainDT,trainSVM]
    results= compareSupLearnMods(modelNames,trainingFunctions, tfidf)
    print('AUC comparison across all supervised learning models:')
    for result in results:
        print(f'Model: {result[0]}. AUC Score: {result[1]}')



