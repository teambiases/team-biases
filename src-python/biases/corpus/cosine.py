import mwclient
from biases.wiki.langlinks import get_unified_link_set, mwclient_site
from biases.utils.math import set_cosine_similarity, spectrum_from_similarities

"""
Use get_unified_link_set to get links and put it into a set.
Need to do this for current article AND seed article, so we need 2 sets.
"""

def threshold(page): 

    threshold = .1
    seed_links = get_unified_link_set(("en", "Cold_War"), set("en"))
    test_page_links = get_unified_link_set(("en", page.name), set("en"))

    return set_cosine_similarity(seed_links, test_page_links) > threshold

def cosine_relevance(page):
    return threshold(page)

