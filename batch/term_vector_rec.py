import math
import json
import glob
import string
import os
import pprint
#having trouble with python packages not working, (nltk, numpy, metapy, pandas). Suspect Big Sur compatibility issues. Could also be a file path issue
"""term_vector_rec.py

Module Overview
- Static Inputs: (recipes Corpus, list of user-relevant doc IDs)
- Output: (top k-rated document IDs)

Workflow
- cosine()

- recommender(seen,unseen, k)
                    seen is the list of documents that describe a user
                    unseen are all other documents in the Corpus
                    sorted list(IDs) <- the k top-rated unseen documents to recommend based on cosine similarity to seen documents
"""

def cosine(seen_doc, unseen_doc):
    """ cosine(weighted_a, weighted_b) -> float value of cosine similarity of two input vectors
    seen_doc = dictionary that is a BM25-weighted document term vector
    unseen_doc = dictionary that is a BM25-weighted document term vector
    """
    similarity = 0
    for w,score in seen_doc.items():
        if w in unseen_doc:
            similarity += score * unseen_doc[w]
    return similarity


def recommender(seen, unseen, k):
    """ recommender(seen,unseen) -> list of top-k scores stored as [{ID: score},{ID:score},...]
    seen = dict of documents that describe a user's preferences
    unseen = dict of all other documents in the Corpus
    k = number of recommendations
    """
    top_scores = []
    recommendations = []
    for i in range(k):
        top_scores.append(-1)
        recommendations.append({"ID":0})
   
    for seen_key,seen_doc in seen.items():
        for unseen_key,unseen_doc in unseen.items():
            score = cosine(seen_doc,unseen_doc)
            i = -1
            while (score > top_scores[i]) and (abs(i) <= k):
                if abs(i) == k:
                    top_scores[i] = score
                    recommendations[i] = {unseen_key:score}
                    break
                elif top_scores[i-1] > score:
                    top_scores[i] = score
                    recommendations[i] = {unseen_key:score}
                    break
                else:
                    i = i - 1

    return recommendations


def main():
    #TODO(Jon) Figure out how to Pass seen_id_vec dynamically or else hardcode for each recommendation run
    #These are ten relevant documents I retreived from ES queries
    a = "XetGJ5Ol0bwPahBTuG3gWCTPWU0CDQ"
    b = "YAQgjmB48uiqScqstzl/hjVtNAB9pPy"
    c = "NtnYhnSlP9xOxjI6WPFI7Lv1wBYOCEq"
    d = "yI2gS/CB4Usl4uVsuNMUHisdvJ6lXWW"
    e = "a/iQ5J27pdS4Jw7Di4LiiyIV6wjAWom"
    f = "4JRqlB8HTpsynhLQ9mGKeczw5O18pC"
    g = "vkvvqPI7anmpsckOS3rJfHAHSh7rte"
    h = "ivbCqdV1TE31XZCewCZqi4JM3lDa3EK"
    i = "nO98G0dYo2PTel/EVeNmbl1cmJ0OlzK"
    j = "LxJMWb4fbPJ4FDeKX0hc6LEy0L8BK8e"

    #set parameters Beta and Kappa for BM25, and top-K number of recommendations to return  
    seen_id_vec = [a,b,c,d,e,f,g,h,i,j]
    seen_docs = {}
    unseen_docs = {}
    top_k = 5

    #TODO(Jon) Load up the json file
    FILE_PATH = '/Users/jon/recipes-search-engine/dataset/associated/weighted_doc_term_vecs.json'
    with open(FILE_PATH, 'r') as doc_open:
        doc_vector = json.load(doc_open)

    #Split document Corpus into seen and unseen document collections
    for id in seen_id_vec:
        seen_docs[id] = (doc_vector.pop(id,None))
    unseen_docs = doc_vector

    #Compares document similarity to user-preferences to create list of recommendations
    print("Finding Relevant Documents...\n")
    recommendations = recommender(seen_docs,unseen_docs,top_k)
    
    #display the top-k ranked recipe recommendations (as IDs)
    print('User Recommendations IDs with scores:\n')
    for item in recommendations:
        print(item)

    #convert list to dict
    rec_dict = {}
    for item in recommendations:
        rec_dict.update(item)

    #TODO(Jon) Solve known issue with file format of data
    #load up the data to find recipes

    inputs = {}
    outputs = {}
    DATASET_LOC_A = '/Users/jon/recipes-search-engine/dataset/recipes_raw_nosource_ar.json'
    DATASET_LOC_B = '/Users/jon/recipes-search-engine/dataset/recipes_raw_nosource_epi.json'
    with open(DATASET_LOC_A) as file_a:
        with open(DATASET_LOC_B) as file_b:
            data_a = json.load(file_a)
            data_a = json.load(file_b)
            for item in seen_id_vec:
                if item in data_a:
                    inputs[item] = data_a[item]
                elif item in data_b:
                    inputs[item] = data_b[item]
            for key,value in rec_dict.items():
                if key in data_a:
                    outputs[key] = data_a[key]
                elif key in data_b:
                    outputs[key] = data_b[key]

    pp = pprint.PrettyPrinter(indent=4)
    print('----------------- liked RECIPES --------------------')
    pp.pprint(inputs)
    print('\n----------------- Recommended RECIPES --------------------\n')
    pp.pprint(outputs)


if __name__ == "__main__":
    main()