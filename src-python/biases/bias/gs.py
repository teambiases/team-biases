"""Bias algorithms from Gentzkow & Shapiro (2010)."""

from biases.utils.translate import translation_client
from nltk.util import ngrams
from collections import Counter
from stop_words import get_stop_words
import pickle
import itertools
import sys
import os
import re

def align_ngrams(lang_ngrams, length_limit=None):
    """
    Aligns ngrams from different languages into groups that are translations
    of one another. The input is expected to be a list of tuples
    (lang, ngrams), where lang is a two-letter language code (say 'en' or 'es')
    and ngrams is a list of ngrams that should be included in the final
    alignment.
    
    This returns a tuple (alignments, lookup). Alignments is a list of
    alignments, where each alignment is a list of (lang, ngram) tuples that
    all have the same meaning. lookup is a dictionary such that
    lookup[lang][ngram] gives a representative tuple of the alignment
    cooresponding to the given ngram in the given language.
    
    If length_limit is specified, then no possible translations longer than that
    length in words will be returned.
    """
    
    langs = [lang for lang, ngrams in lang_ngrams]
    lookup = {lang: {} for lang in langs}
    
    to_translate = set()
    for lang, ngrams in lang_ngrams:
        for ngram in ngrams:
            # Keep everything lowercase
            ngram = ngram.lower()
            lookup[lang][ngram] = [(lang, ngram)]
            to_translate.add((lang, ngram))
    
    while len(to_translate) > 0:
        # Perform translation
        new_to_translate = set()
        for from_lang in langs:
            from_lang_ngrams = [ngram for lang, ngram in to_translate if 
                                lang == from_lang]
            for to_lang in langs:
                if to_lang != from_lang and len(from_lang_ngrams) > 0:
                    to_lang_ngrams = [result['translatedText'] for result in 
                            translation_client.translate(from_lang_ngrams,
                            source_language=from_lang,
                            target_language=to_lang)]
                    for from_lang_ngram, to_lang_ngram in \
                            zip(from_lang_ngrams, to_lang_ngrams):
                        # Keep everything lowercase
                        to_lang_ngram = to_lang_ngram.lower()
                        # Make sure translation is under the length limit
                        if length_limit is None or \
                                len(to_lang_ngram.split()) <= length_limit:
                            from_lang_alignment = \
                                    lookup[from_lang][from_lang_ngram]
                            # If we've already seen this word
                            if to_lang_ngram in lookup[to_lang]:
                                to_lang_alignment = \
                                        lookup[to_lang][to_lang_ngram]
                                # If the alignments aren't already combined...
                                if to_lang_alignment is not \
                                        from_lang_alignment:
                                    # ...combine them
                                    from_lang_alignment.extend(
                                            to_lang_alignment)
                                    for align_lang, align_ngram in \
                                            to_lang_alignment:
                                        lookup[align_lang][align_ngram] = \
                                                from_lang_alignment
                            # If it's a new word
                            else:
                                from_lang_alignment.append((to_lang,
                                                            to_lang_ngram))
                                lookup[to_lang][to_lang_ngram] = \
                                        from_lang_alignment
                                new_to_translate.add((to_lang,
                                                      to_lang_ngram))
        to_translate = new_to_translate
    
    # Build alignments list
    alignment_ids = set()
    alignments = []
    for lang in langs:
        for ngram, alignment in lookup[lang].items():
            if id(alignment) not in alignment_ids:
                alignments.append(alignment)
                alignment_ids.add(id(alignment))
                
    alignment_id2tuple = {}
    for alignment in alignments:
        # Get the first aligned word in each language to make a tuple 
        # representation
        alignment_tuple = []
        for lang in langs:
            for ngram_lang, ngram in alignment:
                if ngram_lang == lang:
                    alignment_tuple.append(ngram)
                    break
        alignment_id2tuple[id(alignment)] = tuple(alignment_tuple)
    tuple_lookup = {lang: {ngram: alignment_id2tuple[id(lookup[lang][ngram])]
                         for ngram in lookup[lang]} for lang in langs}
                
    return alignments, tuple_lookup

