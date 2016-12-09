import _path_config

import sys
import random
import pickle

from biases.wiki.chunks import print_chunk

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Usage: python3 sample_chunks.py chunks.pickle sample.txt articles chunks/article seed')
        print('Given a list of chunks as output by split_chunks.py, samples a certain number')
        print('of articles and a certain number of chunks from each of those articles and')
        print('writes the results to sample.txt. seed specificies the seed for the random')
        print('number generator and can be any string.')
    else:
        _, chunks_fname, sample_fname, num_articles, num_chunks, seed \
                = sys.argv
        num_articles = int(num_articles)
        num_chunks = int(num_chunks)
        
        random.seed(seed)
        
        with open(chunks_fname, 'rb') as chunks_file:
            chunked_articles = pickle.load(chunks_file)
            
        # Keep track of remaining articles that we could include in the sample
        shuffled_articles = list(sorted(chunked_articles.keys()))
        random.shuffle(shuffled_articles)
        sampled_articles = 0
        
        with open(sample_fname, 'w') as sample_file:
            for article_title in shuffled_articles:
                shuffled_chunks = list(chunked_articles[article_title])
                random.shuffle(shuffled_chunks)
                sampled_chunks = []
                for chunk_index, chunk in enumerate(shuffled_chunks):
                    if len(shuffled_chunks) - chunk_index + \
                            len(sampled_chunks) < num_chunks:
                        print('Not enough chunks in this article. Skipping...')
                        break
                    
                    print_chunk(chunk)
                    yn = 'invalid'
                    while yn not in 'yn':
                        yn = input('Is this a valid chunk? (y/n) ')
                        if yn == '':
                            yn = 'invalid'
                    if yn == 'y':
                        sampled_chunks.append(chunk)
                    
                    if len(sampled_chunks) >= num_chunks:
                        break
                    
                    
                if len(sampled_chunks) == num_chunks:
                    print('Completed sample of {} chunks from {}'.format(
                            num_chunks, article_title))
                    for chunk in sampled_chunks:
                        sample_file.write('\t'.join(map(str, chunk.id)) +
                                           '\n')
                    sampled_articles += 1
                
                if sampled_articles >= num_articles:
                    break
