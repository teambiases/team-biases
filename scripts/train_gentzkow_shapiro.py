"""
train_gentzkow_shapiro.py

Given endpoint0 at data/endpoints/something... and endpoint1 at data/endpoints/somethingelse...
read in the endpoint data, create n-grams up to 3-grams, and perform a chi^2 analysis on each
of them.
The main correlation algorithm is:


pl = (fplr*cfpld-fpld*cfplr)^2/
(fplr + fpld)(fplr + cfplr)(fpld + cfpld)(cfplr + cfpld)
"""
import _path_config
from biases.bias.gs import align_ngrams, GentzkowShapiro
import sys
import re
from nltk.util import ngrams

if __name__ == '__main__':
    if len(sys.argv) <= 4:
        print('Usage: python3 train_gentzkow_shapiro.py <endpoint0> <endpoint1> <lang0> <lang1> <...lang1> <out_file>')
        print('Uses endpoints stored at <endpoint0> and <endpoint1>')
        print('and computes the Gentzkow-Shapiro algorithm, outputting <out_file> pickle file for the phrases')
    else:
        with open(sys.argv[1], 'r') as e0, open(sys.argv[2], 'r') as e1:
            langs = sys.argv[3:-1]
            outfile = sys.argv[-1]
            e0lang = langs[0]
            e1lang = langs[1]

            e0rawiter, e1rawiter = e0.read(), e1.read()
            wordfind = re.compile('\w+').findall
            e0rawiter, e1rawiter = wordfind(e0rawiter),wordfind(e1rawiter)
            bigram0, bigram1 = ngrams(e0rawiter,2), ngrams(e1rawiter,2)
            trigram0, trigram1 = ngrams(e0rawiter,3),ngrams(e1rawiter,3)
            lang_ngrams = [(e0lang,bi) for bi in bigram0] + [(e0lang,tri) for tri in trigram0] + [(e1lang,bi) for bi in bigram1] + [(e1lang,tri) for tri in trigram1] 
            num_grams = len(lang_ngrams)
            smaller_sample = lang_ngrams[0:100] + lang_ngrams[round(num_grams/4):round(num_grams/4+100)] + lang_ngrams[round(num_grams/2):round(num_grams/2+100)] + lang_ngrams[round(3*num_grams/4):round(3*num_grams/4+100)]
            alignment,lookup = align_ngrams(smaller_sample)
            gs = GentzkowShapiro(alignment,lookup)
            params = bigram0,bigram1,trigram0,trigram1,langs,langs.index('en')

            gs.train(params)

            #....
            #.... TODO?






            

