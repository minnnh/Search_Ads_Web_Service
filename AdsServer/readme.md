# SearchAds

## Process
- install jetty server  
- create HttpServerlet  
	- config web.xml  
- create MYSQL handler
- develop ads workflow
	- QU  
	- Ads selector  
	- Ads filter  
	- Campaign Manage    

## Work-Flow
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

## SQL Database
### AD  
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

### Campaign
- CampaignID
- Budget*

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
### Basic Ads
- [x] Ad
- [x] Utility
	- tokenize ad 
- [X] QueryParse
	- query understanding
- [x] Campaign
- [x] MySQLAccess
	- operations related to SQL
- [x] IndexBuilder
	- store to Memcached
- [x] AdsCampaignManager
- [x] AdsSelector
	- select the ads to process
- [x] AdsFilter
- [x] AdsAllocation
- [x] AdsEngine
- [x] AdsServer
- [x] SearchAds
	- servlet
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

### With Price and Recommendations
- [x] AdPricing
- [x] AdsRanker
- [x] QueryParser
- [x] AdsEngine
- [x] AdsSelector
- [x] CTRModel
- [x] IndexBuilder
- [x] Utility


### pre-process
- sql (searchAds.init(), adsEngine.init(), indexBuilder.buildInvertIndex(ad))
- memcached (searchAds.init(), adsEngine.init(), indexBuilder.buildForwardIndex)
- synonyms memcached (generate_synonym.py)





