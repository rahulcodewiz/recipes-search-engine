import requests
import json
import glob
from elasticsearch import Elasticsearch

url = 'http://localhost:9200/'

#Ensure ES Server is up and running, then launch an ES instance/cluster at localhost url
r = requests.get(url)
if r.status_code == 200:
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
else:
    print("Error: unable to connect to ES server")
    quit()

#ensure es cluster is up and running first with es.ping(), then create new index 'recipes' if it doesn't already exist
if es.ping():
    with open('/es-setup/index-put.json') as put: #'index-put.json' is the index configuration file
        if not es.indices.exists(index="recipes"):
            es.create(index='recipes',body=put) 

#Prepare data for ingestion by iterating through a list of all json files found in 'data' directory
data_vec = glob.glob('/data/*.json')

#Iterate through all json files in collection
docs_indexed = 0
for doc in data_vec:
    data = json.load(doc)
    for key in data.keys():
        row=data.get(key)
        key=key.replace(".", "")
        res = es.index(index='recipes',id=key,body=row)
        if res["result"] == 'created':
            docs_indexed += 1
            
#user output
print(f'{docs_indexed} documents successfully indexed in \'recipes\' index.')

                


