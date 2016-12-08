import _path_config

import sys
import csv
import logging
import bz2
import pickle

from biases.wiki.chunks import chunk_article
from gensim.corpora import wikicorpus

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python3 split_chunks.py corpus.txt pages-articles.xml.bz2 langlinks.csv chunks.pickle')
        print('Reads a corpus file (one article title per line) and a langlinks.csv file as')
        print('outputted by export_*_langlinks_csv.py and processes each article that is in')
        print('both the corpus file and langlinks file as so:')
        print(' * Splits the article into sections and removes wikitext markup')
        print(' * Splits each section into "chunks" of about 180 words that attempt to follow')
        print('   paragraph boundaries.')
        print('Then, saves all those chunks to chunks.pickle.')
    else:
        _, corpus_fname, dump_fname, langlinks_fname, chunks_fname = sys.argv
        
        with open(corpus_fname, 'r') as corpus_file:
            corpus = {line.strip() for line in corpus_file}
        corpus_size = len(corpus)
            
        # Use langlinks file to make sure we only process articles that have
        # cooresponding versions in the other languages
        with open(langlinks_fname, 'r') as langlinks_file:
            langlinks_csv = csv.reader(langlinks_file)
            langs = next(langlinks_csv)
            langlinks_articles = {row[0] for row in langlinks_csv}
        corpus = corpus & langlinks_articles
        
        logging.info('loaded corpus with %d articles (%d with langlinks)',
                     corpus_size, len(corpus))
        
        chunked_articles = {}
        total_chunks = 0
        with bz2.open(dump_fname, 'rt') as dump_file:
            for title, content, pageid in \
                    wikicorpus.extract_pages(dump_file):
                if title in corpus:
                    chunks = chunk_article(title, content)
                    chunked_articles[title] = chunks
                    total_chunks += len(chunks)
                    
        logging.info('split %d articles into %d chunks',
                     len(chunked_articles), total_chunks)
        
        logging.info('writing chunks to %s', chunks_fname)
        with open(chunks_fname, 'wb') as chunks_file:
            pickle.dump(chunked_articles, chunks_file)
            