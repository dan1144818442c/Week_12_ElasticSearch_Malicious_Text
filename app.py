from fastapi import FastAPI ,Request
import uvicorn
from elastic_serch import *
from contextlib import asynccontextmanager
from elastic_serch import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    import main
    yield


app = FastAPI(
    lifespan=lifespan
)
es = ElasticSearch_().es

@app.get("/data/antisemitic_with_weapons")
async def antisemitic_with_weapons():
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"Antisemitic": "1"}},
                    {"exists": {"field": "weapons_detected"}}
                ]
            }
        }
    }
    res = es.search(index='tweet_index', body=query, size=10000)
    hits = res['hits']['hits']
    if hits:
        return [hit['_source'] for hit in hits]
    else:
        return {"message": "No antisemitic documents with weapons found."}



@app.get("/data/min_2_weapons")
async def min_2_weapons():
    query = {
        "query": {
            "script": {
                "script": {
                    "source": "doc['weapons_detected'].size() >= 2"
                }
            }
        }
    }
    res = es.search( index='tweet_index',body=query, size=10000)
    hits = res['hits']['hits']
    if hits:
        return [hit['_source'] for hit in hits]
    else:
        return {"message": "No documents found with 2 or more weapons."}

if __name__ == "__main__":

    uvicorn.run(app, host="localhost", port=8000)
