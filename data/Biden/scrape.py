import bs4 as bs
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

samples = {'July082020': 'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-at-ibews-2020-virtual-political-conference',
'June252020':'https://www.rev.com/blog/transcripts/joe-biden-speech-treanscript-on-health-care-affordable-care-act',
'June172020':'https://www.rev.com/blog/transcripts/joe-biden-pa-speech-transcript-on-reopening-country-amid-covid-19',
'June092020':'https://www.rev.com/blog/transcripts/joe-biden-eulogy-transcript-at-george-floyds-funeral',
'June022020':'https://www.rev.com/blog/transcripts/joe-biden-philadelphia-speech-transcript-on-protests-for-george-floyd',
'July212020':'https://www.rev.com/blog/transcripts/joe-biden-child-and-elder-care-plan-speech-transcript-july-21',
'July142020':'https://www.rev.com/blog/transcripts/joe-biden-clean-energy-plan-speech-transcript-july-14',
'July092020':'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-on-economic-recovery-plan-july-9',
'July042020':'https://www.rev.com/blog/transcripts/joe-biden-fourth-of-july-speech-2020',
'July032020':'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-to-the-national-education-association-july-3',
'July022020':'https://www.rev.com/blog/transcripts/joe-biden-video-speech-transcript-on-jobs-report-july-2',
'May292020':'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-on-minneapolis-protests-george-floyd',
'May042020':'https://www.rev.com/blog/transcripts/joe-biden-town-hall-protecting-essential-workers',
'March232020':'https://www.rev.com/blog/transcripts/joe-biden-youtube-speech-transcript-on-coronavirus-march-23',
'April072020':'https://www.rev.com/blog/transcripts/transcript-joe-biden-speech-to-afl-cio-union-members-on-coronavirus',
'March172020':'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-on-primary-night-coronavirus-economy-primaries',
'March122020':'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-on-coronavirus-march-12-2020',
'March102020':'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-after-wins-in-missouri-michigan-primaries',
'February292020':'https://www.rev.com/blog/transcripts/joe-biden-victory-speech-transcript-biden-wins-south-carolina-democratic-primary',
'February172020':'https://www.rev.com/blog/transcripts/joe-biden-reno-nevada-town-hall-campaign-transcript-february-17-2020',
'October092019':'https://www.rev.com/blog/transcripts/joe-biden-town-hall-transcript-biden-says-trump-should-be-impeached',
'August082019':'https://www.rev.com/blog/transcripts/joe-biden-iowa-trump-rebuke-speech-transcript-august-7',

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
	remove = ['joe','biden','http','https','datepublished','datemodified']
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

	outname = key+'.txt'
	outFile = open(outname,'w')
	for i in range(len(trans)):
		outFile.write(trans[i] + ' ')
	outFile.close()

	#for bit in transcript:
	#print(bit.get_text())
