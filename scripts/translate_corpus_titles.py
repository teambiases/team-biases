import _path_config

import sys
import csv
import logging

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python3 translate_corpus_titles.py titles.txt langlinks.csv lang titles.lang.txt')
        print('Given a file of Wikipedia titles, converts them to files in a different language')
        print('using the given langlinks file and puts them in titles.lang.txt.')
    else:
        _, titles_fname, langlinks_fname, lang, output_fname = sys.argv
        
        logging.info('reading langlinks from %s...', langlinks_fname)
        title_map = {}
        with open(langlinks_fname, 'r') as langlinks_file:
            langlinks_csv = csv.reader(langlinks_file)
            langs = next(langlinks_csv)
            lang_index = langs.index(lang)
            for langlink_row in langlinks_csv:
                if langlink_row[lang_index] != '':
                    title_map[langlink_row[0]] = langlink_row[lang_index]
            
        logging.info('writing %s...', output_fname)
        with open(output_fname, 'w') as output_file:
            with open(titles_fname, 'r') as titles_file:
                for title in titles_file:
                    title = title.strip()
                    if title in title_map:
                        output_file.write(title_map[title] + '\n')
            
