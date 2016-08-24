import _path_config

import sys, csv, pickle, bz2, os, shutil
from collections import defaultdict
import itertools
from gensim.corpora.dictionary import Dictionary

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 parallelize_wiki_dicts.py langlinks.csv lang1.dict.pickle lang2.dict.pickle ... output.dict.pickle')
        print('Given a CSV file of interlanguage links (as produced by export_langlinks_csv.py)')
        print('and several dictionaries from Wikipedia corpora, combines them into a single')
        print('dictionary where each word in a language is replaced by lang#word. For instance,')
        print('the word "apple" in english is replaced by "en#apple". This dictionary can be')
        print('used with the parallel vector corpus producted by parallelize_wiki_vectors.py.')
    else:
        langlinks_fname = sys.argv[1]
        in_dict_fnames = sys.argv[2:-1]
        num_langs = len(in_dict_fnames)
        out_dict_fname = sys.argv[-1]
        
        with open(langlinks_fname) as langlinks_file:
            langlinks = csv.reader(langlinks_file)
            lang_names = next(langlinks) # Read header row
        
        out_dict = Dictionary()
        id_offset = 0
        for in_dict_fname, lang_name in zip(in_dict_fnames, lang_names):
            in_dict = Dictionary.load(in_dict_fname)
            for token, old_id in in_dict.token2id.items():
                df = in_dict.dfs[old_id]
                new_id = old_id + id_offset
                new_token = '{}#{}'.format(lang_name, token)
                
                out_dict.token2id[new_token] = new_id
                out_dict.dfs[new_id] = df
                
            out_dict.num_docs += in_dict.num_docs
            out_dict.num_pos += in_dict.num_pos
            out_dict.num_nnz += in_dict.num_nnz
            
            id_offset += len(in_dict)
            
        out_dict.save(out_dict_fname)
                    