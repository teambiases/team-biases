import _path_config

import sys
import bz2
import logging
import re
import argparse
import gensim
import pickle

from biases.wiki.titles import make_wiki_title
from biases.corpus.search_queries import ALL_SEARCH_QUERIES, search_query_help
from biases.utils.gensim import load_mm_corpus
from gensim.corpora import wikicorpus

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description =
            'Search a Wikipedia dump for articles that match given criteria.',
            epilog = search_query_help(),
            formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument('wiki_dump_fname', type=str, metavar='wiki-dump',
                        help='Wikipedia dump to search')
    parser.add_argument('mm_fname', type=str, metavar='mm-dump',
                        help='matrix market file of tfidf vectors for dump')
    parser.add_argument('dict_fname', type=str, metavar='dict',
                        help='dictionary file')
    parser.add_argument('categories_fname', type=str, metavar='categories',
                        help='categories file')
    parser.add_argument('titles_out_fname', type=str, metavar='titles',
                        help='output file with one article title per line')
    parser.add_argument('search_query', type=str, metavar='search-query',
                        help='search query (described more below)')
    
    args = parser.parse_args()
    
    # Load MM corpus and dictionary
    corpus = load_mm_corpus(args.mm_fname)
    dict = gensim.corpora.Dictionary.load(args.dict_fname)
    with open(args.categories_fname, 'rb') as categories_file:
        categories = pickle.load(categories_file)
    
    prepared_query_funcs = {}
    for name, search_query in ALL_SEARCH_QUERIES.items():
        prepared_query_funcs[name] = search_query(corpus, dict, categories)
    search_query_func = eval(args.search_query, prepared_query_funcs)
    
    num_hits = 0

    logging.info('Searching %s with query %s',
                 args.wiki_dump_fname, args.search_query)
    with bz2.open(args.wiki_dump_fname, 'rt') as wiki_dump_file:
        with open(args.titles_out_fname, 'w') as titles_out_file:
            for title, content, pageid in \
                    wikicorpus.extract_pages(wiki_dump_file,
                                             filter_namespaces=('0',)):
                if search_query_func(content):     
                    titles_out_file.write(make_wiki_title(title) + '\n')
                    num_hits += 1
                    
    logging.info('Found %d matches', num_hits)
    
