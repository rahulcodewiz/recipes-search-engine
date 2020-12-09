from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask import Flask, render_template
from json2html import *
import requests
import json
import os
from elasticsearch import Elasticsearch

default_query_terms = ['meat']

INDEX_NAME="recipes_idx"
#es = Elasticsearch(['localhost','0.0.0.0'], port=9200)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
def searchEs(query):

    queryStr = str(query,'utf-8')  
    formatQuery(queryStr) 
    esQuery = json.dumps({
            "query": {
                "match": {
                    "title": queryStr
                }
            },
                "highlight" : {
                        "pre_tags" : ["<mark>"],
    "post_tags" : ["</mark>"],
        "fields" : {
            "title" : {}
        }
            }
        })
    print("Search Query:",esQuery)
    res = es.search(index=INDEX_NAME, body=esQuery)
    print("Search result:",res)
    return res
    #return json2html.convert(json = res)

def userProfileParser(user_idx):
   
    #Ex profile: in /app/user-profile/user1.json
    up_json_file = str("user"+str(user_idx)+".json")
    profile_ = os.path.join("/app/search-engine-webapp/user-profile", up_json_file)

    with open(profile_) as f:
        data = json.load(f)
        #print("user data", data)
    
    if data['food']['interest']:
        t_ = data['food']['interest']
        terms = t_.split()
    else:
        return None
    return terms

def recommenderSystem(user_idx):
    terms = userProfileParser(user_idx)
    if not terms:
        terms = default_query_terms

    #Extract username from profile
    with open(profile_) as f:
        data = json.load(f)
        user_name = data['name']

    res = []
    for term in terms:
        esQuery = json.dumps({
            "query": {
                "match": {
                    "title": term
                }
            }
        })
    print(f"{user_name}, since you like {data}, here are some recommended recipes:" , esQuery)
    res = es.search(index=INDEX_NAME, body=esQuery)
    return json2html.convert(json = res)

def autosuggestTerm(query):
    esquery = json.dumps({
                "suggest": {
                    "text": query,
                    "recipes": {
                        "term": {
                            "field": "title"
                            }
                    }
                }
            })
    print("Search Query:",esquery)
    suggestRes= es.search(index=INDEX_NAME, body=esquery)
    print(suggestRes)
    return suggestRes

def autosuggestPhrase(query):
    esQuery=json.dumps({
    "suggest": {
        "text": query,
        "recipes": {
        "phrase": {
            "field": "title.trigram",
            "size": 4,
            "gram_size": 3,
            "direct_generator": [ {
            "field": "title.trigram",
            "suggest_mode": "always"
            } ],
            "highlight": {
            "pre_tag": "<em>",
            "post_tag": "</em>"
            }
        }
        }
        }
        })
    print("Search Query:",esQuery)
    suggestRes= es.search(index=INDEX_NAME, body=esQuery)
    print(suggestRes)
    return suggestRes

def formatQuery(searchquery):
    import json
    import pprint
    from collections import defaultdict
    nested_dict = lambda: defaultdict(nested_dict)
    query=nested_dict()
    query['span_near']['clauses']=list()
    query['slop']='1'
    query['in_order']="true"
    words=searchquery.split()
    for w in words:
        nest = nested_dict()
        nest["span_multi"]["match"]["fuzzy"]["msg"]["fuzziness"]["value"]=w
        nest["span_multi"]["match"]["fuzzy"]["msg"]["fuzziness"]["fuzziness"]="1"
        json.dumps(nest)
        query['span_near']['clauses'].append(json.loads(json.dumps(nest)))


    pprint.pprint(json.loads(json.dumps(query)))
