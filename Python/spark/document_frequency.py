import sys
import json
from pyspark import SparkContext

def get_term(line):
    entry = line.split('_')
    return entry[1]

def get_adid_terms(line):
    entry = json.loads(line.strip())
    ad_id = entry['adId']
    # ad_id = entry[4]
    adid_terms = []
    print (entry['keyWords'])
    for term in entry['keyWords']:
    # for term in entry[3]:
        val = str(ad_id) + "_" + term
        adid_terms.append(val)
    return adid_terms

def generate_json(items):
    result = {}
    result['doc_freq'] = items[0]
    result['count'] = items[1]
    return json.dumps(result)

if __name__ == "__main__":
    # adid_keys count
    # adfile = sys.argv[1] #raw search log
    DIR = "../../data/"
    # DIR2 = "../../data2/"
    adfile =  DIR + "deduped/cleaned_ads.txt"
    # adfile = DIR2 + "log/simulated_click_log.txt"
    sc = SparkContext(appName="DF_Features")
    data = sc.textFile(adfile).flatMap(lambda line: get_adid_terms(line)).distinct().map(lambda w: (get_term(w),1)).reduceByKey(lambda v1,v2: v1 + v2).map(generate_json)
    
    data.saveAsTextFile(DIR + "log/DF")
    sc.stop()
