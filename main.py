from elastic_serch import ElasticSearch_
from  tools import  *


if __name__ == '__main__':
    mapping = { "properties": {
                            "TweetID": {"type": "keyword"},
                            "CreateDate": {"type": "text"},
                            "Antisemitic": {"type": "keyword"},
                            "text": {"type": "text",
                                     "fields": {
                                         "exact": {"type": "keyword"}}},
                            "sentiment": {"type": "keyword"},
                            "weapons_detected": {"type": "keyword"}
                        }}


    a = ElasticSearch_()
    # print(a.es)
    a.es.indices.delete(index="tweet_index")
    a.create_indexand("tweet_index" , mappings=mapping )
    data = Loader.load_from_csv_to_list_of_dict(r'C:\Users\1\Desktop\DATA_Analiza\Week_12_ElasticSearch_Malicious_Text\data\tweets_injected 3.csv')
    a.index_documents(data=data , index_name='tweet_index')
    # print(a.get_all_data(index_name="tweet_index"))
    a.update_all_documents_by_func("tweet_index" , update_func=Enricher.add_sentiment_to_dict)
    a.update('tweet_index' ,Loader.load_from_txt_to_list(r"C:\Users\1\Desktop\DATA_Analiza\Week_12_ElasticSearch_Malicious_Text\data\weapon_list.txt") )
    a.delete_uneccercey("tweet_index")