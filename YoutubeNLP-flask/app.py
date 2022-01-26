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

    with open("./data/comments-youtube.csv") as fp:
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

"""
Exemple de JSON pour la requete POST 
{
    "id_video": "g0Y98HpdIS4"
}
"""
@app.route('/predict',  methods = ['POST'])
def predict():
    json = request.json
    id_video = json["id_video"]

    # Récuperation des commentaires youtubes
    df_comments = script.script.get_comment(id_video)

    # Processing des données
    df_process = Processing.clean_data(df_comments)
    df_process = df_process.reset_index()

    # Predict label comments
    df_feature = df_process['comment'].values
    predict_label = Ml.predict(df_feature)
    predict_label = [(int(label)) for label in predict_label]

    # Prepare Json response
    df_process["label"] = predict_label
    df_process = df_process[["comment", "label"]]
    nb_pertinent = int(df_process["label"].sum())
    nb_comments = int(df_process["label"].count())
    json_dict = {
        "comments": [],
        "nb_pertinent": nb_pertinent,
        "nb_non_pertinent": nb_comments - nb_pertinent
    }
    for index, row in df_process.iterrows():
        value = {
            "comment": row['comment'],
            "label": row['label'],
            "label_name": "Non pertinent" if row['label'] == 0 else "Pertinent"
        }
        json_dict["comments"].append(value)
    return jsonify(json_dict)

if __name__ == '__main__':
    app.run()
