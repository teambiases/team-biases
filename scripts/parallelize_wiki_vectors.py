import _path_config

import sys, csv, pickle, bz2, os, shutil, itertools, logging
from collections import defaultdict
from biases.wiki.titles import make_wiki_title

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 parallelize_wiki_vectors.py langlinks.csv lang1.mm.bz2 lang2.mm.bz2 ... output.mm')
        print('Given a CSV file of interlanguage links (as produced by export_langlinks_csv.py)')
        print('and several vectorized Wikipedia corpora, combines them into a single corpus,')
        print('where each document in the combined corpus is composed of parallel documents')
        print('in each of the input languages.')
    else:
        langlinks_fname = sys.argv[1]
        mm_fnames = sys.argv[2:-1]
        num_langs = len(mm_fnames)
        out_fname = sys.argv[-1]
        
        with open(langlinks_fname) as langlinks_file:
            langlinks = csv.reader(langlinks_file)
            lang_names = next(langlinks) # Read header row
            title2id = [{} for _ in range(num_langs)]
            current_id = 0
            for langlink in langlinks:
                if '' not in langlink: # Make sure all languages are represented
                    for lang_index, article_title in enumerate(langlink):
                        article_title = make_wiki_title(article_title)
                        title2id[lang_index][article_title] = current_id
                    current_id += 1
        
        id2id = [{} for _ in range(num_langs)]
        new_id_counts = defaultdict(int)
        for lang_index, mm_fname in enumerate(mm_fnames):
            # Remove .bz2 suffix and add .metadata.cpickle
            meta_fname = mm_fname[:-4] + '.metadata.cpickle'
            with open(meta_fname, 'rb') as meta_file:
                metadata = pickle.load(meta_file)
                for old_id, (article_id, article_title) in metadata.items():
                    article_title = make_wiki_title(article_title)
                    if article_title in title2id[lang_index]:
                        new_id = title2id[lang_index][article_title]
                        new_id_counts[new_id] += 1
                        id2id[lang_index][old_id] = new_id
        
        id2title = [dict((id, title) for title, id in t2i.items())
                    for t2i in title2id]
        del title2id
            
        # Remove articles from id2id that don't appear in all languages
        id2compact_id = {}
        current_compact_id = 0
        for new_id in range(current_id):
            if new_id_counts[new_id] == num_langs:
                id2compact_id[new_id] = current_compact_id
                current_compact_id += 1
            else:
                id2compact_id[new_id] = None
        total_num_docs = current_compact_id
        new_id2id = [{} for _ in range(num_langs)]
        for lang_index in range(num_langs):
            for old_id, new_id in id2id[lang_index].items():
                compact_id = id2compact_id[new_id]
                if compact_id is not None:
                    new_id2id[lang_index][old_id] = compact_id
        del id2id
        id2id = new_id2id
        
        # Create index for parallelized corpus
        logging.info('Constructing new index')
        new2old = dict((new_id, old_id) for old_id, new_id in
                   id2compact_id.items() if new_id is not None)
        parallel_index = {}
        for new_id, old_id in new2old.items():
            article_titles = map(make_wiki_title,
                                 (i2t[old_id] for i2t in id2title))
            parallel_index[new_id] = tuple(article_titles)
        index_fname = out_fname[:-7] + '.index.pickle' # remove .mm.bz2
        logging.info('Saving index to %s', index_fname)
        with open(index_fname, 'wb') as index_file:
            pickle.dump(parallel_index, index_file)
        
        del id2compact_id, new2old
        
        # Initialize Apache Spark
        #sc = SparkContext('local', 'parallelize_wiki_vectors')
        
        word_id_offset = 0
        all_entries = []
        mm_files = []
        for lang_index, (lang_name, mm_fname) in enumerate(zip(lang_names,
                                                               mm_fnames)):
            mm_file = bz2.open(mm_fname, 'r')
            header = str(next(mm_file), encoding='utf-8').strip() # Extract first header
            num_docs, dict_size, nnz_entries = map(int, next(mm_file).split())
            
            def line2entry(line):
                r, c, v = line.split()
                return int(r), int(c), float(v)
            
            class map_entries:
                def __init__(self, entries, word_id_offset, lang_index, fname):
                    self.entries = entries
                    self.word_id_offset = word_id_offset
                    self.lang_index = lang_index
                    self.fname = fname
                def __iter__(self):
                    logging.info('Reading %s', self.fname)
                    for old_article_id, old_word_id, value in self.entries:
                        # Subtract 1 from article id since MM is 1-indexed
                        old_article_id -= 1
                        new_article_id = id2id[self.lang_index].get(old_article_id)
                        if new_article_id is not None:
                            new_word_id = old_word_id + self.word_id_offset
                            # Add 1 to article id since MM is 1-indexed
                            yield (new_article_id + 1), new_word_id, value
                        
            entries = map(line2entry, mm_file)
            new_entries = map_entries(entries, word_id_offset, lang_index,
                                      mm_fname)
            
            all_entries.append(new_entries)
            
            word_id_offset += dict_size
            mm_files.append(mm_file) # So we can close them all later on
                
        total_dict_size = word_id_offset
        all_entries = itertools.chain(*all_entries)
        sorted_entries = sorted(all_entries)
        total_nnz_entries = len(sorted_entries)
        lines = map(lambda entry: ' '.join(map(str, entry)), sorted_entries)
        header_lines = [header, ' '.join(map(str, [total_num_docs,
                total_dict_size, total_nnz_entries]))]
        lines = itertools.chain(header_lines, lines)
        logging.info('Writing matrix market data to %s', out_fname)
        with bz2.open(out_fname, 'w') as out_file:
            for line in lines:
                out_file.write(bytes(line + '\n', encoding='utf-8'))
        
        for mm_file in mm_files:
            mm_file.close()
                    