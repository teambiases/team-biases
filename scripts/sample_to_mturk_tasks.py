import _path_config

import sys
import pickle
import csv
from biases.wiki.chunks import chunk_to_html

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 sample_to_mturk_tasks.py sample.txt chunks.pickle tasks.csv')
        print('Given a sample of article chunks and the article chunk file, converts the')
        print('chunks in that sample to mechanical turk tasks and outputs them to a CSV.')
    else:
        _, sample_fname, chunks_fname, tasks_fname = sys.argv
        
        sample = []
        with open(sample_fname, 'r') as sample_file:
            for line in sample_file:
                article, section_index, chunk_index = line.strip().split('\t')
                sample.append((article, int(section_index), int(chunk_index)))
        
        with open(chunks_fname, 'rb') as chunks_file:
            chunked_articles = pickle.load(chunks_file)
            
        with open(tasks_fname, 'w') as tasks_file:
            tasks_out = csv.writer(tasks_file)
            # Write header row
            tasks_out.writerow(['article', 'section_index', 'chunk_index',
                                'sentences'])
            
            for chunk_id in sample:
                article, section_index, chunk_index = chunk_id
                article_chunks = chunked_articles[article]
                for chunk in article_chunks:
                    if chunk.id == chunk_id:
                        tasks_out.writerow([article, section_index,
                                chunk_index, chunk_to_html(chunk)])
