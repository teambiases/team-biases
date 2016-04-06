import sys
from collections import deque
import argparse
import mwclient
from human_relevance import human_relevance

def create_corpus(seed_article, lang_code):
	
	articles_to_check = deque()
	corpus = []
	seen = []

	relevant = human_relevance
	
	site = mwclient.Site(lang_code + '.wikipedia.org')
	
	page = site.Pages[seed_article]

	articles_to_check.append(page)
	
	while articles_to_check:
		article = articles_to_check.pop()
		if relevant(article):
			links = article.links()
			for link in links:
				if link not in seen:
					articles_to_check.append(article)
					seen.append(link)
					print link.name
			corpus.append(article.name)
		
	for article in corpus:
		print article.name

if __name__ == '__main__':
	create_corpus(sys.argv[1], sys.argv[2])
