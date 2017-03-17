"""
Utilities having to do with translation.
"""

import os
import shelve
from os.path import dirname, realpath, sep, pardir
from google.cloud import translate

class CachedTranslationClient(object):
    """
    Similar to the Google Cloud Translate client object, but caches the
    translation results to avoid excessive requests to the API.
    """
    
    def __init__(self):
        # Configure translation API keys
        credentials_file = sep.join([dirname(realpath(__file__)), pardir,
                pardir, pardir, 'config', 'Team-BIASES-3948f0cc1da3.json'])
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
        
        self.client = translate.Client()
        
        self.shelf = shelve.open('data/cache/translate.google.shelf')
        
    def __del__(self):
        self.shelf.close()
        
    def _make_cache_key(self, value, source_language, target_language):
        return '{}->{} {}'.format(source_language or '', target_language,
                                  value)
        
    def translate(self, values, target_language='en', source_language=None):
        """
        Given a list of strings in values, translates them all to the
        given target language, either detecting the language or using the
        specified source language.
        """
        
        query_index = 0
        query_index_map = {}
        query_values = []
        results = []
        
        for index, value in enumerate(values):
            cache_key = self._make_cache_key(value, source_language,
                                             target_language)
            if cache_key in self.shelf:
                results.append(self.shelf[cache_key])
            else:
                results.append(None)
                query_values.append(value)
                query_index_map[query_index] = index
                query_index += 1
        
        print(query_values)
        if len(query_values) > 0:
            query_results = self.client.translate(query_values,
                    target_language=target_language,
                    source_language=source_language)
        else:
            query_results = []
        
        for query_index, result in enumerate(query_results):
            index = query_index_map[query_index]
            cache_key = self._make_cache_key(values[index], source_language,
                                             target_language)
            self.shelf[cache_key] = result
            results[index] = result
            
        return results
    
translation_client = CachedTranslationClient()
