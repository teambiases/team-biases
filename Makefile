
PYTHON=python3
DATADIR=data
LIBDIR=lib

SPARKVERSION=2.0.0-bin-hadoop2.7
SPARKDIR=$(LIBDIR)/spark-$(SPARKVERSION)

TARGETLANG=es
SPECTRUMLANG0=en
SPECTRUMLANG1=ru
DUMPDATE=20170120
COMBINED_ID=$(TARGETLANG)-$(SPECTRUMLANG0)-$(SPECTRUMLANG1)-wiki-$(DUMPDATE)
CORPUS_QUERY="categories_in(['Categoría:Guerra_Fría', 'Categoría:Alemania_Occidental', 'Categoría:Unión_Soviética', 'Categoría:Cultura_de_la_Unión_Soviética', 'Categoría:Terminología_soviética', 'Categoría:Símbolos_de_la_Unión_Soviética', 'Categoría:Arte_de_la_Unión_Soviética', 'Categoría:Realismo_socialista', 'Categoría:Historia_de_la_Unión_Soviética', 'Categoría:Represión_política_en_la_Unión_Soviética', 'Categoría:Gulag', 'Categoría:Gran_Purga', 'Categoría:Relaciones_internacionales_de_la_Unión_Soviética', 'Categoría:Relaciones_bilaterales_de_la_Unión_Soviética', 'Categoría:Relaciones_Turquía-Unión_Soviética', 'Categoría:Relaciones_Checoslovaquia-Unión_Soviética', 'Categoría:Relaciones_Hungría-Unión_Soviética', 'Categoría:Relaciones_India-Unión_Soviética', 'Categoría:Relaciones_Reino_Unido-Unión_Soviética', 'Categoría:Relaciones_Mongolia-Unión_Soviética', 'Categoría:Relaciones_Irán-Unión_Soviética', 'Categoría:Relaciones_Francia-Unión_Soviética', 'Categoría:Relaciones_México-Unión_Soviética', 'Categoría:Relaciones_Alemania-Unión_Soviética', 'Categoría:Relaciones_Unión_Soviética-Uruguay', 'Categoría:Relaciones_Unión_Soviética-Vietnam', 'Categoría:Relaciones_Suiza-Unión_Soviética', 'Categoría:Relaciones_Polonia-Unión_Soviética', 'Categoría:Relaciones_China-Unión_Soviética', 'Categoría:Relaciones_Bulgaria-Unión_Soviética', 'Categoría:Relaciones_Estados_Unidos-Unión_Soviética', 'Categoría:Relaciones_Cuba-Unión_Soviética', 'Categoría:Relaciones_España-Unión_Soviética', 'Categoría:Relaciones_Rumania-Unión_Soviética', 'Categoría:Ocupaciones_militares_de_la_Unión_Soviética', 'Categoría:Espías_de_la_Unión_Soviética', 'Categoría:Guerras_de_la_Unión_Soviética', 'Categoría:Resoluciones_del_Consejo_de_Seguridad_de_las_Naciones_Unidas_referentes_a_la_Unión_Soviética', 'Categoría:Símbolos_de_la_Unión_Soviética', 'Categoría:Propaganda_de_la_Unión_Soviética', 'Categoría:Resoluciones_del_Consejo_de_Seguridad_de_las_Naciones_Unidas_referentes_a_la_Unión_Soviética', 'Categoría:KGB', 'Categoría:Disolución_de_la_Unión_Soviética', 'Categoría:Tratados_de_la_Unión_Soviética', 'Categoría:Símbolos_de_la_Unión_Soviética', 'Categoría:Política_de_la_Unión_Soviética', 'Categoría:Partido_Comunista_de_la_Unión_Soviética', 'Categoría:KGB', 'Categoría:NKVD', 'Categoría:Represión_política_en_la_Unión_Soviética', 'Categoría:Relaciones_internacionales_de_la_Unión_Soviética', 'Categoría:Propaganda_de_la_Unión_Soviética', 'Categoría:Tratados_de_la_Unión_Soviética', 'Categoría:Unión_de_Partidos_Comunistas', 'Categoría:Políticos_de_la_Unión_Soviética', 'Categoría:Derecho_de_la_Unión_Soviética', 'Categoría:Tratados_de_la_Unión_Soviética', 'Categoría:Constituciones_de_la_Unión_Soviética', 'Categoría:Represión_política_en_la_Unión_Soviética', 'Categoría:Derechos_humanos_en_la_Unión_Soviética', 'Categoría:Sociedad_de_la_Unión_Soviética', 'Categoría:Cultura_de_la_Unión_Soviética', 'Categoría:Derechos_humanos_en_la_Unión_Soviética', 'Categoría:Soviéticos', 'Categoría:Diáspora_soviética', 'Categoría:Emigrantes_de_la_Unión_Soviética', 'Categoría:Ejecutados_de_la_Unión_Soviética', 'Categoría:Economía_de_la_Unión_Soviética', 'Categoría:Primavera_de_Praga', 'Categoría:Operación_Cóndor', 'Categoría:Terrorismo_de_Estado_en_Argentina_en_las_décadas_de_1970_y_1980', 'Categoría:Escuela_de_las_Américas', 'Categoría:Conflictos_de_la_Guerra_Fría', 'Categoría:Historia_de_Estados_Unidos_(1945-1989)', 'Categoría:Zona_de_ocupación_estadounidense', 'Categoría:Intervenciones_militares_de_Cuba', 'Categoría:Revolución_Sandinista', 'Categoría:Conferencias_de_la_Segunda_Guerra_Mundial', 'Categoría:Revoluciones_de_1989', 'Categoría:Muro_de_Berlín', 'Categoría:Anticomunismo', 'Categoría:Revoluciones_de_1989', 'Categoría:Propaganda_anticomunista', 'Categoría:Espías_de_la_Guerra_Fría', 'Categoría:Directores_del_KGB', 'Categoría:Operaciones_de_la_KGB', 'Categoría:Agentes_del_KGB', 'Categoría:Bloque_del_Este', 'Categoría:Primavera_de_Praga']) > 0"
CORPUS_NAME=coldwar

