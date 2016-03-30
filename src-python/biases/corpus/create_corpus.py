from collections import deque
import argparse
import mwclient

def create_corpus(seed_article, lang_code):
	
	articles_to_check = deque()
	corpus = []
	seen = []
	
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
				seen.add(link)
		corpus.add(article.name)
		
	print(corpus)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument()
	parser.parse_args()
	create_corpus()