import _path_config

import sys, bz2, logging

from gensim.corpora import wikicorpus
from biases.wiki.titles import make_wiki_title

import re

text_replace1 = re.compile('(\{\{.*\}\})|(<.*>)')

def threshold_eval(content,keys,threshold):
    """
    Does a very simple keyword threshold, as in if the number of keywords
    found exceeds a percentage of the words in the article, we return true.
    """
    num_hits = 0
    content = re.sub(text_replace1,"",content)
    content = content.split()
    with open(keys,'r') as f:
        key_set = set([x.lower() for x in f.read().split('\n')])
        for word in content:
            if word in key_set:
                num_hits += 1
            if float(num_hits)/len(content) > threshold:
                return True
            else: 
                return False

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: python3 search_dump.py wiki-pages-articles.xml.bz2 titles.txt search-query-doc threshold [0-1]')
        print('Searchs through the given Wikipedia dump for all articles that contain')
        print('any of the search-queries (case insensitive), and puts the titles of those')
        print('articles in titles.txt, one line per title.')
    else:
        wiki_dump_fname = sys.argv[1]
        titles_out_fname = sys.argv[2]
        search_queries = sys.argv[3]
        threshold = float(sys.argv[-1])
        num_hits = 0

        # Cleans up the article text so thresholding can work
        link_pattern2 = re.compile('Template:.*|File:.*|w:.*|:*:.*')
        link_replace = re.compile('Category:|Wikipedia:|#redirect|#REDIRECT|(\[\[)|(\]\])')

        logging.info('Searching %s', wiki_dump_fname)
        with bz2.open(wiki_dump_fname, 'rt') as wiki_dump_file:
            with open(titles_out_fname, 'w') as titles_out_file:
                for title, content, pageid in \
                        wikicorpus.extract_pages(wiki_dump_file):
                    content = re.sub(link_replace,"",content.lower())
                    if (re.search(link_pattern2,title) == None and
                           threshold_eval(content,search_queries,threshold)):     
                        titles_out_file.write(make_wiki_title(title) + '\n')
                        print(title)
                        num_hits += 1
                        
        logging.info('Found %d matches', num_hits)
    
