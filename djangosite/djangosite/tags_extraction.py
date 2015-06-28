import requests, re
import simplejson as json

apiSyntax = "https://api.idolondemand.com/1/api/sync/analyzesentiment/v1?text="
language = "language=eng&"
apiKey = "apikey=a06ba46e-0b5a-4fcf-9ab7-3d2f39a85035"

# outputs list of list
# Sample output: [[u'chinese', 0.7176687736973063], [u'indian', 0.8559265596235319]]
def extractTagsWithScore(inputMsg):
	inputStr = re.sub(r"\W+", "+", inputMsg) + "&"
	url = apiSyntax + inputStr + language + apiKey
	r = requests.get(url)
	call_results = json.loads(r.text)

	tags_lst_canon = []
	#separates out negative sentiment
	if call_results['positive'] or call_results['aggregate']['score'] > 0:
		for keys in call_results['positive']:
			list_of_topics = keys['topic'].split(" ")
			for item in list_of_topics:
				tags_lst_canon.append([item.lower(), keys['score']])
	else:
		print "Nothing to recommend."


	food_lst_canon = ["chinese", "indian", "afghani", "dumplings", "congee", "bubbletea", "doughnuts", "sandwiches"]

	tags_output = []
	for entry in tags_lst_canon:
		if entry[0] in food_lst_canon:
			tags_output.append(entry)
	print tags_output
	return tags_output

# testing
# message = "I like skydiving"
# extractTagsWithScore(message)

	

	
