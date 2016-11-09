"""
Query system that can be used for determining if a document should be
included in a corpus.
"""

import operator
import logging

from biases.utils.math import safe_ratio, cosine_similarity
from biases.wiki.text import extract_links
from gensim.corpora import wikicorpus
from gensim.models import TfidfModel
from biases.wiki.titles import make_wiki_title
from biases.wiki.categories import get_subcategories

ALL_SEARCH_QUERIES = {}

class SearchQuery(object):
    
    def __init__(self, query_func):
        """
        Given a function that takes content and produces a numeric or boolean
        value, this returns that function as a SearchQuery which can be called
        and also can be combined with the operators ~,&,|,<=,==,>=,<,>,!=.
        """
        self.query_func = query_func
        
    def __call__(self, title, content):
        return self.query_func(title, content)
        
    def _operation(self, op, other = None):
        def new_query_func(title, content):
            args = [self(title, content)]
            if other is not None:
                if isinstance(other, SearchQuery):
                    args.append(other(title, content))
                else:
                    args.append(other)
            return op(*args)
        return SearchQuery(new_query_func)
    
    def __and__(self, other):
        return self._operation(operator.and_, other)
    
    def __or__(self, other):
        return self._operation(operator.or_, other)
    
    def __not__(self):
        return self._operation(operator.not_)
    
    def __le__(self, other):
        return self._operation(operator.le, other)
    
    def __eq__(self, other):
        return self._operation(operator.eq, other)
    
    def __ge__(self, other):
        return self._operation(operator.ge, other)
    
    def __lt__(self, other):
        return self._operation(operator.lt, other)
    
    def __gt__(self, other):
        return self._operation(operator.gt, other)
    
    def __ne__(self, other):
        return self._operation(operator.ne, other)
    
def search_query_help():
    """
    Returns a string explaining search queries and the available query
    functions.
    """
    
    # Construct epilog for help message detailing search queries
    help_text = """additional details on search queries:
  Search queries contain a number of query functions combined with operators
  such as <, ==, >=, etc. (comparison) and &, |, ~ (boolean). For instance,
  and example query could be:
  
  "(text_occurences('france') >= 3) | (text_occurences('britain') != 0)
  
""" + query_func_help()
    
    return help_text
        
def query_func_help():
    """
    Returns a string explaining the available query functions.
    """
    
    help_text = 'available query functions:'
    
    for query_function in ALL_SEARCH_QUERIES.values():
        help_text += '\n  ' + query_function.__doc__
        
    return help_text
    
def make_search_query(help):
    """
    Given a function query_func: (corpus, dict, args...) -> (content) -> value,
    wraps it so it can be used in a query string.
    """
    
    def query_decorator(query_func):
        def query_wrap(corpus, dict, categories):
            def query(*args, **kwargs):
                return query_func(corpus, dict, categories, *args, **kwargs)
            return query
        
        ALL_SEARCH_QUERIES[query_func.__name__] = query_wrap
        query_wrap.__doc__ = help
        return query_wrap
    
    return query_decorator
    
def load_keywords_from_file(keywords_fname):
    """
    Given a file with a list of keywords, one per line, return them as a set.
    """
    
    logging.info('loading keywords from %s', keywords_fname)
    with open(keywords_fname, 'r') as keywords_file:
        keywords = {l.strip().lower() for l in keywords_file}
        
    return keywords
    
@make_search_query('keyword_portion(\'keywords.txt\'): portion of keywords that are present in article')
def keyword_portion(corpus, dict, categories, keywords_fname):
    keywords = load_keywords_from_file(keywords_fname)
    def keyword_portion_query(title, content):
        word_set = {word.decode('utf-8') for word in
                    wikicorpus.tokenize(wikicorpus.filter_wiki(content))}
        keywords_in_words = sum(keyword in word_set for keyword in keywords)
        return safe_ratio(keywords_in_words, len(keywords))
    return SearchQuery(keyword_portion_query)
    
@make_search_query('word_portion(\'keywords.txt\'): portion of words in article that are keywords')
def word_portion(corpus, dict, categories, keywords_fname):
    keywords = load_keywords_from_file(keywords_fname)
    def word_portion_query(title, content):
        words = [word.decode('utf-8') for word in
                 wikicorpus.tokenize(wikicorpus.filter_wiki(content))]
        words_in_keywords = sum(word in keywords for word in words)
        return safe_ratio(words_in_keywords, len(words))
    return SearchQuery(word_portion_query)

