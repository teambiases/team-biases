import _path_config

import sys, os, pickle, csv, logging
from biases.wiki.langlinks import read_langlinks_from_dump
from biases.wiki.titles import make_wiki_title

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: python3 export_dump_langlinks_csv.py langlinks.sql.gz vectors.mm.bz2 langlinks.csv lang1 lang2... ')
        print('Given a dump of the langlinks table in a Wikipedia database and a matrix-market')
        print('dump of the articles in that wiki, outputs the data to a CSV file. First')
        print('specified should be the language of the dump, other languages are the ones to')
        print('find langlinks to.')
    else:
        dump_fname = sys.argv[1]
        mm_fname = sys.argv[2]
        csv_fname = sys.argv[3]
        langs = sys.argv[4:]
        
        from_lang = langs[0]
        to_langs = langs[1:]
        
        logging.info('Reading langlink data from %s', dump_fname)
        langlinks = read_langlinks_from_dump(dump_fname, to_langs)
        
        metadata_fname = mm_fname[:-4] + '.metadata.cpickle'
        logging.info('Reading article titles from %s', metadata_fname)
        with open(metadata_fname, 'rb') as metadata_file:
            metadata = pickle.load(metadata_file)
        
        logging.info('Saving langlinks to %s', csv_fname)
        with open(csv_fname, 'w') as csv_file:
            out = csv.writer(csv_file)
            out.writerow(langs)
            for article_id, article_title in metadata.values():
                article_id = int(article_id)
                if article_id in langlinks:
                    row = [make_wiki_title(article_title)]
                    row += [make_wiki_title(title) if title else '' for title
                            in langlinks[article_id]]
                    out.writerow(row)
