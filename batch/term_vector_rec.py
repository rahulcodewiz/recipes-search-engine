import math
import json
import glob
import string
import os
#having trouble with python packages not working, (nltk, numpy, metapy, pandas). Suspect Big Sur compatibility issues. Could also be a file path issue
"""term_vector_rec.py

Module Overview
- Static Inputs: (recipes Corpus, list of user-relevant doc IDs)
- Output: (top k-rated document IDs)

Workflow
- preprocessor()    Load data (JSON), extract ID, title and ingredients fields
                    Concatenate and preprocess title and ingredients string (tokenize,stopword removal,stemming)
                    dict <- {ID: preprocessed title+ingredients string}
- vocabulary(list)  Extract Corpus vocabulary from list as dictionary {word: num_docs_occurred}
                    tuple <- (avg_doc_len, {corpus vocabulary})
- BM25(doc_word_vec, doc_freq_vec, m, avg_dl, beta, kappa)
                    documents fed into BM25 to update word vectors with  BM25 weighting 
- recommender(seen,unseen, k)
                    seen is the list of documents that describe a user
                    unseen are all other documents in the Corpus
                    sorted list(IDs) <- the k top-rated unseen documents to recommend based on cosine similarity to seen documents
"""

#until I get NLP packages to work, will have to do some basic preprocessing taks with python 
def preprocessor():
    """ preprocessor() -> list of documents as dictionaries [{ID:"word_i, word_i+1, ..."} , {ID:"word_i word_i+1"}, ...}] """
    DATASET_LOC = '/Users/jon/recipes-search-engine/dataset/*.json'
    STOPWORDS_LOC = '/Users/jon/recipes-search-engine/batch/nltk_stopwords.txt'
    data_vec = glob.glob(DATASET_LOC)
    alpha = set()
    for char in string.ascii_lowercase:
        alpha.add(char)

    stopwords = set()
    with open(STOPWORDS_LOC) as f:
        for line,item in enumerate(f):
            stopwords.add(item.strip())
    
    document_vector = {}

    #Load up data, extract ID,Title,Ingredients, As a crude substitute for stemming/lemmatization just doing stopword removal and non-alpha removal
    for doc in data_vec:
        with open(doc) as doc_open:
            data = json.load(doc_open)
            for key in data.keys():
                body=data.get(key)
                key=key.replace(".", "")        #fix '.' in recipe IDs
                document = str(body.get('title')).lower() + str(body.get('ingredients')).lower()
                word_list = []
                for char in document:
                    if char not in alpha:
                        document.replace(char,'')
                word_list = document.split()
                for word in word_list:
                    if word not in stopwords:
                        word_list.remove(word)          
                document_vector[key] = word_list 
    
    return document_vector


def vocublary(vec_docs):
    """ vocabulary(vec_docs) -> tuple: (int avg_doc_len, updated vec_docs, corpus Vocabulary dictionary {"word": num_docs_have__this_term, ...})
    vec_docs = list of documents as dictionaries [{ID:"word_i word_i+1 ..."} , {ID:"word_i word_i+1"}, ...}] 
    """

    vocabulary = {}
    count_vec = []  #used for aggregating doc lengths in a list to determining avg_doc_len

    #Extract len of docs anonymously, convert vec_docs values to c(w,d), Create corups Vocabulary as c(d,w)
    for key,value in vec_docs.items():  #recall: {key = "doc_ID": value = [list, of, words, in, each, document]}
        doc_words = {}  
        count_vec.append(len(value)) 
        for word in value:
            #convert doc word list into dict storing c(w,d) ∈ D
            if word in doc_words:
                doc_words[word] = doc_words[word] + 1
            else:
                doc_words[word] = 1
        #Next, create vocubulary c(d,w) ∈ Corpus
        for word,count in doc_words.items():
            if word in vocabulary:
                vocabulary[word] = vocabulary[word] + 1
            else:
                vocabulary[word] = 1
        #last convert {ID:[list,of,words]} -> {ID: {dict:1,of:1,word:1,counts:2} }
        vec_docs[key] = doc_words

    avg_dl = sum(count_vec) / len(count_vec)
    return (avg_dl,vocabulary)


#see page 108, textbook. This variant scores word counts using BM25 model
def BM25(doc_vec, vocabulary, m, avg_dl, beta, kappa):
    """ BM25(dict:doc_vec, dict:vocabulary, int:m, float:avg_dl, float:beta, float:kappa)
    doc_vec = {ID: {'dog':3,'antelope':1,...}, {ID:{c(w,d)},...}
    vocabulary = {'dog':17,'cat':20,'antelope':4,...} num documents in which a word occurs
    m = num of documents in corpus
    avg_dl = average document length in words
    beta = [0,1] parameter controls degree of doc length normalization, the higher the more normalization
    kappa = [0, +infinity] parameter k controls the upper bound on TF-IDF from bit vector up to linear transform
    """

    for key,value in doc_vec.items():
        dl = 0
        for w,c in value.items():   #   dl = word count for doc 
            dl += value[w]
        for w,c in value.items():
            df_weight = math.log((m+1)/vocabulary[w])  #log((M+1)/df(w))
            numerator = (kappa + 1) * value[w]    #(k+1)c(w,d)
            denominator = value[w] + kappa*(1 - beta + beta*(dl/avg_dl)) #c(w,d)+k(1-b+b(|d|/avdl))
            value[w] = (numerator/denominator) * df_weight #replace c(w,d) with BM25 weighted score


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
    #set parameters Beta and Kappa for BM25, and top-K number of recommendations to return
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

    seen_id_vec = [a,b,c,d,e,f,g,h,i,j]
    seen_docs = {}
    unseen_docs = {}
    BETA = 1
    KAPPA = 3
    top_k = 5

    #Data Ingestion and preprocessing
    print("Start preprocessing...")
    doc_vector = preprocessor()
    print("Preprocessing complete.\n")

    #Corpus Vocabulary Init and summary statistics 
    NUM_DOCS_CORPUS = len(doc_vector)
    print("Building vocabulary...")
    vocab_tuple = vocublary(doc_vector)
    AVG_DOC_LEN = vocab_tuple[0]
    corpus_vocab = vocab_tuple[1]
    print("Corpus vocabulary built.\n")

    #BM25 updates the c(w,d) field with BM25 weighted score for each document
    print("Updating document vectors with BM25 weights")
    BM25(doc_vector,corpus_vocab,NUM_DOCS_CORPUS,AVG_DOC_LEN,BETA,KAPPA)
    print("BM25 weighting complete.\n")

    #Split document Corpus into seen and unseen document collections
    for id in seen_id_vec:
        seen_docs[id] = (doc_vector.pop(id,None))
    unseen_docs = doc_vector
    
    #Compares document similarity to user-preferences to create list of recommendations
    print("Finding Relevant Documents...\n")
    recommendations = recommender(seen_docs,unseen_docs,top_k)
    
    #display the top-k ranked recipe recommendations (as IDs)
    print('User Recommendations with scores:\n')
    for i in range(top_k):
        print(recommendations[i])


if __name__ == "__main__":
    main()