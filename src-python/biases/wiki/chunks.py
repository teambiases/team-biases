from collections import namedtuple

import mwparserfromhell
import re
import itertools
import nltk
import random

from gensim.corpora.wikicorpus import filter_wiki

Chunk = namedtuple('Chunk', ['id', 'paragraphs'])
"""
A chunk is a section of a Wikipedia article. Each chunk has a unique ID
which is a triple (article_title, section_index, chunk_index). It also has
one or more paragraphs, each of which is a list of sentences as strings.
"""

def beam_search(initial, objective, mutate, n = 100, p = 0.2, max_iters = 100):
    """
    Run beam search with a given mutate and objective function. In each
    iteration, up to max_iters, the search does the following:
     * Evaluates each of n possible solutions by calling the objective
       function on it (smaller is better).
     * Discards all but the top p-portion of possible solutions.
     * Generates new possible solutions by calling the mutate function on
       top existing solutions until there are n possible solutions again.
    Returns the best solution at the end.
    """
    
    # Mutate initial solution a bunch to create beam
    beam = [initial] + [mutate(initial) for _ in range(n - 1)]
    
    for _ in range(max_iters):
        beam.sort(key = objective)
        beam = beam[:int(n * p)]
        while len(beam) < n:
            beam.append(mutate(random.choice(beam)))
    
    return beam[0]

def chunk_article(title, content):
    """
    Given a Wikipedia article's title and content, returns a list of chunks
    in that article.
    """
    
    sections = mwparserfromhell.parse(content).get_sections(
            include_lead = True, flat = True)
    chunks = []
    
    for section_index, section_content in enumerate(sections):
        chunks.extend(chunk_section(title, section_index, 
                                    str(section_content)))
        
    return chunks

def split_paragraphs(paragraphs, splits):
    """
    Takes a list of paragraphs, each of which is a list of sentences, and
    splits it according to the sentence boundaries identified in splits.
    For example, if the sentences are in two paragraphs ABC DEF and splits is
    [1, 4], would split into [A, BC D, EF].
    """
    
    splits = list(splits)
    splits.sort()
    sentence_index = 0
    
    current_chunk = []
    current_paragraph = []
    
    for paragraph in paragraphs:
        for sentence in paragraph:
            current_paragraph.append(sentence)
            sentence_index += 1
            if len(splits) > 0:
                if sentence_index == splits[0]:
                    current_chunk.append(current_paragraph)
                    yield current_chunk
                    
                    current_chunk = []
                    current_paragraph = []
                    splits = splits[1:]
                
        if current_paragraph != []:
            current_chunk.append(current_paragraph)
            current_paragraph = []
        
    yield current_chunk

def chunk_section(article_title, section_index, section_content):
    """
    Given an article's title and the index and content of a particular section,
    returns a list of chunks in that particular section.
    """
    
    # Split content into paragraphs and filter wiki markup
    paragraphs = [filter_wiki(paragraph) for paragraph in 
                  re.split(r'\n{2,}', section_content)]
    
    # Filter first paragraph if it looks like a title
    if paragraphs[0] == '' or paragraphs[0][0] in '=\n':
        paragraphs = paragraphs[1:]
    
    # Tokenize paragraphs into sentences
    paragraphs = [nltk.sent_tokenize(paragraph) for paragraph in paragraphs
                  if paragraph.strip() != '']
    
    sentences = list(itertools.chain(*paragraphs))
    paragraph_splits = list(itertools.accumulate(map(len, paragraphs)))
    sentence_lengths = [len(sentence.split()) for sentence in sentences]
    
    if len(sentences) == 0:
        return []
    
    # Now we use beam search to optimize chunk splits
    def objective(splits):
        splits = list(sorted(splits))
        
        paragraphs_split = len(set(splits) - set(paragraph_splits))
        
        chunk_lengths = [sum(sentence_lengths[sentence_index] for
                             sentence_index in range(chunk_start, chunk_end))
                         for chunk_start, chunk_end in
                         zip([0] + splits, splits + [len(sentences)])]
        chunk_length_deviation = (sum((chunk_length - 180) ** 2 for
                                      chunk_length in chunk_lengths)
                                  / len(chunk_lengths)) ** 0.5
        
        return chunk_length_deviation + 10 * paragraphs_split
    
    def mutate(splits):
        splits = list(splits)
        mutation_type = random.uniform(0, 1)
        if mutation_type < 0.25 or len(splits) == 0:
            splits.append(random.randint(0, len(sentences)))
        elif mutation_type < 0.75:
            mutation_index = random.randint(0, len(splits) - 1)
            splits[mutation_index] += round(random.normalvariate(0, 2))
            if splits[mutation_index] < 0:
                splits[mutation_index] = 0
            elif splits[mutation_index] > len(sentences):
                splits[mutation_index] = len(sentences)
        else:
            splits.pop(random.randint(0, len(splits) - 1))
        return tuple(splits)
    
    splits = beam_search(tuple(paragraph_splits), objective, mutate)
    
    chunks =  [Chunk((article_title, section_index, chunk_index),
                     chunk_paragraphs)
               for chunk_index, chunk_paragraphs in
               enumerate(split_paragraphs(paragraphs, splits))]
    
    return chunks
    
def chunk_length(chunk):
    """
    Get the length of a chunk in words.
    """
    
    return sum(sum(len(sentence.split()) for sentence in paragraph) for
               paragraph in chunk.paragraphs)
    
def print_chunk(chunk):
    """
    Pretty prints a chunk to stdout.
    """
    
    chunk_id_str = '{} section {} chunk {}'.format(*chunk.id)
    print('=== {} ({} words) ==='.format(chunk_id_str, chunk_length(chunk)))
    for paragraph in chunk.paragraphs:
        print('{}\n'.format(' '.join(paragraph)))
