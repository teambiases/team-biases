
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
CORPUS_QUERY="subcategories_of('Categoría:Guerra_Fría') > 0"
CORPUS_NAME=coldwar

LDA_TOPICS=2000
LDA_PASSES=5

.PRECIOUS: $(DATADIR)/wikipedia/dict/%.dict.pickle
.INTERMEDIATE: $(LIBDIR)/spark-%.tgz
.PHONY: topicmodel topicscorpus

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
	
# Build category trees from dumps
$(DATADIR)/wikipedia/categories/%.categories.pickle : scripts/extract_categories.py $(DATADIR)/wikipedia/dump/%-pages-articles.xml.bz2
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@

# Creating tf-idf matrix market files from corpora and dictionaries
$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 : scripts/build_wiki_vectors.py $(DATADIR)/wikipedia/dump/%-pages-articles.xml.bz2 $(DATADIR)/wikipedia/dict/%.dict.pickle
	$(PYTHON) $^ $(patsubst %.bz2,%,$@)
	bzip2 -f $(patsubst %.bz2,%,$@)
	
# Extract langlinks
$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG1)-$(SPECTRUMLANG2)-$(DUMPDATE).langlinks.csv : \
	scripts/export_dump_langlinks_csv.py \
	$(DATADIR)/wikipedia/dump/$(TARGETLANG)wiki-$(DUMPDATE)-langlinks.sql.gz \
	$(DATADIR)/wikipedia/vector/$(TARGETLANG)wiki-$(DUMPDATE).tfidf.mm.bz2
	$(PYTHON) $^ $@ $(TARGETLANG) $(SPECTRUMLANG1) $(SPECTRUMLANG2)
	
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
	
# Run LDA over dumps (first rule for when topic number is unspecified)

$(DATADIR)/lda/%.lda.pickle : scripts/train_lda.py \
	$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/%.dict.pickle
	$(PYTHON) $^ $@

$(DATADIR)/lda/%.$(LDA_TOPICS)t.lda.pickle : scripts/train_lda.py \
	$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/%.dict.pickle
	$(PYTHON) $^ $@ $(LDA_TOPICS) $(LDA_PASSES)
	
# Output LDA topics to CSV
	
$(DATADIR)/lda/%.lda.topics.csv : scripts/lda_to_csv.py $(DATADIR)/lda/%.lda.pickle
	$(PYTHON) $^ $@

topicmodel: $(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.pickle \
	$(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.topics.csv
	
# Create corpus through text search

$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).titles.txt : scripts/search_dump.py \
	$(DATADIR)/wikipedia/dump/$(TARGETLANG)wiki-$(DUMPDATE)-pages-articles.xml.bz2 \
	$(DATADIR)/wikipedia/vector/$(TARGETLANG)wiki-$(DUMPDATE).tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/$(TARGETLANG)wiki-$(DUMPDATE).dict.pickle \
	$(DATADIR)/wikipedia/categories/$(TARGETLANG)wiki-$(DUMPDATE).categories.pickle
	$(PYTHON) $^ $@ $(CORPUS_QUERY)
	
# Create corpus with topics

$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.pickle : scripts/build_topics_corpus.py \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).titles.txt \
	$(DATADIR)/wikipedia/vector/$(COMBINED_ID).parallel.tfidf.mm.bz2 \
	$(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.pickle
	$(PYTHON) $^ $@
	
topicscorpus: $(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.pickle
