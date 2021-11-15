from flask import Flask, Response, request
import script as script
app = Flask(__name__)

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

    with open("./comments-youtube.csv") as fp:
        csv = fp.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":"attachment; filename=comments-youtube.csv"}
    )


if __name__ == '__main__':
    app.run()
