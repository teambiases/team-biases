import _path_config

import sys
import pickle
import logging
import bz2

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 parallelize_wiki_vectors.py vectors.mm.bz2 titles.txt filtered.mm.bz2')
        print('Given a matrix market file of tf-idf vectors from Wikipedia, filters them to')
        print('only include vectors from documents with titles in the given file.')
    else:
        _, in_fname, titles_fname, out_fname = sys.argv
        in_index_fname = in_fname[:-7] + '.index.pickle'
        
        with open(in_index_fname, 'rb') as in_index_file:
            in_index = pickle.load(in_index_file)
            
        with open(titles_fname, 'r') as titles_file:
            corpus_titles = {line.strip() for line in titles_file}
        logging.info('loaded %s titles in corpus', len(corpus_titles))
        
        # Calculate mapping of old article IDs to new ones
        old2new_id = {}
        new_index = {}
        current_id = 1
        for old_id, titles in in_index.items():
            if titles[0] in corpus_titles:
                old2new_id[old_id] = current_id
                new_index[current_id] = titles
                current_id += 1
        new_num_docs = len(old2new_id)
        logging.info('old corpus size=%d, new corpus size=%d', len(in_index),
                     new_num_docs)
        
        def line2entry(line):
            r, c, v = line.split()
            return int(r), int(c), float(v)
        
        logging.info('reading %s', in_fname)
        new_entries = []
        with bz2.open(in_fname, 'r') as in_file:
            header = next(in_file)
            old_num_docs, dict_size, old_num_nnz = map(int,
                                                       next(in_file).split())
            for r, c, v in map(line2entry, in_file):
                new_r = old2new_id.get(r)
                if new_r is not None:
                    new_entries.append((new_r, c, v))
        new_num_nnz = len(new_entries)
            
        logging.info('writing %s', out_fname)
        with bz2.open(out_fname, 'w') as out_file:
            # Write the first header
            out_file.write(header)
            out_file.write(bytes('{} {} {}\n'.format(new_num_docs, dict_size,
                                                     new_num_nnz),
                                 encoding='utf-8'))
            for entry in new_entries:
                out_file.write(bytes(' '.join(map(str, entry)) +'\n',
                                     encoding='utf-8'))
                
        new_index_fname = out_fname[:-7] + '.index.pickle'
        logging.info('writing %s', new_index_fname)
        with open(new_index_fname, 'wb') as new_index_file:
            pickle.dump(new_index, new_index_file)
                    