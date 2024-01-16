import sys
import json
from pyspark import SparkContext
from pyspark.mllib.feature import Word2Vec

DIR = "../../data/"
# DIR2 = "../../data2/"

training_file = DIR + "word2vec_training_cleaned.txt"
synonyms_data_file = DIR + "word2vec_training.txt"
# training_file = DIR2 + "word2vec_training_cleaned.txt"
# synonyms_data_file = DIR2 + "word2vec_training.txt"

sc = SparkContext(appName="word2vec")

try:
    # Load and preprocess training data
    training_data = sc.textFile(training_file).map(lambda line: line.split(" "))

    # Train Word2Vec model
    word2vec = Word2Vec().setMinCount(5).setVectorSize(100).setSeed(2017).setWindowSize(4)
    model = word2vec.fit(training_data)

    # Save the model
    model.save(sc, DIR + "model/word2vec_0416")
    # model.save(sc, DIR2 + "model/word2vec_0416")

    # Generate and save synonyms data
    vec = model.getVectors()
    synonyms_data = []

    for word in vec.keys():
        if word in vec:
            synonyms = model.findSynonyms(word, 10)
            entry = {"word": word, "synonyms": [synonym for synonym, _ in synonyms]}
            synonyms_data.append(entry)

    with open(synonyms_data_file, "w", encoding="utf-8") as file:
        json.dump(synonyms_data, file, ensure_ascii=False, indent=2)

    # Test data
    test_data = ["furniture", "shaver", "toddler", "sport", "xbox", "led", "organizer"]
    for w in test_data:
        if w in vec:
            synonyms = model.findSynonyms(w, 10)
            print(f"Synonyms of {w}: {[word for word, _ in synonyms]}")
        else:
            print(f"{w} not in the vocabulary of the model.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    sc.stop()
