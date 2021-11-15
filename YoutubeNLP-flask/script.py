import utils
class script():

    @staticmethod
    def get_comments(ids_videos):
        for id in ids_videos:
            response = utils.Utils.call_api_youtube_comments(id)
            data = utils.Utils.parse_request_youtube(response)
            utils.Utils.whrite_csv(data)