ENDPOINT0=dem
ENDPOINT1=rep

SAMPLE_SEED=dec2016
SAMPLE_ARTICLES=15
SAMPLE_CHUNKS=3

LDA_TOPICS=400
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
	mkdir -p $(dir $@)
	$(PYTHON) $^ $(patsubst %.bz2,%,$@)
	bzip2 -f $(patsubst %.bz2,%,$@)
	
# Extract langlinks
$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG0)-$(SPECTRUMLANG1)-$(DUMPDATE).langlinks.csv : \
	scripts/export_dump_langlinks_csv.py \
	$(DATADIR)/wikipedia/dump/$(TARGETLANG)wiki-$(DUMPDATE)-langlinks.sql.gz \
	$(DATADIR)/wikipedia/vector/$(TARGETLANG)wiki-$(DUMPDATE).tfidf.mm.bz2
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@ $(TARGETLANG) $(SPECTRUMLANG0) $(SPECTRUMLANG1)
	
# Combine matrix market files and sort

$(DATADIR)/wikipedia/vector/$(COMBINED_ID).parallel.tfidf.mm.bz2 : scripts/parallelize_wiki_vectors.py \
	$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG0)-$(SPECTRUMLANG1)-$(DUMPDATE).langlinks.csv \
	$(DATADIR)/wikipedia/vector/$(TARGETLANG)wiki-$(DUMPDATE).tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/vector/$(SPECTRUMLANG0)wiki-$(DUMPDATE).tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/vector/$(SPECTRUMLANG1)wiki-$(DUMPDATE).tfidf.mm.bz2
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
# Combine dictionaries

$(DATADIR)/wikipedia/dict/$(COMBINED_ID).parallel.dict.pickle : scripts/parallelize_wiki_dicts.py \
	$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG0)-$(SPECTRUMLANG1)-$(DUMPDATE).langlinks.csv \
	$(DATADIR)/wikipedia/dict/$(TARGETLANG)wiki-$(DUMPDATE).dict.pickle \
	$(DATADIR)/wikipedia/dict/$(SPECTRUMLANG0)wiki-$(DUMPDATE).dict.pickle \
	$(DATADIR)/wikipedia/dict/$(SPECTRUMLANG1)wiki-$(DUMPDATE).dict.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
# Filter matrix market files given a list of titles

$(DATADIR)/wikipedia/vector/$(CORPUS_NAME).$(COMBINED_ID).parallel.tfidf.mm.bz2 : scripts/filter_wiki_vectors.py \
	$(DATADIR)/wikipedia/vector/$(COMBINED_ID).parallel.tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).titles.txt
	$(PYTHON) $^ $@
	
# Run LDA over dumps (first rule for when topic number is unspecified)

$(DATADIR)/lda/%.lda.pickle : scripts/train_lda.py \
	$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/%.dict.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@

$(DATADIR)/lda/%.$(LDA_TOPICS)t.lda.pickle : scripts/train_lda.py \
	$(DATADIR)/wikipedia/vector/%.tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/%.dict.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@ $(LDA_TOPICS) $(LDA_PASSES)
	
