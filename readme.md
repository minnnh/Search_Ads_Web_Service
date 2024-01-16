# Search Ads Web Service
The Search Ads Web Service project is a Java-based web application with a robust web crawler for gathering product data from Amazon. It enhances online shopping through advanced search capabilities, including query understanding and ads optimization based on user behavior. The goal is to provide users with a straightforward and personalized shopping experience.
## Demo
Environment
- Java 8
- Maven 3
- Jetty 9
- Python 3.11
- Spark 3.5

## Builte With
__Crawler__ : Java, Maven, SQL, JSoup, Proxy
__Modeling__: Python, SparkMLlib, Linear Regression, Logistic Regression, Decision Tree, Neural Network, Word2Vector, TF-IDF
__Ads Server__: Java, Jetty
__Data__: MySQL, Memcached

## How it works
### Crawler
- Parse HTML Page asynchronously
1. start with feeds file
2. a list of website url
3. request url with different parameter
4. sample feeds file
- Process
    - http request
    - response
    - store response
    - extract data from HTML

### Modeling
- Query Understanding
    - Lucean to clean the text
    - word2vec to find K nearest neighbors of original query, semantically similar queries
- Ads Relevancy
    - logistic regression classifier is used to determine the goodness of each subquery
    - use TF-IDF algorithm as the relevance score
    - Relevance Score = measure how relevant query is to key words in ads =>  number of word match query / total number of words in key words
- P-Click Prediction
    - pClick = The “clickability” which can be defined as the probability of click or estimated Click Through Rate (CTR)
    - Positive feature
       + IP
       + device_id
       + AdId
       + QueryCategry_AdsCategory match
       + Query_CampaignId match
       + Query_AdId match
    - Negative feature
        - mismatched query_category ads_category
        - mismatched Query_CampaignId
        - mismatched Query_AdId
        - lowest campaignId weight, lowest adId weight per query group
    - Step 1: Segment users
    - Step 2: assign campaign ID, Ad Id, Click(0/1),Ad category_Query category(0/1) to user
- Online Ads Ranking and Pricing
    - Rank score = quality Score * bid
    - Quality Score = 0.75 * pClick+ 0.25 * relevance Score
    - Cost per click (CPC)
        = (next quality score/current quality score) * next bid price + 0.01
        = next rank score / current quality score + 0.01

### Ads Server
- SearchAd.doGet 
- adsEngine.selectAds

- if enable_query_rewrite
	- QueryParser.getInstance()
		- do OfflineQueryRewrite (if have the same tokens list in memcachedServer):
			+ query-> rewrite query stored in synonymsMemcached 
		- else, do OnlineQueryRewrite:
			+ query-> rewrite query stored in synonymsMemcached 
	- AdsSelector.selectAds
		- select from memcached, and find the corresponding ad from sql
		- relevanceScore
		- if enableTFIDF
			+ AdsSelector.getRelevanceScoreByTFIDF (tfMemcached and dfMemcached)
		- if enable_pClick
			+ AdsSelector.predictCTR (featureMemcachedPortal)
			+ CTRModel.predictCTRWithLogisticRegression
- else
	- AdsSelector.selectAds (the same as above)

- AdsRanker
- AdsFilter
- AdsCampaignManager
- AdPricing.setCostPerClick (pricing： next rank score/current score * current bid price)
- AdsAllocation.AllocateAds

### Data
- MySQL
    + ad
        - AdID
        - CampaignId
        - Keywords
        - Bid
        - price
        - thumbnail
        - Description
        - Brand
        - detail_url
        - Category
        - Title
    + campaign
        - CampaignID
        - Budget*
- Memcached
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

## Getting Started
1. Clone the repo
```sh
git clone https://github.com/minnnh/Search_Ads_Web_Service
```
2. Crawl Ads
```sh
mvn clean install
```
```sh
./crawler_launch.sh
```
3. Pre-Process for SearchAds
    - Store synonym to memcached (11219)
    ```sh
    python generate_synonym.py
    ```
    - Store TFIDF to memcached (tf 11220, df 11221)
	```sh
    spark-submit store_tf_idf.py
    ```
    - Store features to memcached (11218)
	```sh
    python store_ctr_feature.py
    ```
4. Run the Ads Server with Jetty
## Todo List
### Coding
- [x] [Crawler](./WebCrawler)
    - [x] Ad
    - [x] Utility
    - [x] AmazonCrawler
    - [x] CrawlerMain
    - [x] test
- [x] [Python](./Python)
    - [x] prepare data
    - [x] synonym
    - [x] tfidf
    - [x] ctr    
- [x] [SearchAds]()
    - without modeling
        - [x] Ad
        - [x] Utility
        - [X] QueryParse
        - [x] Campaign
        - [x] MySQLAccess
        - [x] IndexBuilder
        - [x] AdsCampaignManager
        - [x] AdsSelector
        - [x] AdsFilter
        - [x] AdsAllocation
        - [x] AdsEngine
        - [x] AdsServer
        - [x] SearchAds
            - servlet
    - with modeling
        - [x] AdPricing
        - [x] AdsRanker
        - [x] QueryParser
        - [x] AdsEngine
        - [x] AdsSelector
        - [x] CTRModel
        - [x] IndexBuilder
        - [x] Utility

### Data Process
- [x] ads -> sql
- [x] ads -> memcached
- [x] synonyms memcached
	- [x] prepare data
	- [x] java coding
- [x] tfdf memcached
	- [x] prepare data
	- [x] java coding   
- [x] pclick memcached 
	- [x] prepare data
	- [x] java coding 