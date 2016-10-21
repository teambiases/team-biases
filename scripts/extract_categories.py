import _path_config

import sys
import bz2
import pickle
import logging

from collections import defaultdict
from gensim.corpora.wikicorpus import extract_pages
from biases.wiki.text import extract_links

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 extract_categories.py wiki-pages-articles.xml.bz2 categories.pickle')
        print('Extract all categories from a Wikipedia database dump as a dictionary of')
        print('category: [subcategories] pairs and writes it to a pickle file.')
    else:
        _, dump_fname, categories_fname = sys.argv
        
        logging.info('extracting categories from %s', dump_fname)
        # filter_namespaces = ('14',) extracts only category pages
        category_pages = ((title, content, pageid) for title, content, pageid
                          in extract_pages(bz2.open(dump_fname, 'r'),
                                           filter_namespaces = ('14',))
                          if content != '')
        
        categories = defaultdict(list)
        
        for title, content, pageid in category_pages:
            category_prefix = title[:title.index(':') + 1]
            # Make entry for this category with no subcategories if it
            # doesn't exist
            if title not in categories:
                categories[title] = []
            
            # Look for supercategories of this category
            for link_article, link_text in extract_links(content):
                if link_article.startswith(category_prefix):
                    categories[link_article].append(title)
                    
        with open(categories_fname, 'wb') as categories_file:
            logging.info('saving categories to %s', categories_fname)
            pickle.dump(categories, categories_file)
