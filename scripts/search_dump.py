import _path_config

import sys, bz2, logging

from gensim.corpora import wikicorpus

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 search_dump.py wiki-pages-articles.xml.bz2 titles.txt search-query-1 search-query-2')
        print('Searchs through the given Wikipedia dump for all articles that contain')
        print('any of the search-queries (case insensitive), and puts the titles of those')
        print('articles in titles.txt, one line per title.')
    else:
        wiki_dump_fname = sys.argv[1]
        titles_out_fname = sys.argv[2]
        search_queries = [q.lower() for q in sys.argv[3:]]
        num_hits = 0
        
        logging.info('Searching %s', wiki_dump_fname)
        with bz2.open(wiki_dump_fname, 'rt') as wiki_dump_file:
            with open(titles_out_fname, 'w') as titles_out_file:
                for title, content, pageid in \
                        wikicorpus.extract_pages(wiki_dump_file):
                    if any(search_query in content.lower() for search_query
                           in search_queries):
                        titles_out_file.write(title + '\n')
                        num_hits += 1
                        
        logging.info('Found %d matches', num_hits)
    