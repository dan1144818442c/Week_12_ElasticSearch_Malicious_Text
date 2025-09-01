from elasticsearch import Elasticsearch

class ElasticSearch_:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")


    def create_indexand(self, index_name, mappings):

        # Make sure index exists (you can create with mapping before this)
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body={
                "mappings":
                   mappings
            })

        print(f" Index  created")


    def index_documents(self, data, index_name):
        # Insert documents one by one
        c = 0
        for dic in data:  # data is your list[dict] from CSV
            res = self.es.index(index=index_name, document=dic)
            print(c)
            c += 1
        print("index doc")

    def get_all_data(self , index_name):
        query_all = {
            "size": 10000,  # Adjust size as needed to retrieve all documents
            "query": {
                "match_all": {}
            }
        }

        response = self.es.search(index=index_name, body=query_all)
        documents = response['hits']['hits']
        return documents


    def update_all_documents_by_func(self, index_name, update_func):
        """
        update_func: function(doc: dict) -> dict
        """
        # קרא את כל המסמכים
        docs = self.es.search(index=index_name, body={"query": {"match_all": {}}}, size=10000)
        for hit in docs['hits']['hits']:
            doc_id = hit['_id']

            source = hit['_source']
            new_doc = update_func(source)  # הפעל את הפונקציה על המסמך
            self.es.update(index=index_name, id=doc_id, body={"doc": new_doc})



    def update(self ,index_name , list_weapond):
        update_query = {
            "script": {
                "lang": "painless",
                "source": """
                    if (ctx._source.weapons_detected == null) {
                        ctx._source.weapons_detected = [];
                    }
                    for (w in params.weapons) {
                        if (ctx._source.text.toLowerCase().contains(w)) {
                            if (!ctx._source.weapons_detected.contains(w)) {
                                ctx._source.weapons_detected.add(w);
                            }
                        }
                    }
                """,
                "params": {"weapons": list_weapond}
            },
            "query": {
                "match_all": {}  # or any filter you want
            }
        }

        res = self.es.update_by_query(index=index_name, body=update_query, refresh=True)
        # print(res)

    def delete_uneccercey(self, index_name):
        field1_name = "Antisemitic"
        field1_value = "0"
        field2_name = "weapons_detected"
        field3_name = "sentiment"
        field3_value = "negative"

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {field1_name: field1_value}}
                    ],
                    "must_not": [
                        {"exists": {"field": field2_name}},  # deletes docs with no weapons_detected
                        {"term": {field3_name: field3_value}}  # deletes docs where sentiment == negative
                    ]
                }
            }
        }

        self.es.delete_by_query(index=index_name, body=query)

#
#
# found = []
#     for weapon in weapons_list:
#         query = {
#             "query": {
#                 "match": {
#                     "text": {
#                         "query": weapon,
#                         "operator": "and"
#                     }
#                 }
#             }
#         }
#         resp = client.search(index=ELASTIC_INDEX, body=query, size=1)
#         if resp["hits"]["total"]["value"] > 0 and weapon.lower() in text.lower():
#             found.append(weapon)
#     return list(set(found))