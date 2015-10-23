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
from itertools import chain, islice

def ichunked(seq, chunksize):
    """Yields items from an iterator in iterable chunks."""
    it = iter(seq)
    while True:
        yield chain([next(it)], islice(it, chunksize-1))

class PairBuilder(object):

    input_fn = '/tmp/bp_ngrams.csv'
    output_fn = '/tmp/bp_ngram_pairs.csv'
    threshold_distance = 10

    def run(self):
        indata = pd.read_csv(self.input_fn, names = ['doc_id', 'ngram_id', 'position'])
        outdata = defaultdict(list)
        sliding_window = ichunked(indata.iterrows(), self.threshold_distance)
        for window in sliding_window:
            # each of these is 10-line segment of the input window
            first = next(window)[1]
            for dist, row in window:
                if row.doc_id != first.doc_id:
                    print('skipping item in different doc')
                    continue
                outdata[(first.ngram_id, row.ngram_id)].append(row.position - first.position)
        self.write_csv(outdata)
        return indata, outdata

    def write_csv(self, outdata):
        with open(self.output_fn, 'w') as outf:
            writer = csv.writer(outf)
            for k,v in outdata.items():
                if len(v) > 1:
                    row = list(k) + v
                    writer.writerow(row)

        
        
        
