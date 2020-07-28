from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import glob
import pandas as pd
from numpy import random

transcripts = glob.glob('../data/Biden/*.txt')

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
		#print(line)
		words += word_tokenize(line)
		#tokens = word_tokenize(line)
		#words.append(tokens)
	seperator = ' '
	speeches.append(seperator.join(words))

#print(speeches[0])

#print(speeches[0])
#print('=================')
#print(speeches[1])

#tfidf_vectorizer=TfidfVectorizer(use_idf=True)
#fitted_vectorizer = tfidf_vectorizer.fit_transform(speeches)
#tfidf_vectorizer_vectors = fitted_vectorizer.transform(speeches)

vectorizer = TfidfVectorizer()
vectorized_speeches = vectorizer.fit(speeches)

X = vectorizer.transform(speeches)

#print(vectorizer.vocabulary_)
#print(vectorizer.idf_)


#X = tfidf_vectorizer_vectors


#cv = CountVectorizer()

#vectorizer = TfidfVectorizer(stop_words = 'english')
#X = cv.fit_transform(speeches)
#tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
#tfidf_transformer.fit(X)
#count_vector=cv.transform(speeches)
#tf_idf_vec = tfidf_transformer.transform(count_vector)
#X = vectorizer.fit_transform(speeches)

#for k in range(4):

#df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["idf_weights"]

#df_idf.sort_values(by=['idf_weights'])

#feature_names = cv.get_feature_names()
#first_doc_vec = tf_idf_vec[0]
#print(first_doc_vec)

k = 3	
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

#for i in range(len(testing)):
#	Y = vectorizer.transform(testing[i])
#	prediction = model.predictY
#	print(prediction)

