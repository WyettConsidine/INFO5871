from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from textProcessing import textProcessor
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA



def cleanEmptyLines(filePath):
    with open(filePath, 'r') as f:
        cleanedLines = []
        for line in f:
            if line.split(",", 2)[2] == '\n':
                continue
            else:
                cleanedLines.append(line)
        f.close()
    newFilePath = filePath.replace('.csv','')+' cleaned.csv'
    with open(newFilePath, 'w') as f:
        for line in cleanedLines:
            f.write(line)
        f.close()

def readInAndProcessText(filepath):
    print(f"Reading in {filepath}")
    tfidfDF, _ = textProcessor(filepath,
                                     textType='content', contentOrigin= 'scraped', stemORlem='neither', 
                                     countORtfidf='tfidf', sources = True, labeled=True, maxFeatures=15, max_df = .8, min_df = .3)
    print(f"From File: {tfidfDF}")
    return tfidfDF

def stripLabelandSource(tfidfDF):
    labelsAndSources = []
    vectors = []
    vectorDim = len(tfidfDF.columns)-2
    for key, vals in tfidfDF.iterrows():
        labelsAndSources.append((vals[0],vals[1]))
        vectors.append(vals[2:vectorDim])
    return labelsAndSources, vectors

def applyKMeans(vectors, labelsASources, clusters):
    kmeans = KMeans(n_clusters=clusters, random_state=0, n_init="auto").fit(vectors)
    clustLabels = kmeans.labels_
    centers = kmeans.cluster_centers_

    lsClustered = list(zip(labelsASources,clustLabels))
    return lsClustered, centers

def LabeledToDF(lsClustered):
    labels = []
    sources = []
    cluster = []
    for point in lsClustered:
        labels.append(point[0][0])
        sources.append(point[0][1])
        cluster.append(point[1])
    df = pd.DataFrame({'Labels':labels, 'Sources':sources, 'Cluster Label': cluster})

    return df


def visClusters2D(centers, vectors, LSCDF):
    print("visualizations")
    pca = PCA(n_components=2)
    points = pca.fit_transform(vectors)
    pcaCenters = pca.transform(centers)
    print(points)
    LSCDF['x'] = [x[0] for x in points]
    LSCDF['y'] = [x[1] for x in points]
    print(LSCDF)
    unique_labels = LSCDF['Cluster Label'].unique()
    colors = ['y', 'c', 'm', 'r', 'g', 'b']
    for i, label in enumerate(unique_labels):
        cluster_data = LSCDF[LSCDF['Cluster Label'] == label]
        plt.scatter(cluster_data['x'], cluster_data['y'], c=colors[i], label=f"Cluster {label}")
    pcaCentersX = [x[0] for x in pcaCenters]
    pcaCentersY = [x[1] for x in pcaCenters] 
    plt.scatter(x=pcaCentersX, y=pcaCentersY, color = 'black', label='K-Means Centroids')
    plt.legend(loc="upper left")
    plt.xlabel("PCA1")
    plt.ylabel("PCA2")
    plt.title(f"2D Cluster Projections to Analyze K-Means Partitions \n Number of Clusters: {len(unique_labels)}")
    plt.show()

def main():
    print("main")
    #cleanEmptyLines('Assignment1\\resourceFiles\\corpus4(bs4)\\webScrapedLabeledSources(query=Nuclear Energy)risk.csv')

    tfidfVects = readInAndProcessText('Assignment1\\resourceFiles\\corpus4(bs4)\\webScrapedLabeledSources(query=Nuclear Energy)risk cleaned.csv')
    tfidfVects.to_csv('Assignment1\\resourceFiles\\tfidfData.csv')
    # labelsASources, vectors = stripLabelandSource(tfidfVects)
    # lsClustered, centers = applyKMeans(vectors, labelsASources, 2)
    # LSCDF = LabeledToDF(lsClustered)
    # clusterLabels = LSCDF['Cluster Label'].unique()
    # print(LSCDF.columns)
    # for cl in clusterLabels:
    #     print(f"Length of cluster {cl} = {len(LSCDF[LSCDF['Cluster Label'] == cl])}")
    # visClusters2D(centers, vectors, LSCDF)


if __name__ == "__main__":
    main()
    