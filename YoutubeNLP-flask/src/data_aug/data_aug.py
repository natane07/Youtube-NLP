import pandas as pd
from deep_translator import GoogleTranslator

class Data_aug:

    def __init__(self):
        self.df_data_comments_youtube = pd.read_csv("../../data/comments-youtube-label.csv")
        self.df_data_comments_youtube = self.df_data_comments_youtube[["video_Id", "comment", "label"]]
        self.df_data_comments_youtube_copy = self.df_data_comments_youtube[["video_Id", "comment", "label"]]

    def apply_data_aug(self):
        self.df_data_comments_youtube_copy['comment'] = self.df_data_comments_youtube_copy['comment'].apply(
            lambda x: self.tranlate_text(str(x)) if x is not None else ' '
        )
        print(self.df_data_comments_youtube_copy.head(5))


    def tranlate_text(self, text):
        try:
            translated = GoogleTranslator(source='fr', target='en').translate(text)
            print(translated)
            translated = GoogleTranslator(source='en', target='fr').translate(translated)
            print(translated)
            return translated
        except:
            print("ERROR")
            return text


if __name__ == '__main__':
    data_aug = Data_aug()
    data_aug.apply_data_aug()
    data_aug.df_data_comments_youtube_copy.to_csv("../../data/comments-youtube-label-data-aug.csv")
