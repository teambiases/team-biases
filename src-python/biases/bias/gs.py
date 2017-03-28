"""Bias algorithms from Gentzkow & Shapiro (2010)."""

from biases.utils.translate import translation_client

def align_ngrams(lang_ngrams, length_limit=None):
    """
    Aligns ngrams from different languages into groups that are translations
    of one another. The input is expected to be a list of tuples
    (lang, ngrams), where lang is a two-letter language code (say 'en' or 'es')
    and ngrams is a list of ngrams that should be included in the final
    alignment.
    
    This returns a tuple (alignments, lookup). Alignments is a list of
    alignments, where each alignment is a list of (lang, ngram) tuples that
    all have the same meaning. lookup is a dictionary such that
    lookup[lang][ngram] gives a representative tuple of the alignment
    cooresponding to the given ngram in the given language.
    
    If length_limit is specified, then no possible translations longer than that
    length in words will be returned.
    """
    
    langs = [lang for lang, ngrams in lang_ngrams]
    lookup = {lang: {} for lang in langs}
    
    to_translate = set()
    for lang, ngrams in lang_ngrams:
        for ngram in ngrams:
            # Keep everything lowercase
            ngram = ngram.lower()
            lookup[lang][ngram] = [(lang, ngram)]
            to_translate.add((lang, ngram))
    
    while len(to_translate) > 0:
        # Perform translation
        new_to_translate = set()
        for from_lang in langs:
            from_lang_ngrams = [ngram for lang, ngram in to_translate if 
                                lang == from_lang]
            for to_lang in langs:
                if to_lang != from_lang and len(from_lang_ngrams) > 0:
                    to_lang_ngrams = [result['translatedText'] for result in 
                            translation_client.translate(from_lang_ngrams,
                            source_language=from_lang,
                            target_language=to_lang)]
                    for from_lang_ngram, to_lang_ngram in \
                            zip(from_lang_ngrams, to_lang_ngrams):
                        # Keep everything lowercase
                        to_lang_ngram = to_lang_ngram.lower()
                        # Make sure translation is under the length limit
                        if length_limit is None or \
                                len(to_lang_ngram.split()) <= length_limit:
                            from_lang_alignment = \
                                    lookup[from_lang][from_lang_ngram]
                            # If we've already seen this word
                            if to_lang_ngram in lookup[to_lang]:
                                to_lang_alignment = \
                                        lookup[to_lang][to_lang_ngram]
                                # If the alignments aren't already combined...
                                if to_lang_alignment is not \
                                        from_lang_alignment:
                                    # ...combine them
                                    from_lang_alignment.extend(
                                            to_lang_alignment)
                                    for align_lang, align_ngram in \
                                            to_lang_alignment:
                                        lookup[align_lang][align_ngram] = \
                                                from_lang_alignment
                            # If it's a new word
                            else:
                                from_lang_alignment.append((to_lang,
                                                            to_lang_ngram))
                                lookup[to_lang][to_lang_ngram] = \
                                        from_lang_alignment
                                new_to_translate.add((to_lang,
                                                      to_lang_ngram))
        to_translate = new_to_translate
    
    # Build alignments list
    alignment_ids = set()
    alignments = []
    for lang in langs:
        for ngram, alignment in lookup[lang].items():
            if id(alignment) not in alignment_ids:
                alignments.append(alignment)
                alignment_ids.add(id(alignment))
                
    alignment_id2tuple = {}
    for alignment in alignments:
        # Get the first aligned word in each language to make a tuple 
        # representation
        alignment_tuple = []
        for lang in langs:
            for ngram_lang, ngram in alignment:
                if ngram_lang == lang:
                    alignment_tuple.append(ngram)
                    break
        alignment_id2tuple[id(alignment)] = tuple(alignment_tuple)
    tuple_lookup = {lang: {ngram: alignment_id2tuple[id(lookup[lang][ngram])]
                         for ngram in lookup[lang]} for lang in langs}
                
    return alignments, tuple_lookup
