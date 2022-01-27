import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load
import pickle

from src.preproc_data.processing_data import Processing



class Ml():

    def __init__(self, df):
        self.df = df
        self.X = df['comment'].values
        self.Y = df['label'].values

    def train(self):
        # Transformation du text en vecteur
        X_tfidf = self.transform_text_to_vector_tf_idf(self.X)

        # Creation du modele Naive Bayes + train
        model = MultinomialNB().fit(X_tfidf, self.Y)
        # Accuracy du model
        scores = cross_val_score(model, X_tfidf, self.Y)
        # Save du modele
        dump(model, './model/model_nb.joblib')

        return scores


    @staticmethod
    def predict(data):
        # Load Vector an TFIDF model
        filename_model_vector = './model/vector_model.pkl'
        with open(filename_model_vector, 'rb') as f:
            model_vec = pickle.load(f)
        X = model_vec.transform(data)

        filename_model_tfidf = './model/tfidf_model.pkl'
        with open(filename_model_tfidf, 'rb') as f:
            model_tfidf = pickle.load(f)
        X_tfidf = model_tfidf.transform(X)

        # Load du model NB
        model = load('./model/model_nb.joblib')
        # Prediction
        predicted = model.predict(X_tfidf)
        return predicted

    def transform_text_to_vector_tf_idf(self, X):
        # Transformation des données en vecteurs
        vector = CountVectorizer()
        X_vector = vector.fit_transform(X)
        # Save Vector model
        filename = './model/vector_model.pkl'
        with open(filename, 'wb') as m:
            pickle.dump(vector, m)

        # TF-IDF vectorize.
        tfidf_transformer = TfidfTransformer()
        X_tfidf = tfidf_transformer.fit_transform(X_vector)
        # Save Vector and TF-IDF model
        filename = './model/tfidf_model.pkl'
        with open(filename, 'wb') as fo:
            pickle.dump(tfidf_transformer, fo)

        return X_tfidf


if __name__ == '__main__':
    train = False
    if train:
        p = Processing()
        df_transform = p.apply()
        df_transform = df_transform.reset_index()
        print("ML")
        ml = Ml(df_transform)
        ml.train()
        print("fin Train")
    else:
        docs_new = ['God is love', 'OpenGL on the GPU is fast', "United states goes to Iraq"]
        predict = Ml.predict(docs_new)
        print(docs_new, predict)


