from flask import Flask, Response, request
from flask import jsonify
from src.download_comment import script as script
from src.ml.ml import Ml
from src.preproc_data.processing_data import Processing

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


"""
Exemple de JSON pour la requete POST 
{
    "ids_videos" : [
        "g0Y98HpdIS4",
        "HlRNt30zdJU"
    ]
}
"""
@app.route('/get_comments',  methods = ['POST'])
def execute_script_data():
    json = request.json
    ids_videos = json["ids_videos"]

    script.script.get_comments(ids_videos)

    with open("data/comments-youtube.csv") as fp:
        csv = fp.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=./data/comments-youtube.csv"}
    )

@app.route('/train_model')
def execute_train():
    # Procesing data
    p = Processing()
    df_transform = p.apply()

    # Train and Save model
    ml = Ml(df_transform)
    acc = ml.train()

    return jsonify({
        "acc": acc.tolist(),
    })

@app.route('/predict',  methods = ['POST'])
def train():
    json = request.json


if __name__ == '__main__':
    app.run()
