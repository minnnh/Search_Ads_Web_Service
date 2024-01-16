# Python Modleing

## Getting Started
### Data Prepare
- Prepare for ads
	+ dedupe_ads.py
	+ generate_budeget.py
- Click Log 	
	+ generate_user.py
 	+ generate_click_log.py
	+ generate_name_click_log.py
### Spark
1. store synonym to memcached (enable_query_rewrite)
	- generate_word2vec_training_data.py (enable_pClick)
	- word2vec.py
	- generate_synonym.py 
2. store tfidf to memcached (enable_TFIDF)
	- document_frequency.py 
	- term_frequency.py
	- store_tf_idf.py
3. store features to memcached (enable_pclick)
	- generate_query_ad.py
	- select_feature.py
	- store_ctr_feature.py
	- prepare_ctr_training_data.py
	- ctr_gbdt.py
	- ctr_logistic.py

## Pre-Process for SearchAds
1. store synonym to memcached (11219)
	- ```python generate_synonym.py```
2. store tfidf to memcached (tf 11220, df 11221)
	- ```spark-submit store_tf_idf.py```
3. store features to memcached (11218)
	- ```python store_ctr_feature.py```



## Memcached
- mMemcachedPortal: 11212
	+ crwaled data 
	+ key, exp, adidlist
- synonymsMemcachedPortal: 11219
	+ store synonyms e.g: word: synonyms
- featureMemcachedPortal: 11218
	+ pClick data caculated by spark
- dfMemcachedPortal: 11221
	+ document frequency
- tfMemcachedPortal: 11220
	+ document tfMemcachedPortal



## Todo List
- [x] Query understanding with word2vector (enable_query_rewrite)
	- [x] generate_word2vec_training_data.py (enable_pClick)
	- [x] word2vec.py
	- [x] generate_synonym.py 
- [x] store tfidf to memcached (enable_TFIDF)
	- [x] document_frequency.py 
	- [x] term_frequency.py
	- [x] store_tf_idf.py
- [x] Predict click probabbility (enable_pclick)
	- [x] generate_query_ad.py
	- [x] select_feature.py
	- [x] store_ctr_feature.py
	- [x] prepare_ctr_training_data.py
	- [x] ctr_gbdt.py
	- [x] ctr_logistic.py








