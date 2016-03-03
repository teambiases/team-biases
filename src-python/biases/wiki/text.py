"""Tools for processing MediaWiki markup."""

import re
from biases.wiki.titles import make_wiki_title

MEDIAWIKI_LINK_RE = re.compile(r'\[\[([^\|#]+)(?:#[^\|]*)?(\|[^\]]+)?\]\]')

def extract_links(text):
    """Given a selection of MediaWiki text, returns a generator over the links
    in the text as tuples (article, link text)."""
    
    for match in MEDIAWIKI_LINK_RE.finditer(text):
        link = match.groups()
        # Some links only contain a page title
        if len(link) == 1:
            title, = link
            link_text, = link
        else:
            title, link_text = link
            
        yield (make_wiki_title(title), link_text)
