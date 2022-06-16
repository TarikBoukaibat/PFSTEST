import sklearn.externals
import joblib
 
from flask import Flask, jsonify, request
import Preprocess
import Getter
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

Vectorizer = joblib.load("Vocabulary/vectorizer.pkl")
HOST = '0.0.0.0'
PORT =8081

@app.route('/api/analyse', methods = ['GET','POST'])

def analyse():
    #recupérer les informations de la requête
    req = request.get_json()

    #chargement du modèle
    if req['model'] == 'Support Vector Machine (SVM)':
        Model = joblib.load("Models/Model_SVM.pkl")
    elif req['model'] == 'Logistic Regression':
        Model = joblib.load("Models/Model_LogiticRegression.pkl")
    elif req['model'] == 'Naives Bayes':
        Model = joblib.load("Models/Model_NBC.pkl")

    #parametre pour la recherche
    date_debut = req['start_date']
    date_fin = req['end_date']
    keywords = req['tweet']
    limit = 50 # le nombre de tweets à récupérer à chaque analyse

    tweet_df = Getter.get_tweets(keywords,date_debut,date_fin,limit)

    #creation d'une colonne contenant les tweets prétraités

    tweet_df['tweet_cleaned'] = tweet_df['tweet'].apply(Preprocess.process_tweet)

    #transformation des tweets en vecteurs et application du modèle
    tweet_df['predicted_value'] = None
    for i in tweet_df.index:
        tweet_df['predicted_value'][i] = Model.predict(Vectorizer.transform([tweet_df['tweet_cleaned'][i]]))[0]

    positive_at_count = tweet_df.loc[tweet_df['predicted_value'] == 1]['predicted_value'].count()
    negative_at_count = tweet_df.loc[tweet_df['predicted_value'] == 0]['predicted_value'].count()
    
    return jsonify([{'name':'positive','value':int(positive_at_count)},
                    {'name':'negative','value':int(negative_at_count)}])



@app.route('/api/GetPolarity', methods=['GET', 'POST'])

def GetPolarity():
    # recupérer les informations de la requête
    requ = request.get_json()

    tweet=requ['text']

    # chargement du modèle
    model = joblib.load("Models/Model_LogiticRegression.pkl")


    # parametre pour la recherch
    # creation d'une colonne contenant les tweets prétraités

    tweet_cleaned = Preprocess.process_tweet(tweet)

    # transformation des tweets en vecteurs et application du modèle

    predicted_value =model.predict(Vectorizer.transform([tweet_cleaned]))

    return jsonify([{'name':'pred','value':int(predicted_value[0])}])



'''return jsonify([{'name': 'positive', 'value': 10},
        {'name': 'negative', 'value': 10}])'''

'''@app.errorhandler(500)
def internal_error(error):

return "500 error"

@app.errorhandler(404)
def not_found(error):
return "404 error",404'''

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)
    app.debug = True
