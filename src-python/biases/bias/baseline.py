from biases.wiki.langlinks import get_unified_link_set, mwclient_site
from biases.utils.math import set_cosine_similarity, spectrum_from_similarities

def link_baseline(target_article, spectrum_langs):
    """Given a Wikipedia article as a tuple of the form (lang, title) and
    two spectrum languages, returns a 3-tuple where the first two elements
    represent the similarity of the article to each of the baselines and the
    third element represents a placement of the article along the spectrum from
    -1 to 1."""
    
    target_lang, target_title = target_article
    langs = set(spectrum_langs) | {target_lang}
    
    langlinks = dict(mwclient_site(target_lang).pages[target_title]
                     .langlinks())
    spectrum_articles = [(spectrum_lang, langlinks[spectrum_lang]) if
                         spectrum_lang in langlinks else None
                         for spectrum_lang in spectrum_langs]
    
    target_links = get_unified_link_set(target_article, langs)
    spectrum_link_sets = [get_unified_link_set(spectrum_article, langs)
                          if spectrum_article is not None else {}
                          for spectrum_article in spectrum_articles]
    
    similarities = [set_cosine_similarity(target_links, spectrum_links)
                    for spectrum_links in spectrum_link_sets]
    
    return similarities[0], similarities[1], \
        spectrum_from_similarities(*similarities)
