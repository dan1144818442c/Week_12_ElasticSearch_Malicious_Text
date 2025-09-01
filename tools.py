import nltk
import csv
nltk.download('/usr/local/share/nltk_data')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Enricher:

    @staticmethod
    def weapons_detected(weapon_path:str,data:str):
        weapon_list = Loader.load_from_txt_to_list(weapon_path)
        clean_weapon_list = []
        for weapon in weapon_list:
            clean_weapon_list.append(weapon.lower())
        weapons = []
        for word in data.split():
            if word in clean_weapon_list:
                weapons.append(word)

        return weapons

    @staticmethod
    def find_emotion_of_text( text: str):
        score = SentimentIntensityAnalyzer().polarity_scores(text)
        emotion = score['compound']
        if 1 > emotion > 0.5:
            return "positive"
        elif 0.5 > emotion > -0.5:
            return "neutral"
        elif -0.5 > emotion > -1:
            return "negative"
        else:
            return "?"

    @staticmethod
    def add_sentiment_to_dict(dict_):
        emotion = Enricher.find_emotion_of_text(dict_["text"])
        dict_["sentiment"] = emotion
        return dict_


class Loader :

    @staticmethod
    def load_from_txt_to_list(path):
        try:
            with open(path, "r", encoding="utf-8") as weapons:
                # read lines, strip newline, convert to lowercase
                return [line.strip().lower()  for line in weapons]
        except FileNotFoundError:
            print("didn't find this file")
            return []

    @staticmethod
    def load_from_csv_to_list_of_dict(path):
        data_list = []
        with open(path, 'r' , encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_list.append(row)

        return data_list



#
# print(Loader.load_from_txt_to_list(
#     r'C:\Users\1\Desktop\DATA_Analiza\Week_12_ElasticSearch_Malicious_Text\data\weapon_list.txt'))
# print(Loader.load_from_csv_to_list_of_dict(r'C:\Users\1\Desktop\DATA_Analiza\Week_12_ElasticSearch_Malicious_Text\data\tweets_injected 3.csv'))


# print(Loader.load_from_txt_to_list(
#     r'C:\Users\1\Desktop\DATA_Analiza\Week_12_ElasticSearch_Malicious_Text\data\weapon_list.txt'))