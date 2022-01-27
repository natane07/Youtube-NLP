import streamlit as st
import requests
from pandas import json_normalize
from st_aggrid import AgGrid, GridOptionsBuilder
from urllib.parse import urlparse
from st_aggrid.shared import JsCode

def call_api(id_video):
    json_send = {"id_video": id_video}
    response = requests.post('http://127.0.0.1:5000/predict', json=json_send)
    jsonResponse = response.json()
    return jsonResponse

st.title("Vos commentaires youtube sont il pertinent ?")
text_input = st.text_input("Url youtube", "")

if text_input != "":
    # Parse de l'url
    url = urlparse(text_input)

    try:
      id_video = url.query.replace("v=", "")
      # Call de l'api
      data = call_api(id_video)
      df_comments = json_normalize(data, 'comments')
      df_comments = df_comments[["label_name", "comment"]]

      # Affichage de la vidéo youtube
      st.video(text_input, format="video/mp4", start_time=0)

      # Affichage des metrics
      col1, col2, col3 = st.columns(3)
      col1.metric("Nombre de commentaire", data["nb_pertinent"] + data["nb_non_pertinent"])
      col2.metric("Commentaire pertinent", data["nb_pertinent"])
      col3.metric("Commentaire non pertinent", data["nb_non_pertinent"])

      # Tableau des données
      st.header('Tableau des commentaires')
      gb = GridOptionsBuilder.from_dataframe(df_comments)
      gb.configure_pagination()
      gb.configure_side_bar()
      gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
      cellsytle_jscode = JsCode(
        """function(params) {
            if (params.value.includes('Pertinent')) {
                return {
                    'color': 'white',
                    'backgroundColor': 'green'
                }
            } else {
                return {
                    'color': 'white',
                    'backgroundColor': 'red'
                }
            }
        };"""
      )

      gb.configure_column("label_name", cellStyle=cellsytle_jscode)
      gridOptions = gb.build()
      AgGrid(
        df_comments,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True
      )
    except:
      st.error('Vidéo Youtube introuvable')