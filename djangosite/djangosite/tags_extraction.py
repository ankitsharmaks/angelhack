import requests, re
import simplejson as json

apiSyntax = "https://api.idolondemand.com/1/api/sync/analyzesentiment/v1?text="
language = "language=eng&"
apiKey = "apikey=a06ba46e-0b5a-4fcf-9ab7-3d2f39a85035"

def main(inputMsg):
	inputStr = re.sub(r"\W+", "+", inputMsg) + "&"

	#inputStr = inputMsg.replace(" ", "+") + "&"
	url = apiSyntax + inputStr + language + apiKey
	
	r = requests.get(url)	

	call_results = json.loads(r.text)
	#print call_results
	#separates out negative sentiment
	if call_results['positive'] or call_results['aggregate']['score'] > 0:

		for keys in call_results['positive']:
			tags_lst = (keys['topic']).split(" ")
			tags_lst_canon = [x.lower() for x in tags_lst]
	else:
		print "Nothing to recommend."


	food_lst_canon = ["chinese", "indian", "afghani", "dumplings", "congee", "bubbletea", "doughnuts", "sandwiches"]
	
	tags_output = []
	
	for word in tags_lst_canon:
		if word in food_lst_canon:
			tags_output.append(word)

	return tags_output		
			

if __name__ == '__main__':
	main("I want chinese or indian food.")
	

	
