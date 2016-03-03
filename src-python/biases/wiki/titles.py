"""Functions relating to wikipedia titles."""

def make_wiki_title(title):
    """Given a title, returns the official title of the article that it refers
    to by captilizing the first letter and replacing spaces with
    underscores. For instance, 'money laundering' becomes 
    'Money_laundering'."""
    
    return (title[0].upper() + title[1:]).replace(' ', '_')
