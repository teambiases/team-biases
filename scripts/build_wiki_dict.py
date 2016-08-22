import _path_config

import sys

from gensim.corpora.wikicorpus import WikiCorpus

if __name__ == '__main__':
    if len(sys.argv) not in range(3, 5):
        print('Usage: python3 build_wiki_dict wiki-pages-articles.xml.bz2 dict.pickle (dict.txt)')
        print('Build a frequency dictionary of all words in the given Wikipedia dump.')
        print('Saves the dictionary as a pickle dump and optionally as a text file.')
    else:
        dump_fname = sys.argv[1]
        dict_pickle_fname = sys.argv[2]
        dict_txt_fname = sys.argv[3] if len(sys.argv) >= 4 else None
        
        corpus = WikiCorpus(dump_fname)
        corpus.dictionary.filter_extremes(no_below=20, no_above=0.1, keep_n=100000)
        
        corpus.dictionary.save(dict_pickle_fname)
        if dict_txt_fname:
            corpus.dictionary.save_as_text(dict_txt_fname)
