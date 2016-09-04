"""Tools for dealing with Wikipedia content and dumps. This root package
may contain some basic utilies that haven't been categorized into a 
submodule."""

import mwclient

MWCLIENT_SITES = {}

def mwclient_site(lang):
    """Given a language code, get the mwclient Site object for that language
    edition of Wikipedia. Caches Site objects to avoid making them over and
    over."""
    
    if lang not in MWCLIENT_SITES:
        MWCLIENT_SITES[lang] = mwclient.Site('{}.wikipedia.org'.format(lang))
        
    return MWCLIENT_SITES[lang]