$(DATADIR)/lda/$(CORPUS_NAME).%.$(LDA_TOPICS)t.lda.pickle : scripts/train_lda.py \
	$(DATADIR)/wikipedia/vector/$(CORPUS_NAME).%.tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/%.dict.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@ $(LDA_TOPICS) 10
	
# Output LDA topics to CSV
	
$(DATADIR)/lda/%.lda.topics.csv : scripts/lda_to_csv.py $(DATADIR)/lda/%.lda.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@

topicmodel: $(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.pickle \
	$(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.topics.csv \
	$(DATADIR)/lda/$(CORPUS_NAME).$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.pickle \
	$(DATADIR)/lda/$(CORPUS_NAME).$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.topics.csv
	
# Create corpus through text search

$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).titles.txt : scripts/search_dump.py \
	$(DATADIR)/wikipedia/dump/$(TARGETLANG)wiki-$(DUMPDATE)-pages-articles.xml.bz2 \
	$(DATADIR)/wikipedia/vector/$(TARGETLANG)wiki-$(DUMPDATE).tfidf.mm.bz2 \
	$(DATADIR)/wikipedia/dict/$(TARGETLANG)wiki-$(DUMPDATE).dict.pickle \
	$(DATADIR)/wikipedia/categories/$(TARGETLANG)wiki-$(DUMPDATE).categories.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@ $(CORPUS_QUERY)
	
# Create corpus with topics

$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.pickle : scripts/build_topics_corpus.py \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).titles.txt \
	$(DATADIR)/wikipedia/vector/$(COMBINED_ID).parallel.tfidf.mm.bz2 \
	$(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
# Analyze corpus with topics

$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.analysis.csv : \
	scripts/analyze_topics_corpus.py \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.pickle \
	$(DATADIR)/lda/$(COMBINED_ID).parallel.$(LDA_TOPICS)t.lda.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
topicscorpus: $(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.pickle \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).$(LDA_TOPICS)topics.analysis.csv

# Split corpus into chunks

$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.pickle : scripts/split_chunks.py \
	$(DATADIR)/wikipedia/corpus/$(CORPUS_NAME).$(COMBINED_ID).titles.txt \
	$(DATADIR)/wikipedia/dump/$(TARGETLANG)wiki-$(DUMPDATE)-pages-articles.xml.bz2 \
	$(DATADIR)/wikipedia/langlinks/$(TARGETLANG)-$(SPECTRUMLANG0)-$(SPECTRUMLANG1)-$(DUMPDATE).langlinks.csv
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
# Sample chunks

$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.$(SAMPLE_SEED).sample.txt : scripts/sample_chunks.py \
	$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@ $(SAMPLE_ARTICLES) $(SAMPLE_CHUNKS) $(SAMPLE_SEED)
	
# Output mechanical turk tasks

$(DATADIR)/wikipedia/mturk/$(CORPUS_NAME).$(COMBINED_ID).$(SAMPLE_SEED).tasks.csv : scripts/sample_to_mturk_tasks.py \
	$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.$(SAMPLE_SEED).sample.txt \
	$(DATADIR)/wikipedia/chunks/$(CORPUS_NAME).$(COMBINED_ID).chunks.pickle
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
mturktasks: $(DATADIR)/wikipedia/mturk/$(CORPUS_NAME).$(COMBINED_ID).$(SAMPLE_SEED).tasks.csv

# Render versions of mechanical turk survey

web/mturk-wiki-bias/%.html : scripts/render_template.py web/mturk-wiki-bias/base.html web/mturk-wiki-bias/%.json
	$(PYTHON) $^ $@

# Analyze interannotator agreement

$(DATADIR)/wikipedia/mturk/%.results.agreement.txt : scripts/annotator_agreement.py \
	$(DATADIR)/wikipedia/mturk/%.results.csv
	$(PYTHON) $^ $@
	
# Convert mechanical turk results to bias scores

$(DATADIR)/wikipedia/bias/%.mturk.scores.csv : scripts/mturk_results_to_scores.py \
	$(DATADIR)/wikipedia/mturk/%.results.csv
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
	
# Train Gentzkow & Shapiro models

$(DATADIR)/gs/%.$(ENDPOINT0)-$(ENDPOINT1).gs.csv: scripts/train_gentzkow_shapiro.py \
	$(DATADIR)/endpoints/%.$(ENDPOINT0).txt \
	$(DATADIR)/endpoints/%.$(ENDPOINT1).txt \
    $(DATADIR)/gs/$(ENDPOINT0)-$(ENDPOINT1).gs.csv
	mkdir -p $(dir $@)
	$(PYTHON) $^ $@
