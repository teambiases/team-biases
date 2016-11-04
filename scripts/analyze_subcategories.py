import _path_config

import sys
import pickle
import csv
import logging
import bz2

from collections import defaultdict
from gensim.corpora import wikicorpus

from biases.wiki.titles import make_wiki_title
from biases.wiki.categories import get_subcategories
from biases.wiki.text import extract_links

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python3 analyze_subcategories.py wiki-pages-articles.xml.bz2 categories.pickle results.csv "Category:name"')
        print('Analyze the subcategories of the given category for properties such as the depth')
        print('below the root and the number of times the root category name is mentioned.')
    else:
        _, dump_fname, categories_fname, results_fname, category = sys.argv
        
        # If category is 'Category:Cold_War', category_name is 'cold war'
        category = make_wiki_title(category)
        category_name = category[category.index(':') + 1:].replace('_', ' ') \
                                                          .lower()
        
        logging.info('loading categories from %s', categories_fname)
        with open(categories_fname, 'rb') as categories_file:
            categories = pickle.load(categories_file)
            
        logging.info('determining subcategories of "%s"', category)
        subcategories = get_subcategories(categories, category)
        logging.info('found %d subcategories of "%s"',
                     len(subcategories), category)
        
        root_name_occurences = defaultdict(int)
        num_articles = defaultdict(int)
        has_main_article = defaultdict(bool)
        
        # Iterate through corpus to determine number of times root category
        # name appears in subcategories, number of articles in each
        # subcategory, and whether each subcategory has a main article.
        logging.info('analyzing subcategories using articles from %s',
                     dump_fname)
        with bz2.open(dump_fname, 'r') as dump_file:
            for title, content, pageid in \
                    wikicorpus.extract_pages(dump_file,
                                             filter_namespaces=('0',)):
                for article_title, link_text in extract_links(content):
                    if article_title in subcategories:
                        subcategory = article_title
                        root_name_occurences[subcategory] += \
                                content.lower().count(category_name)
                        num_articles[subcategory] += 1
                        
                        subcategory_name = subcategory[subcategory.index(':')
                                                       + 1:]
                        if subcategory_name == make_wiki_title(title):
                            has_main_article[subcategory] = True
                                
        # Write results
        with open(results_fname, 'w') as results_file:
            results = csv.writer(results_file)
            results.writerow(['Subcategory', 'Depth below {}'.format(category),
                              'Number of articles',
                              'Number of subcategories',
                              'Has a main article?',
                              'Occurences of "{}"'.format(category_name)])
            
            for subcategory in subcategories:
                results.writerow([subcategory, subcategory.depth,
                        num_articles[subcategory],
                        len(categories[subcategory]),
                        'yes' if has_main_article[subcategory] else 'no',
                        root_name_occurences[subcategory]])
