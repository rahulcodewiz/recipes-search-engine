import requests
import json
import glob
from elasticsearch import Elasticsearch

ES_SERVER='localhost'
ES_PORT=9200
ES_INDEX='recipes_idx'
INDEX_CONFIG='/app/es-setup/recipes_idx_config.json'
DATASET_LOC='/app/dataset/*.json'

#Ensure ES Server is up and running, then launch an ES instance/cluster at localhost url
es = Elasticsearch([{'host': ES_SERVER, 'port': ES_PORT}])

try:
    print("Connect to ES status.",es.info())
except ConnectionError:
    print("Error: unable to connect to ES server")
    quit()

#If index is not present then create it
if not es.indices.exists(index=ES_INDEX):
    with open(INDEX_CONFIG) as put: #is the index configuration file
        data=json.load(put)
        print("Create Index Status:",es.indices.create(index=ES_INDEX,body=data))

else:
    print("Index already exists starting ingestion")

#Prepare data for ingestion by iterating through a list of all json files found in 'data' directory
data_vec = glob.glob(DATASET_LOC)

#Iterate through all json files in collection
docs_indexed = 0
print("****Load begins****")
for doc in data_vec:
    print("**Loading now:",doc)
    with open(doc) as doc_open:
        data = json.load(doc_open)
        for key in data.keys():
            row=data.get(key)
            key=key.replace(".", "")
            res = es.index(index=ES_INDEX,id=key,body=row)
            if res["result"] == 'created':
                docs_indexed += 1
            
#user output
print(f'{docs_indexed} documents successfully indexed in {ES_INDEX} index.')

                


