"""
Find

From input showing the location of ngrams in a file

# doc_id, ngram_id, location
1,5,4
1,6,5
1,7,6
1,8,7
1,9,8
1,10,9
1,11,10
1,12,11
1,13,12
1,14,13
1,15,14

Generate for each pair, an array of the distances between them in one file

"""

import csv
import pandas as pd
import numpy as np
from collections import defaultdict

class PairBuilder(object):

    input_fn = '/tmp/bp_ngrams.csv'
    output_fn = '/tmp/bp_ngram_pairs.csv'
    threshold_distance = 10

    def run(self):
        indata = pd.read_csv(self.input_fn, names = ['doc_id', 'ngram_id', 'position'])
        outdata = defaultdict(list)
        return indata
        
        
        
