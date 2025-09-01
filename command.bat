  docker run -d --name es -p 9200:9200   -e "discovery.type=single-node"   -e "xpack.security.enabled=false"   -e "ES_JAVA_OPTS=-Xms1g -Xmx1g"   docker.elastic.co/elasticsearch/elasticsearch:8.15.0


  GET /tweet_index/_search
{
  "query": {
    "bool": {
      "must_not": [
        {"term": {"Antisemitic": "1"}},
        {"exists": {"field": "weapons_detected"}}
      ],
      "should": [
        {"term": {"sentiment": "neutral"}},
        {"term": {"sentiment": "positive"}}
      ],
      "minimum_should_match": 1
    }
  }
}


