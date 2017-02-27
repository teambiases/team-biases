"""
train_gentzkow_shapiro.py

Given endpoint0 at data/endpoints/something... and endpoint1 at data/endpoints/somethingelse...
read in the endpoint data, create n-grams up to 3-grams, and perform a chi^2 analysis on each
of them.
The main correlation algorithm is:


pl = (fplr*cfpld-fpld*cfplr)^2/
(fplr + fpld)(fplr + cfplr)(fpld + cfpld)(cfplr + cfpld)
"""
from nltk.util import ngrams
from collections import Counter
import itertools
import sys
import os
import re

def c2_calculate(args):
    c2 = {}
    amalgamated,corp0,corp1 = args
    ref0,ref1 = Counter(corp0), Counter(corp1)
    tpl0,tpl1 = len(corp0), len(corp1)
    for gram in amalgamated:
        if gram not in c2:
            if gram not in ref0:
                fpl0 = 0
            else:
                fpl0 = ref0[gram]
            if gram not in ref1:
                fpl1 = 0
            else:
                fpl1 = ref1[gram]
            cfpl0 = tpl0-fpl0
            cfpl1 = tpl1-fpl1
            chi2 = (fpl0*cfpl1 - fpl1*cfpl0)**2/((fpl0 + fpl1)*(fpl0 + cfpl0)*(fpl1 + cfpl1)*(cfpl0 + cfpl1))
            c2[gram]=([gram, chi2, fpl0, fpl1])
            print(gram, chi2, fpl0, fpl1)
    
    return c2

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 train_gentzkow_shapiro.py <endpoint0> <endpoint1> <out_file>')
        print('Uses endpoints stored at <endpoint0> and <endpoint1>')
        print('and computes the Gentzkow-Shapiro algorithm, outputting <out_file> csv for the phrases')
    else:
        with open(sys.argv[1], 'r') as e0, open(sys.argv[2], 'r') as e1:
            #This portion should create the unigrams/bigrams/trigrams/quadgrams
            e0rawiter, e1rawiter = e0.read(), e1.read()
            wordfind = re.compile('\w+').findall
            e0rawiter, e1rawiter = wordfind(e0rawiter),wordfind(e1rawiter)
           
            bigram0, bigram1 = ngrams(e0rawiter,2), ngrams(e1rawiter,2)
            trigram0, trigram1 = ngrams(e0rawiter,3),ngrams(e1rawiter,3)
            
            #We now create a mapping between the bigrams and trigrams with their chi^2 value as well as e0, e1 frequencies
                     
            bigram0 = sorted(bigram0)
            bigram1 = sorted(bigram1)
            trigram0 = sorted(trigram0)
            trigram1 = sorted(trigram1)

            c0 = {}
            c1 = {}
           # c2_calculate(c2values, bigram0+bigram1, bigram0, bigram1)
           # c2_calculate(c2values, trigram0+trigram1, trigram0, trigram1)
            c0,c1 = (c2_calculate((bigram0+bigram1,bigram0,bigram1)),c2_calculate((trigram0+trigram1,trigram0,trigram1)))

        with open(sys.argv[3], 'w') as f:
            total = list(c0.values()) + list(c1.values())
            for line in sorted(total, key= lambda x: x[1], reverse=True):
                f.writelines(','.join([str(x) for x in line])+'\n')

