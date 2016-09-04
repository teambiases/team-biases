
import sys
from functools import lru_cache

from biases.wiki import mwclient_site
from biases.wiki.text import extract_links
from biases.utils.math import cosine_similarity

from gensim.corpora.wikicorpus import filter_wiki, tokenize
from gensim.models.tfidfmodel import TfidfModel
from biases.wiki.titles import make_wiki_title
        
@lru_cache(maxsize=10)
def _article_text(lang, article_title):
    try:
        return mwclient_site(lang).pages[article_title].text()
    except KeyError:
        return None

@lru_cache(maxsize=None)
def _article_links(lang, article_title):
    return {title for title, _ in extract_links(_article_text(lang,
                                                              article_title))}

_dict = None
_tfidf = None
@lru_cache(maxsize=None)
def _article_tfidf(lang, article_title):
    text = _article_text(lang, article_title)
    if text is None:
        return None
    else:
        return dict(_tfidf[_dict.doc2bow(tokenize(filter_wiki(text)))])
        
def dbscan_single(lang, seed_titles, min_pts, eps, dictionary):
    """
    Finds a single DBSCAN cluster on Wikipedia with a given set of seed
    articles and parameters min_pts and epsilon. For DBSCAN, "neighbors" are
    considered to be articles that are linked to and that have tfidf cosine
    similarity greater than eps. dictionary should be a gensim dictionary
    that can be used for computing tfidf values. Returns a set of article
    titles.
    """
    
    global _dict, _tfidf
    _dict = dictionary
    _tfidf = TfidfModel(dictionary = dictionary)

    frontier = {make_wiki_title(title) for title in seed_titles}
    cluster = set()
    visited = set()
    
    while len(frontier) > 0:
        article_title = next(iter(frontier))
        frontier.remove(article_title)
        visited.add(article_title)
        
        # Get neighbors
        linked_titles = _article_links(lang, article_title)
        sys.stdout.flush()
        article_tfidf = _article_tfidf(lang, article_title)
        neighbors = []
        for linked_title in linked_titles:
            linked_tfidf = _article_tfidf(lang, linked_title)
            if linked_tfidf is not None:
                _article_links(lang, linked_title)
                cosine_sim = cosine_similarity(article_tfidf, linked_tfidf)
                sys.stdout.flush()
                if cosine_sim >= eps:
                    neighbors.append(linked_title)
                
        sys.stdout.flush()
        if len(neighbors) >= min_pts:
            # Add all neighbors to frontier
            for neighbor_title in neighbors:
                if neighbor_title not in visited:
                    frontier.add(neighbor_title)
        
        cluster.add(article_title)
        
    return cluster
