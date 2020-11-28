from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask import Flask, render_template
from json2html import *
import requests
import json
import os
from elasticsearch import Elasticsearch

INDEX_NAME="recipes_idx"
#es = Elasticsearch(['localhost','0.0.0.0'], port=9200)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
def searchEs(term):
   esQuery = json.dumps({
        "query": {
            "match": {
                "title": term
            }
        }
    })
   print("Search Query:",esQuery)
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
    suggestRes= es.search(index=INDEX_NAME, body=esQuery)
    print(suggestRes)
    return suggestRes