import requests
import simplejson as json

apiSyntax = "https://api.idolondemand.com/1/api/sync/analyzesentiment/v1?text="
language = "language=eng&"
apiKey = "apikey=a06ba46e-0b5a-4fcf-9ab7-3d2f39a85035"

# outputs list of list
# Sample output: [[u'chinese', 0.7176687736973063], [u'indian', 0.8559265596235319]]
def extractTagsWithScore(inputMsg):
	for ch in [",", " "]:
		if ch in inputMsg:
			inputStr=inputMsg.replace(ch, "+") + "&"

	url = apiSyntax + inputStr + language + apiKey
	r = requests.get(url)
	print r.text
	call_results = json.loads(r.text)
	
	tags_lst_canon = []
	try:
		#handles positive sentiment
		if call_results['positive']:
			for keys in call_results['positive']:
				list_of_topics = keys['topic'].split(" ")
				for item in list_of_topics:
					tags_lst_canon.append([item.lower(), keys['score']])
				#print tags_lst_canon

		#handles neutral sentiment
		elif call_results['aggregate']['score'] == 0:
			tags_lst_neutral = inputStr[:-1].split("+")
			for item in tags_lst_neutral:
				tags_lst_canon.append([item.lower(), '0.01'])
				#print tags_lst_canon

		#handles negative sentiment		
		elif not call_results['positive']:
			print 'Nothing positive to recommend.'
			tags_lst_canon =[]

		food_lst_canon =['afghan',
		'algerian',
		'american',
		'angolan',
		'argentine',
		'australian',
		'austrian',
		'backshop',
		'bagels',
		'bakeries',
		'bangladeshi',
		'beer',
		'wine',
		'spirits',
		'belarusian',
		'belgian',
		'beverage store',
		'bolivian',
		'bosnian/herzegovinian',
		'brazilian',
		'breweries',
		'british',
		'bubble tea',
		'bulgarian',
		'butcher',
		'cafe'
		'cafes'
		'cambodian',
		'cameroonian',
		'canadian',
		'candy stores',
		'central african',
		'chadian',
		'cheese shops',
		'chinese',
		'chocolate',
		'chocolatiers & shops',
		'churros',
		'coffee',
		'coffee & tea supplies',
		'coffee & tea',
		'colombian',
		'congolese',
		'congolese',
		'convenience stores',
		'costa rican',
		'croatian',
		'csa',
		'cupcakes',
		'czech',
		'danish',
		'delicatessen',
		'desserts',
		'distilleries ',
		'do-it-yourself food',
		'donairs',
		'donuts',
		'dutch',
		'ecuadorian',
		'egyptian',
		'emirati',
		'english',
		'estonian',
		'ethic grocery',
		'ethiopian',
		'ethnic food',
		'ethnic grocery',
		'farmers market',
		'finnish',
		'fishmonger',
		'food delivery services',
		'food trucks',
		'french',
		'friterie',
		'fruits & veggies',
		'gelato',
		'german',
		'ghanaian',
		'greek',
		'grocery',
		'guatemalan',
		'happy hour',
		'hawker centre',
		'health markets',
		'herbs & spices',
		'honduran',
		'honey',
		'hungarian',
		'ice cream & frozen yogurt',
		'icelandic',
		'indian',
		'indonesian',
		'internet cafes',
		'iranian',
		'iraqi',
		'irish',
		'israeli',
		'italian',
		'ivorian',
		'jamaican',
		'japanese sweets',
		'japanese',
		'jordanian',
		'juice bars & smoothies',
		'kazakh',
		'kenyan',
		'kiosk',
		'lao',
		'latvian',
		'libyan',
		'lithuanian',
		'macarons',
		'malagasy',
		'malaysian',
		'malian',
		'mauritanian',
		'meat shops',
		'mexican',
		'milkshake bars',
		'moroccan',
		'mulled wine',
		'namibian',
		'nasi lemak',
		'nicaraguan',
		'nigerian',
		'nigerien',
		'norwegian',
		'omani',
		'organic stores',
		'pakistani',
		'panamanian',
		'panzerotti',
		'paraguayan',
		'parent cafes',
		'pasta shops',
		'patisserie/cake shop',
		'peruvian',
		'philippine',
		'piadina',
		'polish',
		'popcorn shops',
		'portuguese',
		'pretzels',
		'romanian',
		'russian',
		'salumerie',
		'salvadoran',
		'saudi arabian',
		'scottish',
		'seafood markets',
		'senegalese',
		'serbian',
		'shaved ice',
		'singaporean',
		'slovak',
		'somalian',
		'south african',
		'spanish',
		'specialty food',
		'street vendors',
		'sudanese',
		'swedish',
		'swiss',
		'syrian',
		'tea rooms',
		'thai',
		'tofu shops',
		'torshi',
		'tortillas',
		'tunisian',
		'turkish',
		'turkmen',
		'ukranian',
		'uruguayan',
		'vietnamese',
		'welsh',
		'wine tasting room',
		'wineries',
		'zambian',
		'zapiekanka',
		'zimbabwean']

		tags_output = []

		#generating list of lists of tags
		for entry in tags_lst_canon:
			if entry[0] in food_lst_canon:
				tags_output.append(entry)

		#print tags_output
		return tags_output

	except:
		pass
# testing
#message = "I absolutely loove malaysian."
#extractTagsWithScore(message)

	

	
