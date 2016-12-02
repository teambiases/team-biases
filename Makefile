
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
CORPUS_QUERY="categories_in(['Categoría:Guerra_Fría', 'Categoría:Alemania_Occidental', 'Categoría:Unión_Soviética', 'Categoría:Cultura_de_la_Unión_Soviética', 'Categoría:Terminología_soviética', 'Categoría:Símbolos_de_la_Unión_Soviética', 'Categoría:Arte_de_la_Unión_Soviética', 'Categoría:Realismo_socialista', 'Categoría:Historia_de_la_Unión_Soviética', 'Categoría:Represión_política_en_la_Unión_Soviética', 'Categoría:Gulag', 'Categoría:Gran_Purga', 'Categoría:Relaciones_internacionales_de_la_Unión_Soviética', 'Categoría:Relaciones_bilaterales_de_la_Unión_Soviética', 'Categoría:Relaciones_Turquía-Unión_Soviética', 'Categoría:Relaciones_Checoslovaquia-Unión_Soviética', 'Categoría:Relaciones_Hungría-Unión_Soviética', 'Categoría:Relaciones_India-Unión_Soviética', 'Categoría:Relaciones_Reino_Unido-Unión_Soviética', 'Categoría:Relaciones_Mongolia-Unión_Soviética', 'Categoría:Relaciones_Irán-Unión_Soviética', 'Categoría:Relaciones_Francia-Unión_Soviética', 'Categoría:Relaciones_México-Unión_Soviética', 'Categoría:Relaciones_Alemania-Unión_Soviética', 'Categoría:Relaciones_Unión_Soviética-Uruguay', 'Categoría:Relaciones_Unión_Soviética-Vietnam', 'Categoría:Relaciones_Suiza-Unión_Soviética', 'Categoría:Relaciones_Polonia-Unión_Soviética', 'Categoría:Relaciones_China-Unión_Soviética', 'Categoría:Relaciones_Bulgaria-Unión_Soviética', 'Categoría:Relaciones_Estados_Unidos-Unión_Soviética', 'Categoría:Relaciones_Cuba-Unión_Soviética', 'Categoría:Relaciones_España-Unión_Soviética', 'Categoría:Relaciones_Rumania-Unión_Soviética', 'Categoría:Ocupaciones_militares_de_la_Unión_Soviética', 'Categoría:Espías_de_la_Unión_Soviética', 'Categoría:Guerras_de_la_Unión_Soviética', 'Categoría:Resoluciones_del_Consejo_de_Seguridad_de_las_Naciones_Unidas_referentes_a_la_Unión_Soviética', 'Categoría:Símbolos_de_la_Unión_Soviética', 'Categoría:Propaganda_de_la_Unión_Soviética', 'Categoría:Resoluciones_del_Consejo_de_Seguridad_de_las_Naciones_Unidas_referentes_a_la_Unión_Soviética', 'Categoría:KGB', 'Categoría:Disolución_de_la_Unión_Soviética', 'Categoría:Tratados_de_la_Unión_Soviética', 'Categoría:Símbolos_de_la_Unión_Soviética', 'Categoría:Política_de_la_Unión_Soviética', 'Categoría:Partido_Comunista_de_la_Unión_Soviética', 'Categoría:KGB', 'Categoría:NKVD', 'Categoría:Represión_política_en_la_Unión_Soviética', 'Categoría:Relaciones_internacionales_de_la_Unión_Soviética', 'Categoría:Propaganda_de_la_Unión_Soviética', 'Categoría:Tratados_de_la_Unión_Soviética', 'Categoría:Unión_de_Partidos_Comunistas', 'Categoría:Políticos_de_la_Unión_Soviética', 'Categoría:Derecho_de_la_Unión_Soviética', 'Categoría:Tratados_de_la_Unión_Soviética', 'Categoría:Constituciones_de_la_Unión_Soviética', 'Categoría:Represión_política_en_la_Unión_Soviética', 'Categoría:Derechos_humanos_en_la_Unión_Soviética', 'Categoría:Sociedad_de_la_Unión_Soviética', 'Categoría:Cultura_de_la_Unión_Soviética', 'Categoría:Derechos_humanos_en_la_Unión_Soviética', 'Categoría:Soviéticos', 'Categoría:Diáspora_soviética', 'Categoría:Emigrantes_de_la_Unión_Soviética', 'Categoría:Ejecutados_de_la_Unión_Soviética', 'Categoría:Economía_de_la_Unión_Soviética', 'Categoría:Primavera_de_Praga', 'Categoría:Operación_Cóndor', 'Categoría:Terrorismo_de_Estado_en_Argentina_en_las_décadas_de_1970_y_1980', 'Categoría:Escuela_de_las_Américas', 'Categoría:Conflictos_de_la_Guerra_Fría', 'Categoría:Historia_de_Estados_Unidos_(1945-1989)', 'Categoría:Zona_de_ocupación_estadounidense', 'Categoría:Intervenciones_militares_de_Cuba', 'Categoría:Revolución_Sandinista', 'Categoría:Conferencias_de_la_Segunda_Guerra_Mundial', 'Categoría:Revoluciones_de_1989', 'Categoría:Muro_de_Berlín', 'Categoría:Anticomunismo', 'Categoría:Revoluciones_de_1989', 'Categoría:Propaganda_anticomunista', 'Categoría:Espías_de_la_Guerra_Fría', 'Categoría:Directores_del_KGB', 'Categoría:Operaciones_de_la_KGB', 'Categoría:Agentes_del_KGB', 'Categoría:Bloque_del_Este', 'Categoría:Primavera_de_Praga']) > 0"
CORPUS_NAME=coldwar

SAMPLE_SEED=nov2016

LDA_TOPICS=100
LDA_PASSES=3

.PRECIOUS: $(DATADIR)/wikipedia/dict/%.dict.pickle
.INTERMEDIATE: $(LIBDIR)/spark-%.tgz
.PHONY: topicmodel topicscorpus mturktasks

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
	
# Analyze corpus with topics

$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.analysis.csv : \
	scripts/analyze_topics_corpus.py \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.pickle \
	$(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.pickle
	$(PYTHON) $^ $@
	
topicscorpus: $(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.pickle \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.analysis.csv

# Split corpus into chunks

$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.pickle : scripts/split_chunks.py \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).titles.txt \
	$(DATADIR)/wikipedia/dump/$(TARGETLANG)wiki-$(DUMPDATE)-pages-articles.xml.bz2 \
	$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG1)-$(SPECTRUMLANG2)-$(DUMPDATE).langlinks.csv
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
# Sample chunks

$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.$(SAMPLE_SEED).sample.txt : scripts/sample_chunks.py \
	$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@ $(SAMPLE_SEED)
	
# Output mechanical turk tasks

$(DATADIR)/wikipedia/mturk/$(CORPUS_NAME).$(COMBINED_ID).$(SAMPLE_SEED).tasks.csv : scripts/sample_to_mturk_tasks.py \
	$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.$(SAMPLE_SEED).sample.txt \
	$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@ $(SAMPLE_SEED)
	
mturktasks: $(DATADIR)/wikipedia/mturk/$(CORPUS_NAME).$(COMBINED_ID).$(SAMPLE_SEED).tasks.csv

# Render versions of mechanical turk survey

web/mturk-wiki-bias/%.html : scripts/render_template.py web/mturk-wiki-bias/base.html web/mturk-wiki-bias/%.json
	$(PYTHON) $^ $@
