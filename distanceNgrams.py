# N-gram connection via frequencies
# ===============

import re
import networkx as nx
import random as ran
import math
import numpy as np
import pylab as P
import matplotlib.pyplot as plt
import string
import csv

from os import path
from wordcloud import WordCloud


#with open('sample_location_pairs.csv') as csvfile:
with open('location_pairs_all_bp_labelled_subset.csv') as csvfile:
    
    reader = csv.reader(csvfile)
    
    G = nx.Graph()
    
    Anew = [];
    OriginalWeights = [];
    for row in reader:
	
	iNode = row[2];
	jNode = row[3];
	
	lengthRow = len(row);
	distances = row[4:lengthRow];
	distances = filter(bool, distances)
	sumDistances = 0;
	N = len(distances);
	for c in range(N):
	    aRow = distances[c];
	    aRowF = float(aRow)
	    sumDistances = sumDistances+aRowF
	
	averageDistance = sumDistances/N;
	#thisAverageDistance = np.sum(distances);
	edgeInfo = [iNode, jNode, averageDistance];
	Anew.append(edgeInfo)
	
	OriginalWeights =[averageDistance];
	
	G.add_weighted_edges_from(Anew)
	
    Anew = np.asarray(Anew)
    AnewNorm = Anew[:, 2];
    
    maxWeight = max(OriginalWeights);
    print(maxWeight)
    
    Anew_normalized = [];
    for row in reader:
	Anew_normalized[i] = OriginalWeights[i]/maxWeight;
    
    Anew[:, 2] = Anew_normalized;
    
    with open("output_test.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(Anew)

    nx.write_gexf(G,"graph_distanceNgrams1_1.gexf")
    
    # Largest connected component
    #graphs = list(nx.connected_component_subgraphs(G))
    Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)
    G0=Gcc[0]
    nx.write_gexf(G0,"graph_distanceNgrams1_1-largestComponent.gexf")
