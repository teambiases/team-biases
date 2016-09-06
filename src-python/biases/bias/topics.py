
import pickle
import numpy as np

from sklearn.neighbors import KNeighborsRegressor

class TopicsBiasModel:
    """Bias model that uses topic modeling and a KNN regression to place
    documents on the three-viewpoint spectrum."""
    
    def __init__(self, topics_corpus_fname, k = 5):
        """Creates a topic-modeling bias model from the given corpus as
        outputted by build_topics_corpus.py. k is the parameter for the
        KNN regression"""
        
        with open(topics_corpus_fname, 'rb') as topics_corpus_file:
            self.topics_corpus = pickle.load(topics_corpus_file)
            
        self.k = k
        # Add all articles from spectrum viewpoints as training data
        self.X = np.vstack([topics for _, _, topics in self.topics_corpus[1:]])
        # Labels are -1 for spectrum viewpoint 1, 1 for spectrum viewpoint 2
        self.y = [-1] * len(self.topics_corpus[1][1]) + \
                 [1] * len(self.topics_corpus[2][1])
        
        # Create index of lang, title pairs so that we can tell which articles
        # KNN model is returning
        self.lang_title_index = []
        for lang, titles, _ in self.topics_corpus[1:]:
            for title in titles:
                self.lang_title_index.append((lang, title))
                
        # Map from target lang titles to topic distributions
        self.target_lang_topics = {}
        for row, title in enumerate(self.topics_corpus[0][1]):
            self.target_lang_topics[title] = self.topics_corpus[0][2][row]
        
        self.fit()
        
    def fit(self):
        """Refits the KNN regression model."""
        
        self.knn_model = KNeighborsRegressor(n_neighbors=self.k,
                                             weights='distance')
        self.knn_model.fit(self.X, self.y)

    def predict(self, title):
        """Given a title of an article that is in the corpus, predicts a bias
        score from -1 to 1."""
        
        return self.knn_model.predict(self.target_lang_topics[title])

    def predict_verbose(self, title):
        """Given a title of an article that is in the corpus, predicts a bias
        score and also returns other information, including the n most similar
        articles' titles and languages, their topic distributions,
        and distances to the given article. Returns a 2-tuple where the
        first element is the bias score and the second element is a list of
        similar articles, each of which is a 4-tuple
        (lang, title, topics, distance)."""
        
        bias_score = self.predict(title)
        
        dists, inds = self.knn_model.kneighbors(self.target_lang_topics[title])
        dists, inds = dists[0], inds[0]
        articles = []
        for dist, ind in zip(dists, inds):
            lang, title = self.lang_title_index[ind]
            topics = self.X[ind]
            articles.append((lang, title, topics, dist))
            
        return bias_score, articles
    
    def target_lang_titles(self):
        """Returns all titles of articles in the target language."""
        return self.target_lang_topics.keys()
    
    def langs(self):
        """Returns all languages in this model's corpus: target and both
        spectrum languages."""
        return [lang for lang, _, _ in self.topics_corpus]
