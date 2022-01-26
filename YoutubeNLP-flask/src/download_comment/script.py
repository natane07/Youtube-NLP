from src import utils
import pandas as pd

class script():

    @staticmethod
    def get_comments(ids_videos):
        nb_videos = 0
        for id in ids_videos:
            response = utils.Utils.call_api_youtube_comments(id)
            data = utils.Utils.parse_request_youtube(response)
            print(len(data))
            nb_videos += len(data)
            data = [[x[0], script.clean_data(x[1]), x[2]] for x in data]
            utils.Utils.whrite_csv(data)
        print(nb_videos)

    @staticmethod
    def get_comment(id_video):
        response = utils.Utils.call_api_youtube_comments(id_video, 200)
        data = utils.Utils.parse_request_youtube(response)
        print(len(data))
        data = [[x[0], script.clean_data(x[1]), x[2]] for x in data]
        column_names = ["video_Id", "comment", "label"]
        data_df = pd.DataFrame(data, columns=column_names)
        return data_df

    @staticmethod
    def clean_data(data):
        data = utils.Utils.remove_emoji(data)
        return data