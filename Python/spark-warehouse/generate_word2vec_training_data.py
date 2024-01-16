import os
import sys
import json
import random
import re
# from sets import Set

DIR = "../../data/"
# DIR2 = "../../data2/"

if __name__ == "__main__":

    # input_file = DIR + "/deduped/cleaned_ads.txt"
    # word2vec_training_file = "word2vec_training_cleaned.txt"

    input_file = DIR + "/deduped/cleaned_ads.txt"
    word2vec_training_file = DIR + "word2vec_training_cleaned.txt"
    # word2vec_training_file = DIR2 + "word2vec_training_cleaned.txt"
    # word2vec_training_file = "test.txt"

    word2vec_training = open(word2vec_training_file, "w")

    with open(input_file, "r") as lines:
        for line in lines:
            entry = json.loads(line.strip())
            if  "title" in entry and "adId" in entry and "query" in entry:
                    title = entry["title"].lower().encode('utf-8')
                    query = entry["query"].lower().encode('utf-8')

                    #remove number from text
                    new_query_tokens = []
                    query_tokens = query.decode().split(" ")
                    for q in query_tokens:
                        if q.isdigit() == False and len(q) > 1:
                            new_query_tokens.append(q)

                    new_title_tokens = []
                    title_tokens = title.decode().split(" ")
                    for t in title_tokens:
                        if t.isdigit() == False and len(t) > 1:
                            new_title_tokens.append(t)
                    query = " ".join(new_query_tokens)
                    title = " ".join(new_title_tokens)
                    word2vec_training.write(query)
                    word2vec_training.write(" ")
                    word2vec_training.write(title)
                    word2vec_training.write('\n')

    word2vec_training.close()