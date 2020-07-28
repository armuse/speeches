import bs4 as bs
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

samples = {'July242020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-july-24-signs-executive-orders-to-lower-prescription-drug-prices',
'July162020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-on-rolling-back-environmental-regulations',
'July152020':'https://www.rev.com/blog/transcripts/donald-trump-atlanta-speech-transcript-on-rebuilding-infrastructure-july-15',
'July092020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-on-his-executive-order-for-the-hispanic-prosperity-initiative-july-9',
'July072020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-safely-reopening-schools-amid-covid-19-pandemic',
'July0420200':'https://www.rev.com/blog/transcripts/donald-trump-salute-to-america-speech-transcript',
'July032020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-at-mount-rushmore-4th-of-july-event',
'July022020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-at-spirit-of-america-showcase',
'June262020':'https://www.rev.com/blog/transcripts/donald-trump-speech-to-american-workforce-policy-advisory-board-june-26',
'June232020':'https://www.rev.com/blog/transcripts/donald-trump-phoenix-arizona-speech-transcript-turning-point-usa',
'June172020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-announcing-task-force-on-veteran-suicide-prevention',
'June132020':'https://www.rev.com/blog/transcripts/donald-trump-west-point-commencement-speech-transcript',
'May302020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-at-kennedy-space-center-after-spacex-nasa-launch',
'May262020':'https://www.rev.com/blog/transcripts/donald-trump-transcript-on-protecting-seniors-with-diabetes-may-26',
'May252020':'https://www.rev.com/blog/transcripts/donald-trump-memorial-day-speech-transcript-2020',
'May212020':'https://www.rev.com/blog/transcripts/donald-trump-speech-at-ford-plant-in-michigan-full-transcript',
'May192020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-supporting-farmers-ranchers-may-19',
'May152020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-on-vaccine-development-for-coronavirus',
'May142020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-at-pennsylvania-distribution-center-for-coronavirus-relief-supplies',

}

lemmatizer = WordNetLemmatizer()

for key in samples:
	url = samples[key]

	grURL = requests.get(url)
	grHTML = grURL.text

	soup = bs.BeautifulSoup(grHTML, 'html.parser')
	transcript = soup.find_all('script', attrs={'saswp-schema-markup-output'})

	trans = [] #output
	stop_words = set(stopwords.words('english'))
	remove = ['donald','trump','http','https','datepublished','datemodified']
	stop_words.update(remove)

	for words in transcript:
		article = words.get_text()
		article = article.split(',')
		print(article[10:-28]) #Read full transcript here / keywords
		separator = ','
		article = separator.join(article)
		speech = word_tokenize(article)
		for word, tag in pos_tag(speech):
			word = word.lower()
			if tag.startswith('NN'):
				pos='n'
			elif tag.startswith('VB'):
				pos = 'v'
			else:
				pos = 'a'
			if word.isalnum():
				lemmed_word = lemmatizer.lemmatize(word,pos)
				if not lemmed_word in stop_words:
					trans.append(word)

	outname = 'Trump/'+key+'.txt'
	outFile = open(outname,'w')
	for i in range(len(trans)):
		outFile.write(trans[i] + ' ')
	outFile.close()

	#for bit in transcript:
	#print(bit.get_text())
