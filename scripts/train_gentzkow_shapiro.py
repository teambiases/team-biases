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
from itertools import tee
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
            print(sys.argv[3:])
            langs = sys.argv[3:]
            outfile = sys.argv[-1]
            e0lang = langs[0]
            e1lang = langs[1]

            e0rawiter, e1rawiter = e0.read(), e1.read()
            wordfind = re.compile('\w+').findall
            e0rawiter, e1rawiter = wordfind(e0rawiter),wordfind(e1rawiter)
            bigram0, bigram1 = ngrams(e0rawiter,2), ngrams(e1rawiter,2)
            trigram0, trigram1 = ngrams(e0rawiter,3),ngrams(e1rawiter,3)

            #this is only for size reduction
            def g(x):
                for y in x:
                    yield y
            bigram0, bigram1, trigram0, trigram1 = g([x for x in bigram0][:100]),g([x for x in bigram1][:100]),g([x for x in trigram0][:100]),g([x for x in trigram1][:100])
            (bigram0,b0) , (bigram1, b1), (trigram0, t0), (trigram1, t1) = tee(bigram0), tee(bigram1), tee(trigram0), tee(trigram1)
            lang_ngrams = [(e0lang," ".join(bi)) for bi in bigram0] + [(e0lang," ".join(tri)) for tri in trigram0] + [(e1lang," ".join(bi)) for bi in bigram1] + [(e1lang," ".join(tri)) for tri in trigram1] 
            translate_iter = {lang:[] for lang in langs}
            for item in list(set(lang_ngrams)):
                translate_iter[item[0]].append(item[1])

            translate_pack = [(lang,translate_iter[lang]) for lang in translate_iter]
            alignment,lookup = align_ngrams(translate_pack)
            gs = GentzkowShapiro(alignment,lookup)
            params = b0,b1,t0,t1,langs,langs.index('en')

            gs.train(params)

            #....
            #.... TODO?






            

