import os
import googleapiclient.discovery
import csv
import re

class Utils():

    @staticmethod
    def call_api_youtube_comments(id_video):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = ""

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="snippet",
            moderationStatus="published",
            order="time",
            textFormat="plainText",
            videoId=id_video,
            maxResults=65
        )
        response = request.execute()

        return response


    @staticmethod
    def parse_request_youtube(response):
        data = list()
        for items in response['items']:
            row = list()
            video_id = items["snippet"]["topLevelComment"]["snippet"]["videoId"]
            comment = items["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            row.append(video_id)
            row.append(comment)
            row.append("")
            data.append(row)
        return data


    @staticmethod
    def whrite_csv(data):
        if os.stat("./data/comments-youtube.csv").st_size == 0:
            header = ["video_Id", "comment", "label"]
            data.insert(0, header)
        with open('./data/comments-youtube.csv', 'a+', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(data)

    @staticmethod
    def remove_emoji(data):
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
        "]+", re.UNICODE)
        return re.sub(emoj, " ", data)




