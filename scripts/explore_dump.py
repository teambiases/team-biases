import _path_config

import sys
import bz2
import logging
import re
import argparse
import gensim
import csv
import pickle

from biases.wiki.titles import make_wiki_title
from biases.corpus.search_queries import ALL_SEARCH_QUERIES, query_func_help
from biases.utils.gensim import load_mm_corpus
from gensim.corpora import wikicorpus

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description =
            'Explore properties of articles in a Wikipedia dump.',
            epilog = query_func_help(),
            formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument('wiki_dump_fname', type=str, metavar='wiki-dump',
                        help='Wikipedia dump to search')
    parser.add_argument('mm_fname', type=str, metavar='mm-dump',
                        help='matrix market file of tfidf vectors for dump')
    parser.add_argument('dict_fname', type=str, metavar='dict',
                        help='dictionary file')
    parser.add_argument('categories_fname', type=str, metavar='categories',
                        help='categories file')
    parser.add_argument('results_fname', type=str, metavar='results',
                        help='CSV output file')
    parser.add_argument('query_funcs', type=str, nargs='+',
                        metavar='query-function',
                        help='a query function (described more below)')
    
    args = parser.parse_args()
    
    # Load MM corpus and dictionary
    corpus = load_mm_corpus(args.mm_fname)
    dict = gensim.corpora.Dictionary.load(args.dict_fname)
    with open(args.categories_fname, 'rb') as categories_file:
        categories = pickle.load(categories_file)
    
    prepared_query_funcs = {}
    for name, search_query in ALL_SEARCH_QUERIES.items():
        prepared_query_funcs[name] = search_query(corpus, dict, categories)
        
    query_funcs = [eval(query_func, prepared_query_funcs)
                   for query_func in args.query_funcs]

    logging.info('Exploring %s with functions %s',
                 args.wiki_dump_fname,
                 ', '.join(map(str, args.query_funcs)))
    with bz2.open(args.wiki_dump_fname, 'rt') as wiki_dump_file:
        with open(args.results_fname, 'w') as results_file:
            results = csv.writer(results_file)
            # Write header row
            results.writerow(['Title'] + args.query_funcs)
            for title, content, pageid in \
                    wikicorpus.extract_pages(wiki_dump_file,
                                             filter_namespaces=('0',)):
                results.writerow([title] + [query_func(title, content) for query_func
                                            in query_funcs])
    
