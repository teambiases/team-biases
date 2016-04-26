import codecs
import sys
from collections import deque
import argparse
import mwclient
from human_relevance import human_relevance

def create_corpus(seed_article, lang_code):

	UTF8Writer = codecs.getwriter('utf8')
	sys.stdout = UTF8Writer(sys.stdout)
	
	articles_to_check = deque()
	corpus = []
	seen = []

	relevant = human_relevance
	
	site = mwclient.Site(lang_code + '.wikipedia.org')
	
	page = site.Pages[seed_article]

	articles_to_check.append(page)
	seen.append(page)

	evaluated = 0
	
	while articles_to_check and evaluated < 100:
		article = articles_to_check.pop()
		print 'ARTICLE: ' + article.name 		
		if relevant(article):
			links = article.links()
			for link in links:
				print 'LINK: ' + link.name
				if link not in seen:
					articles_to_check.appendleft(link)
					seen.append(link)
			corpus.append(article.name)
		evaluated += 1
		
	for article in corpus:
		print article

if __name__ == '__main__':
	create_corpus(sys.argv[1], sys.argv[2])
