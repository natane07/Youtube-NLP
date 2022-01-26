import pandas as pd
import re
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords

class Processing():

    def __init__(self):
        # Lecture du fichier des commentaires
        self.df_data_comments_youtube = pd.read_csv("./data/comments-youtube-label.csv")
        self.df_data_comments_youtube = self.df_data_comments_youtube[["video_Id", "comment", "label"]]
        # Lecture du fichier des commentaire de data augmentation
        self.df_data_aug_comments_youtube = pd.read_csv("./data/comments-youtube-label-data-aug.csv")
        self.df_data_aug_comments_youtube = self.df_data_aug_comments_youtube[["video_Id", "comment", "label"]]

    def apply(self):
        df = self.concat_df_data_with_data_aug()
        df = Processing.clean_data(df)
        df = df.reset_index()
        return df

    def concat_df_data_with_data_aug(self):
        result = pd.concat([self.df_data_comments_youtube, self.df_data_aug_comments_youtube], ignore_index=True, sort=False)
        return result

    @staticmethod
    def clean_data(df, delete_comment_empty=True):
        # Suppression des sauts de ligne et les valeurs http
        df['comment'] = df['comment'].apply(lambda x: re.sub(r'http\S+', '', str(x)))
        df['comment'] = df['comment'].apply(lambda x: str(x).replace('\n', ' ').replace('\r', '').replace("’", ' ').replace("'", ' '))

        # Suppression des "
        df['comment'] = df['comment'].replace('"', '')

        # Suppression des stop word
        def delete_stop_word(all_stopwords, word):
            text_tokens = word_tokenize(word)
            tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
            return (" ").join(tokens_without_sw)

        all_stopwords = stopwords.words('french')
        df['comment'] = df['comment'].apply(lambda x: delete_stop_word(all_stopwords, str(x)))

        # Suppression des commentaires vides
        if delete_comment_empty:
            df['comment'] = df['comment'].replace('', np.nan)
            df.dropna(subset=['comment'], inplace=True)

        return df

if __name__ == '__main__':
    # TEST
    p = Processing()
    df_transform = p.apply()
    df_transform = df_transform.groupby(['label']).max()

    print(df_transform.dtypes)
    print(df_transform.head(10))
    print(df_transform['comment'].values)
    df_transform.to_csv("../../data/test1.csv")