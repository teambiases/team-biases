
PYTHON=python3
DATADIR=data
LIBDIR=lib

SPARKVERSION=2.0.0-bin-hadoop2.7
SPARKDIR=$(LIBDIR)/spark-$(SPARKVERSION)

TARGETLANG=es
SPECTRUMLANG1=en
SPECTRUMLANG2=ru
DUMPDATE=20160820
COMBINED_ID=$(TARGETLANG)-$(SPECTRUMLANG1)-$(SPECTRUMLANG2)-wiki-$(DUMPDATE)

.PRECIOUS: $(DATADIR)/wikipedia/dict/%.dict.pickle
.INTERMEDIATE: $(LIBDIR)/spark-%.tgz
.PHONY: topicmodel

$(LIBDIR) :
	mkdir $@
	
# For installing Apache Spark

$(LIBDIR)/spark-%.tgz : $(LIBDIR)
	wget http://d3kbcqa49mib13.cloudfront.net/spark-$*.tgz -O $@

$(LIBDIR)/spark-% : | $(LIBDIR)/spark-%.tgz
	tar -xf $< -C $(LIBDIR)

# Building dictionaries from dumps

$(DATADIR)/wikipedia/dict/%.dict.pickle : scripts/build_wiki_dict.py $(DATADIR)/wikipedia/dump/%-pages-articles.xml.bz2
	$(PYTHON) $^ $@

# Creating tf-idf matrix market files from corpora and dictionaries
$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 : scripts/build_wiki_vectors.py $(DATADIR)/wikipedia/dump/%-pages-articles.xml.bz2 $(DATADIR)/wikipedia/dict/%.dict.pickle
	$(PYTHON) $^ $(patsubst %.bz2,%,$@)
	bzip2 -f $(patsubst %.bz2,%,$@)
	
# Combine matrix market files and sort

$(DATADIR)/wikipedia/vector/$(COMBINED_ID).parallel.tfidf.mm.bz2 : scripts/parallelize_wiki_vectors.py \
	$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG1)-$(SPECTRUMLANG2)-$(DUMPDATE).langlinks.csv \
	$(DATADIR)/wikipedia/vector/$(TARGETLANG)wiki-$(DUMPDATE).tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/vector/$(SPECTRUMLANG1)wiki-$(DUMPDATE).tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/vector/$(SPECTRUMLANG2)wiki-$(DUMPDATE).tfidf.mm.bz2
	$(PYTHON) $^ $@
	
# Combine dictionaries

$(DATADIR)/wikipedia/dict/$(COMBINED_ID).parallel.dict.pickle : scripts/parallelize_wiki_dicts.py \
	$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG1)-$(SPECTRUMLANG2)-$(DUMPDATE).langlinks.csv \
	$(DATADIR)/wikipedia/dict/$(TARGETLANG)wiki-$(DUMPDATE).dict.pickle \
	$(DATADIR)/wikipedia/dict/$(SPECTRUMLANG1)wiki-$(DUMPDATE).dict.pickle \
	$(DATADIR)/wikipedia/dict/$(SPECTRUMLANG2)wiki-$(DUMPDATE).dict.pickle
	$(PYTHON) $^ $@
	
# Run LDA over dumps

$(DATADIR)/lda/%.lda.pickle : scripts/train_lda.py \
	$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/%.dict.pickle
	$(PYTHON) $^ $@

topicmodel: $(DATADIR)/lda/$(COMBINED_ID).parallel.lda.pickle
