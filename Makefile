
PYTHON=python3
DATADIR=data

TARGETLANG=es
SPECTRUMLANG1=en
SPECTRUMLANG2=ru
DUMPDATE=20160820

.SECONDARY: # Never delete intermediate files

# Building dictionaries from dumps

$(DATADIR)/wikipedia/dict/%.dict.pickle : scripts/build_wiki_dict.py $(DATADIR)/wikipedia/dump/%-pages-articles.xml.bz2
	$(PYTHON) $^ $@

# Creating tf-idf matrix market files from corpora and dictionaries
$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 : scripts/build_wiki_vectors.py $(DATADIR)/wikipedia/dump/%-pages-articles.xml.bz2 $(DATADIR)/wikipedia/dict/%.dict.pickle
	$(PYTHON) $^ $(patsubst %.bz2,%,$@)
	bzip2 -f $(patsubst %.bz2,%,$@)
	
# TODO Combine matrix market files and sort

# TODO Run LDA over combined matrix market files
