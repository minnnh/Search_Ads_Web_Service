#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import libmc
from libmc import (
    MC_HASH_MD5, MC_POLL_TIMEOUT, MC_CONNECT_TIMEOUT, MC_RETRY_TIMEOUT
)

mc = libmc.Client(
    ["127.0.0.1:11219"], comp_threshold=0, noreply=False, prefix=None, hash_fn=MC_HASH_MD5, failover=False
    # ["127.0.0.1:11218"], comp_threshold=0, noreply=False, prefix=None, hash_fn=MC_HASH_MD5, failover=False
)
mc.config(MC_POLL_TIMEOUT, 100)  # 100 ms
mc.config(MC_CONNECT_TIMEOUT, 300)  # 300 ms
mc.config(MC_RETRY_TIMEOUT, 5)  # 5 s

def query_rewriter_helper(query_terms, synonyms_dict):
    if len(query_terms) == 0:
        return []

    if len(query_terms) == 1:
        if query_terms[0] not in synonyms_dict:
            return [query_terms[0]]
        else:
            return list(synonyms_dict[query_terms[0]])

    prev = query_rewriter_helper(query_terms[:-1], synonyms_dict)
    if query_terms[-1] in synonyms_dict:
        post = synonyms_dict[query_terms[-1]]
        return [s + '_' + c for s in prev for c in post]
    else:
        return [s + '_' + query_terms[-1] for s in prev]

if __name__ == "__main__":
    DIR = "../../data/"
    synonyms_input_file = "word2vec_training.txt"
    ads_input_file = DIR + "/deduped/cleaned_ads.txt"

    synonyms_dict = {}
    query_set = set()

    with open(synonyms_input_file, "r") as lines:
        for line in lines:
            entry = json.loads(line.strip())
            if "word" in entry and "synonyms" in entry:
                synonyms_dict[entry["word"]] = entry["synonyms"]
                synonyms_dict[entry["word"]].append(entry["word"])

    with open(ads_input_file, "r") as lines:
        for line in lines:
            entry = json.loads(line.strip())
            if "query" in entry:
                if entry["query"] not in query_set:
                    query_set.add(entry["query"])

    for query in query_set:
        print("query:", query)
        query_terms = query.lower().split(" ")
        query_key = "_".join(query_terms)
        rewrite_query_list = query_rewriter_helper(query_terms, synonyms_dict)
        
        unique_synonyms = set()
        final_synonyms = []
        for rewrite_query in rewrite_query_list:
            if rewrite_query not in unique_synonyms:
                unique_synonyms.add(rewrite_query)
                final_synonyms.append(rewrite_query)
        try:
            # mc.set(query_key, json.dumps({"synonyms": final_synonyms}).encode('utf-8'))
            mc.set(query_key, json.dumps(final_synonyms).encode('utf-8'))
            # mc.set(query_key, final_synonyms)
            # print("store: " + query_key + "{ " + ", ".join(final_synonyms) + "}")
            print("store: " + query_key)
        except:
            print("something wrong here")
        


        