@make_search_query('text_occurences(\'phrase\'): number of times \'phrase\' (case-insensitive) appears in the text') 
def text_occurences(corpus, dict, categories, phrase):
    phrase = phrase.lower()
    def text_occurences_query(title, content):
        return content.lower().count(phrase)
    return SearchQuery(text_occurences_query)
    
@make_search_query('category_occurences(\'Category-prefix:\', \'phrase\'): number of times \'phrase\' appears in categories of this article')
def category_occurences(corpus, dict, categories, category_prefix, phrase):
    phrase = phrase.lower()
    def category_occurences_query(title, content):
        links = extract_links(content)
        occurences = 0
        for article, link_text in links:
            if article.startswith(category_prefix):
                category = article[len(category_prefix):]
                occurences += category.lower().count(phrase)
        return occurences
    return SearchQuery(category_occurences_query)

@make_search_query('subcategories_of(\'Category:name\', depth): number of subcategories of the given category (within the given depth) that this article appears in')
def subcategories_of(corpus, dict, categories, category, depth = -1):
    logging.info('determining subcategories of \"%s\"', category)
    subcategories = get_subcategories(categories, category, depth)
    depth_message = '' if depth == -1 else ' within depth {}'.format(depth)
    logging.info('found %d subcategories' + depth_message, len(subcategories))
    
    def subcategories_of_query(title, content):
        num_subcategories = 0
        for link_article, link_text in extract_links(content):
            link_article = make_wiki_title(link_article)
            if link_article in subcategories:
                num_subcategories += 1
        return num_subcategories
    
    return SearchQuery(subcategories_of_query)

@make_search_query('subcategory_depth_of(\'Category:name\'): minimum depth below the given category of any category in this article')
def subcategory_depth_of(corpus, dict, categories, category):
    logging.info('determining subcategories of \"%s\"', category)
    subcategories = {category: category.depth for category in 
                     get_subcategories(categories, category)}
    logging.info('found %d subcategories', len(subcategories))
    
    def subcategory_depth_of_query(title, content):
        min_depth = float('inf')
        for link_article, link_text in extract_links(content):
            link_article = make_wiki_title(link_article)
            try:
                depth = subcategories[link_article]
                if depth < min_depth:
                    min_depth = depth
            except KeyError:
                pass
        return min_depth
    
    return SearchQuery(subcategory_depth_of_query)

@make_search_query('categories_in([\'Category:first category\', ...]): number of categories this article has in the given list')
def categories_in(corpus, dict, categories, category_list):
    category_set = {make_wiki_title(category) for category in category_list}
    
    def categories_in_query(title, content):
        num_categories = 0
        for link_article, link_text in extract_links(content):
            link_article = make_wiki_title(link_article)
            if link_article in category_set:
                num_categories += 1
        return num_categories
    
    return SearchQuery(categories_in_query)

@make_search_query('is_category_main_article(): 1 if this is a main article for a category, 0 otherwise')
def is_category_main_article(corpus, dict, categories):
    # Get 'Category:' prefix for this language
    random_category = next(iter(categories))
    category_prefix = random_category[:random_category.index(':') + 1]
    
    def is_category_main_article_query(title, content):
        title = make_wiki_title(title)
        return 1 if (category_prefix + title) in categories else 0
        
    return SearchQuery(is_category_main_article_query)

@make_search_query('tfidf_similarity(\'Article title\'): tfidf cosine similarity to the given article')
def tfidf_similarity(corpus, dictionary, categories, seed_article_title):
    mm, metadata, index = corpus
    
    # Create tfidf model
    tfidf = TfidfModel(dictionary = dictionary)
    
    # Get offset of seed article
    seed_article_offset = None
    for article_index, offset in enumerate(index):
        article_id, article_title = metadata[article_index]
        if article_title == seed_article_title:
            seed_article_offset = offset
            
    # Load seed article
    if seed_article_offset is None:
        logging.error('Seed article "%s" not found', seed_article_title)
    else:
        logging.info('Loading seed article "%s"', seed_article_title)
        seed_article = dict(mm.docbyoffset(seed_article_offset))
        
        def tfidf_similarity_query(title, content):
            tokens = wikicorpus.tokenize(wikicorpus.filter_wiki(content))
            vector = dict(tfidf[dictionary.doc2bow(tokens)])
            return cosine_similarity(seed_article, vector)
        return SearchQuery(tfidf_similarity_query)
    