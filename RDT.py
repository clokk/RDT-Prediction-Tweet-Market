# import requests


def message_slack(text):
	from urllib import request, parse
	import json

	post = {"text": "{0}".format(text)}

	try:
		json_data = json.dumps(post)
		req = request.Request("slack_api_key_goes_here",
			data=json_data.encode('ascii'),
			headers={'Content-Type': 'application/json'})
		resp = request.urlopen(req)
	except Exception as em:
		print("EXCEPTION: " + str(em))

# message_slack("Hello World")


def RDT(bracket, price, noBool):
	from bs4 import BeautifulSoup

	import urllib.request

	import json

	src = urllib.request.urlopen('https://www.predictit.org/api/marketdata/markets/5388').read()


	# result = requests.get('https://www.predictit.org/api/marketdata/markets/5388')

	# print(result.status_code)

	# print(result.headers)

	# src = result.content

	soup = BeautifulSoup(src, 'lxml')

	# print(soup)

	p = soup.find("p").getText()

	# print(p)

	jsonData = json.loads(p)

	indi = jsonData["contracts"]

	negRisk = 0

	for contracts in indi:
		print("-----")
		# print(contracts)
		name = contracts['shortName']
		lastTradePrice = contracts['lastTradePrice']
		bestBuyYesCost = contracts['bestBuyYesCost']
		bestBuyNoCost = contracts['bestBuyNoCost']
		bestSellYesCost = contracts['bestSellYesCost']
		bestSellNoCost = contracts['bestSellNoCost']
		lastClosePrice = contracts['lastClosePrice']
		id = contracts['id']
		# print("lastTradePrice: " + str(lastTradePrice))
		# print("bestBuyYesCost: " + str(bestBuyYesCost))
		# print("bestBuyNoCost: " + str(bestBuyNoCost))
		# print("bestSellYesCost: " + str(bestSellYesCost))
		# print("bestSellNoCost: " + str(bestSellNoCost))
		# print("lastClosePrice: " + str(lastClosePrice))
		if noBool == 1:
			negRisk += bestBuyYesCost

			if bestBuyNoCost < 0.80:
				message_slack("bestBuyNo alert: " + str(name) + " " + str(bestBuyNoCost))

		if bracket == name:
			delta = bestBuyYesCost - price
			print("delta: " + str(delta))
			if delta <= -0.04:
				message_slack("BAD NEWS -- bestBuyYes alert: " + str(name) + " " + str(bestBuyYesCost) + "Delta: " + str(delta))
			elif delta >= 0.04:
				message_slack("GOOD NEWS -- bestBuyYes alert: " + str(name) + " " + str(bestBuyYesCost) + "Delta: " + str(delta))


# RDT("60 - 64", 0.18, 1)

# RDT("80 - 84", 0.06, 0)

def negRisk(url):
	from bs4 import BeautifulSoup

	import urllib.request

	import json

	src = urllib.request.urlopen(url).read()

	soup = BeautifulSoup(src, 'lxml')

	p = soup.find("p").getText()

	jsonData = json.loads(p)

	indi = jsonData["contracts"]

	negRisk = 0

	for contracts in indi:
		print("-----")
		# print(contracts)
		name = contracts['shortName']
		lastTradePrice = contracts['lastTradePrice']
		bestBuyYesCost = contracts['bestBuyYesCost']
		bestBuyNoCost = contracts['bestBuyNoCost']
		bestSellYesCost = contracts['bestSellYesCost']
		bestSellNoCost = contracts['bestSellNoCost']
		lastClosePrice = contracts['lastClosePrice']
		id = contracts['id']
		print(name)
		print((1-bestBuyNoCost)*100)

		negRisk += ((1-bestBuyNoCost)*100)

	if negRisk > 109:
		message_slack("Neg Risk BUY alert: "  + str(negRisk))
	print("neg Risk: " + str(negRisk))
	# else:
		# message_slack("Neg Risk WAIT alert: "  + str(negRisk))

negRisk('https://www.predictit.org/api/marketdata/markets/5404')


