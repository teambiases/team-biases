"""Methods for automatic detection of bias."""

import random

class BiasModel(object):
    """
    A model for predicting the bias of an article along a particular spectrum.
    """
    
    def load(self):
        """
        Load any necessary data for this model. This can be used if data is
        stored outside the model file.
        """
        pass
    
    def predict(self, document, lang):
        """
        This method should predict the bias score of a particular document in
        a particular language. The bias score should range from 0 to 1 (the
        meaning depends on what endpoints the bias model was trained on). The
        input document is represented as a list of sentences, where each
        sentence is a list of tokens.
        """
        raise NotImplementedError()

class RandomBiasModel(object):
    """
    A model that returns a random bias score for any document. This can be
    useful for testing code that requires a bias model.
    """
    
    def __init__(self):
        self.is_loaded = False
    
    def load(self):
        self.is_loaded = True
        
    def predict(self, document, lang):
        if self.is_loaded:
            # Make sure document is as expected
            ' '.join(' '.join(sentence) for sentence in document)
            return random.random()
        else:
            raise RuntimeError('The load() method was not called on this '
                               'model.')
