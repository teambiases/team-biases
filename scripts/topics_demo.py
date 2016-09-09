import _path_config

import sys, webbrowser, random, threading

from flask import Flask, jsonify, request
from os import path

from biases.bias.topics import TopicsBiasModel

static_folder = path.sep.join([path.dirname(path.realpath(__file__)),
                               path.pardir, 'web', 'topics-demo'])

app = Flask(__name__, static_url_path = '', static_folder = static_folder)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/titles/')
def titles():
    """Get titles of all articles that can be analyzed."""
    return jsonify([{'id': title, 'text': title.replace('_', ' ')} for
                    title in bias_model.target_lang_titles()])
    
@app.route('/langs/')
def langs():
    """Get langs present in the bias model."""
    return jsonify(bias_model.langs())
    
@app.route('/calculate-bias/')
def calculate_bias():
    """Calculate bias score for a particular article."""
    title = request.args['title']
    k = int(request.args['k'])
    bias_model.k = k
    bias_model.fit()
    bias_score, similar_articles = bias_model.predict_verbose(title)
    return jsonify({'biasScore': float(bias_score), 'similarArticles':
                    [{'lang': lang, 'title': title, 'topics': topics.tolist(),
                      'readableTitle': title.replace('_', ' '),
                      'distance': distance} for lang, title, topics, distance 
                     in similar_articles],
                    'topics': bias_model.target_lang_topics[title].tolist(),
                    'readableTitle': title.replace('_', ' ')})

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: topics_demo.py topics_corpus.pickle')
        print('Loads the given topics_corpus and runs a web-based demo of the TopicsBiasModel.')
    else:
        global bias_model
        bias_model = TopicsBiasModel(sys.argv[1])
        
        # Choose random port and open index page in user's web browser
        port = 8000 + random.randint(0, 999)
        url = 'http://localhost:{}/'.format(port)
        threading.Timer(1.25, lambda: webbrowser.open(url)).start()
        app.run(port = port)
