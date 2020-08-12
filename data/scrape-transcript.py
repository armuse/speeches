import bs4 as bs
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

samples_trump = {
'July242020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-july-24-signs-executive-orders-to-lower-prescription-drug-prices',
'July162020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-on-rolling-back-environmental-regulations',
'July152020':'https://www.rev.com/blog/transcripts/donald-trump-atlanta-speech-transcript-on-rebuilding-infrastructure-july-15',
'July092020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-on-his-executive-order-for-the-hispanic-prosperity-initiative-july-9',
'July072020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-safely-reopening-schools-amid-covid-19-pandemic',
'July042020':'https://www.rev.com/blog/transcripts/donald-trump-salute-to-america-speech-transcript',
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
'August062020':'https://www.rev.com/blog/transcripts/donald-trump-speaks-at-ohio-airport-transcript-august-6-says-joe-biden-against-god',
'August052020':'https://www.rev.com/blog/transcripts/donald-trump-coronavirus-press-conference-transcript-august-5',
'July282020':'https://www.rev.com/blog/transcripts/donald-trump-coronavirus-press-conference-transcript-july-28',
'April282020':'https://www.rev.com/blog/transcripts/donald-trump-coronavirus-press-conference-transcript-april-28',
'February172020':'https://www.rev.com/blog/transcripts/trump-speech-transcript-at-opportunity-now-summit-in-charlotte-nc',
'March282020':'https://www.rev.com/blog/transcripts/transcript-donald-trump-gives-speech-sending-off-hospital-ship-to-nyc-considers-quarantining-new-york',
'May222020':'https://www.rev.com/blog/transcripts/trump-speech-transcript-at-rolling-to-remember-ceremony-honoring-veterans',
'May072020':'https://www.rev.com/blog/transcripts/donald-trump-mike-pence-melania-trump-national-prayer-day-speech-transcript',
'May052020':'https://www.rev.com/blog/transcripts/donald-trump-press-conference-speech-transcript-at-honeywell-plant-may-5',
'April222020':'https://www.rev.com/blog/transcripts/donald-trump-mike-pence-earth-day-speech-transcript',
'April162020':'https://www.rev.com/blog/transcripts/donald-trump-speech-american-truckers-transcript',
'March132020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-declares-coronavirus-national-emergency',
'March112020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-on-coronavirus-ban-on-europe-travel',
'March032020':'https://www.rev.com/blog/transcripts/donald-trump-national-association-of-counties-speech-transcript',
'February202020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-at-the-hope-for-prisoners-graduation-ceremony',
'February162020':'https://www.rev.com/blog/transcripts/donald-trump-daytona-500-speech-transcript-trump-is-first-president-to-be-daytona-grand-marshal',
'February102020':'https://www.rev.com/blog/transcripts/donald-trump-national-governors-association-speech-transcript',
'February072020':'https://www.rev.com/blog/transcripts/trump-speech-transcript-at-opportunity-now-summit-in-charlotte-nc',
'February062020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-2020-national-prayer-breakfast-trump-goes-after-romney-and-democrats-in-speech',
'February042020':'https://www.rev.com/blog/transcripts/donald-trump-state-of-the-union-speech-transcript-february-4-2020',
'January282020':'https://www.rev.com/blog/transcripts/donald-trump-middle-east-peace-speech-transcript-with-israel-pm-netanyahu',
'January242020':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-trump-speaks-at-march-for-life-event',
'January082020':'https://www.rev.com/blog/transcripts/donald-trump-iran-statement-transcript-trump-makes-statement-after-iran-attacks-us-bases-in-iraq',
'January032020':'https://www.rev.com/blog/transcripts/donald-trump-iran-statement-speech-transcript-trump-orders-strike-on-qasem-soleimani',
'October272019':'https://www.rev.com/blog/transcripts/donald-trump-raid-announcement-transcript-isis-leader-abu-bakr-al-baghdadi-killed',
'October032019':'https://www.rev.com/blog/transcripts/trump-transcript-trump-says-china-should-investigate-biden',
'August212019':'https://www.rev.com/blog/transcripts/transcript-donald-trump-states-i-am-the-chosen-one-in-front-of-white-house-in-china-statement-to-press',
'August142019':'https://www.rev.com/blog/transcripts/donald-trump-pennsylvania-speech-transcript-august-13-full-transcript',
'August052019':'https://www.rev.com/blog/transcripts/donald-trump-statement-on-mass-shootings-full-transcript-of-remarks',
'July312019':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-in-jamestown-virginia-july-30-2019',
'July232019':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-turning-point-usa-teen-student-summit-speech',
'July052019':'https://www.rev.com/blog/transcripts/donald-trump-4th-of-july-event-speech-transcript-full-transcript',
'July282017':'https://www.rev.com/blog/transcripts/donald-trump-speech-transcript-gang-violence-law-enforcement-police',
'April192016':'https://www.rev.com/blog/transcripts/donald-trump-michigan-speech-transcript-asks-black-voters-what-do-you-have-to-lose',

}

samples_biden = {'July082020': 'https://www.rev.com/blog/transcripts/joe-biden-speech-transcript-at-ibews-2020-virtual-political-conference',
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

samples = samples_trump

lemmatizer = WordNetLemmatizer()

for key in samples:
	url = samples[key]

	grURL = requests.get(url)
	grHTML = grURL.text

	#get speech
	soup = bs.BeautifulSoup(grHTML, 'html.parser')
	transcript = soup.find_all('script', attrs={'saswp-schema-markup-output'})

	wordsFromTranscript = [] #output
	stop_words = set(stopwords.words('english'))
	removeThese = ['donald','trump','http','https','datepublished','datemodified',
		'thank','america','great','president','going','american','want','like',
		'people','know','url','got','say','said','good','everybody','make','again',
		'opportunity','really']
	stop_words.update(removeThese)

	for words in transcript:
		article = words.get_text()
		article = article.split(',')
		#print(article[10:-28]) #Read full transcript here / keywords
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
					wordsFromTranscript.append(word)

	outname = 'Trump/'+key+'.txt'
	outFile = open(outname,'w')
	for i in range(len(wordsFromTranscript)):
		outFile.write(wordsFromTranscript[i] + ' ')
	outFile.close()
