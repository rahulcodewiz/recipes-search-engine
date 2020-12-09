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
- output(term_vec)  Writes preprocessed data to file
"""

#until I get NLP packages to work, will have to do some basic preprocessing taks with python 
def preprocessor():
    """ preprocessor() -> list of documents as dictionaries [{ID:"word_i, word_i+1, ..."} , {ID:"word_i word_i+1"}, ...}] """
    DATASET_LOC = '/Users/jon/recipes-search-engine/dataset/*.json'
    STOPWORDS_LOC = '/Users/jon/recipes-search-engine/batch/nltk_stopwords.txt'
    data_vec = glob.glob(DATASET_LOC)
    alpha = {}
    for char in string.ascii_lowercase:
        alpha[char] =''
    stopwords = {}
    with open(STOPWORDS_LOC) as f:
        for line,item in enumerate(f):
            stopwords[item.strip()] =''
    document_vector = {}
    debug_count = 0

    #Load up data, extract ID,Title,Ingredients, As a crude substitute for stemming/lemmatization just doing stopword removal and non-alpha removal
    for doc in data_vec:
        with open(doc) as doc_open:
            data = json.load(doc_open)
            for key in data.keys():
                body=data.get(key)
                if type(body.get('ingredients')) == list:
                    temp = " ".join(body.get('ingredients')).lower()
                elif type(body.get('ingredients')) == str:
                    temp = body.get('ingredients').lower()
                else:
                    temp = ''
                document = str(body.get('title')).lower() + temp
                temp = []        
                debug_count += 1
                for element in document:
                    if (element == ' ') or (element in alpha):
                        temp.append(element)
                document = ''.join(temp)
                document = document.replace("   ", " ")
                document = document.replace("  ", " ")
                word_list = list(document.split(' '))
                temp = []
                for word in word_list:
                    if word not in stopwords:
                        temp.append(word)       
                document_vector[key] = temp 
    
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


def output(doc_vector):
    WRITE_LOC = '/Users/jon/recipes-search-engine/dataset/associated/weighted_doc_term_vecs.json'
    ## Save our changes to JSON file
    with open(WRITE_LOC, "w+") as updated:
        json.dump(doc_vector, updated)

def main(): 
    #Set Parameters
    BETA = 1
    KAPPA = 3

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

    #Write weighted doc_term vectors to dataset/associated
    print("Writing doc vectors to dataset/associated")
    output(doc_vector)
    print("Program complete")


if __name__ == "__main__":
    main()