class GentzkowShapiro():
    """
    Contains the functions that execute the Gentzkow and Shapiro algorithm
    """
    def __init__(alignment=None,lookup=None,file='model.pkl'):
        """
        The alignment and lookup must already be calculated.
        """
        self.alignment = alignment
        self.lookup = lookup
        self.file = file
        self.bigramc = None
        self.trigramc = None

    def load(file='model.pkl'):
        """
        Loads a model file. 
        """
        loaded = pickle.load(open(self.file,'r'))
        self.alignment,self.bigramc,self.trigramc,self.lookup = [loaded[key] for key in sorted(loaded,keys())]             

    def c2_calculate():
        """
        The main Gentzkow Shaprio distribution calculation
        """
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

    def train(params):
        """
        Given the bigrams and trigrams of the two endpoints, convert them to the
        multilingual collections in the lookup files and perform the Gentzkow
        Shapiro algorithm on them.
        """
        lookup = self.lookup
        bigram0, bigram1, trigram0, trigram1, langs, filter_index = params
        bigram0, bigram1, trigram0, trigram1 =\
            ([[lookup[lang][b] for lang in langs] for b in bigram0],
                [[lookup[lang][b] for lang in langs] for b in bigram1],
                [[lookup[lang][t] for lang in langs] for t in trigram0],
                [[lookup[lang][t] for lang in langs] for t in trigram1])
        #We now create a mapping between the bigrams and trigrams with their chi^2 value as well as e0, e1 frequencies

        self.bigram0 = sorted([x for x in bigram0 if (not x[filter_index][0] in sw and not x[filter_index][-1] in sw)])
        self.bigram1 = sorted([x for x in bigram1 if (not x[filter_index][0] in sw and not x[filter_index][-1] in sw)])
        self.trigram0 = sorted([x for x in trigram0 if (not x[filter_index][0] in sw and not x[filter_index][-1] in sw)])
        self.trigram1 = sorted([x for x in trigram1 if (not x[filter_index][0] in sw and not x[filter_index][-1] in sw)]) 

        # c2_calculate(c2values, bigram0+bigram1, bigram0, bigram1)
        # c2_calculate(c2values, trigram0+trigram1, trigram0, trigram1)
        self.bigramc,self.trigramc = (c2_calculate((self.bigram0+self.bigram1,self.bigram0,self.bigram1)),c2_calculate((self.trigram0+self.trigram1,self.trigram0,self.trigram1)))

        pickle.dump({'alignment':self.alignment,'lookup':self.lookup,'bigramc':self.bigramc,'trigramc':self.trigramc},open(self.file,'wb'))

        #~~~~Now we need to train those frequency lists into a logistic model~~~

        # First we get the frequency lists (this may already exist in the code, if so just replace)
        bigram_freq_list_0 = [self.bigramc[gram][2] for gram in self.bigramc.keys()]
        bigram_freq_list_1 = [self.bigramc[gram][3] for gram in self.bigramc.keys()]
        trigram_freq_list_0 = [self.trigramc[gram][2] for gram in self.trigramc.keys()]
        trigram_freq_list_1 = [self.trigramc[gram][3] for gram in self.trigramc.keys()]

        # Then we create a vector of 1's and 0's that's the size of the 1 and 0 lists
        assign_endpoints = np.hstack((np.ones(len(bigram_freq_list_1)+len(trigram_freq_list_1)),np.zeros(len(bigram_freq_list_0)+len(trigram_freq_list_0))))  
        print(assign_endpoints.size())
        # Combine the frequency lists into a single frequency vector the same size as 'assign_endpoints'
        frequency_vector = np.concatenate((bigram_freq_list_1,trigram_freq_list_1,bigram_freq_list_0,trigram_freq_list_0))
        print(frequency_vector.size())

        # Now MAKE. THAT. MODELLLLL
        model = make_pipeline(VarianceThreshold(), LogisticRegression())
        self.log_model = model.fit(frequency_vector,assign_endpoints)

        pickle.dump(self.log_model,open('GSlog_model.pickle'))

    def predict(self, chunk, lang):
        # This does NOT work -- Elliot
        score = self.log_model.predict_proba(np.concatenate((bi_chunk_freq,tri_chunk_freq)))
        result=score[0][0]
        return result

        pass
