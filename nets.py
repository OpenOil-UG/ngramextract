import nltk
import string
from nltk.corpus import stopwords
import itertools
import csv
import glob
import os
import re
import logging

## need to download within the nltk.download window:
# models/punkt
# corpora/stopwords

class NgramGenerator(object):
    
    MAX_FILES = 99999

    def __init__(self, *args, **kwargs):
        self.ngram_dict = {}
        self.doc_dict = {}
        self.ngram_ids, self.doc_ids = itertools.count(1), itertools.count(1)

    def iterate_files(self):
        # (filenames)
        return glob.glob(self.input_filepattern)[:self.MAX_FILES]

    def ngrams_from_file(self, filename):
        text = open(filename).read()
        text = text.lower()
        text = re.sub(r'[^\w ]', '', text)
        words = nltk.word_tokenize(text)
        stops = stopwords.words('english')
        words = [x for x in words if x not in stops]
        trigrams = nltk.trigrams(words)
        return trigrams

    def add_ngrams(self, trigrams):
        with open(self.fn_ngrams, 'a+') as fh:
            dest = csv.writer(fh)
            dest.writerows(trigrams)        

    def final_output(self):
        with open(self.fn_docdict, 'w') as fh:
            dest = csv.writer(fh)
            dest.writerows(self.doc_dict.items())
        with open(self.fn_ngramdict, 'w') as fh:
            dest = csv.writer(fh)
            ngrams = sorted((y, ' '.join(x)) for (x,y) in self.ngram_dict.items())
            dest.writerows(ngrams)        
                
    def run(self):
        if os.path.exists(self.fn_ngrams):
            os.unlink(self.fn_ngrams)

        for fn in self.iterate_files():
            logging.warn('on %s' % fn)
            filenum = next(self.doc_ids)
            self.doc_dict[filenum] = fn

            new_ngrams = []
            for location, trigram in enumerate(self.ngrams_from_file(fn)):
                if trigram in self.ngram_dict:
                    tg_num = self.ngram_dict[trigram]
                else:
                    tg_num = next(self.ngram_ids)
                    self.ngram_dict[trigram] = tg_num
                new_ngrams.append([filenum, tg_num, location])
            self.add_ngrams(new_ngrams)
        self.final_output()

        
class BPNGrams(NgramGenerator):
    fn_ngramdict = '/tmp/bp_ngram_ids.csv'
    fn_docdict = '/tmp/bp_doc_ids.csv'
    fn_ngrams = '/tmp/bp_ngrams.csv'

    input_filepattern = '/home/src/oonetworks/data/bp/*txt'
    input_filepattern = '/data/openoil/source/filings/us_edgar/edgar_filings_text/313807/*txt'
    
if __name__ == '__main__':
    ng = BPNGrams()
    ng.run()
