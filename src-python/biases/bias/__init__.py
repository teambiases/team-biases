"""Methods for automatic detection of bias."""

class BiasModel(object):
    """
    A model for predicting the bias of an article along a particular spectrum.
    """
    
    def predict(self, document, lang):
        """
        This method should predict the bias score of a particular document in
        a particular language. The bias score should range from 0 to 1 (the
        meaning depends on what endpoints the bias model was trained on). The
        input document is represented as a list of sentences, where each
        sentence is a list of tokens.
        """
        raise NotImplementedError()
