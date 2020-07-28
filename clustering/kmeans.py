from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import glob
import pandas as pd
from numpy import random

transcripts = glob.glob('../data/Trump/*.txt')
#transcripts = glob.glob('../data/Biden/*.txt')

random.shuffle(transcripts)
trainFrac = int(len(transcripts)*0.9)

training = transcripts[:trainFrac]
testing = transcripts[trainFrac:]
speeches = []
for i in range(len(training)):
	#print('Speech '+str(i))
	speech = open(training[i],'r')
	words = []
	for line in speech:
		words += word_tokenize(line)
	seperator = ' '
	speeches.append(seperator.join(words))

vectorizer = TfidfVectorizer()
vectorized_speeches = vectorizer.fit(speeches)

X = vectorizer.transform(speeches)

k = 5	
model = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster (out of" +str(k)+":")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(k):
	print("Cluster %d: " % i),
	for ind in order_centroids[i, :10]:
		print(' %s' % terms[ind]),
	print

print("\n") 
print("prediction")

Y = vectorizer.transform(testing)
prediction = model.predict(Y)
print(prediction)


for i in range(len(transcripts)):
	Z = vectorizer.transform(transcripts)
	print(transcripts[i][14:-4])
	classification = model.predict(Z)
	print(classification)

#for i in range(len(testing)):
#	Y = vectorizer.transform(testing[i])
#	prediction = model.predictY
#	print(prediction)

