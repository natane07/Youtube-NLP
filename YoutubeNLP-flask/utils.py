import os
import googleapiclient.discovery
import csv

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
            videoId=id_video
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
        if os.stat("./comments-youtube.csv").st_size == 0:
            header = ["video_Id", "comment", "label"]
            data.insert(0, header)
        with open('./comments-youtube.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)



