# /usr/bin/python

# Created by Vinsen Muliadi <vmuliadi@max-metal.us>
# Scraping data from Ragnarok Online Mobile : Eternal Love Wiki

from bs4 import BeautifulSoup
import json
import requests
import os
# import pymongo

MONGO_HOSTNAME = ""
MONGO_USERNAME = ""
MONGO_PASSWORD = ""


# def get_item_information(item_url):
# 	scrape_text = requests.get('').text
# 	is_sellable = True if else False
# 	is_storagable = True if else False
# 	is_auctionable = True if else False
# 	item_name = BeautifulSoup(scrape_text, 'html.parser').findAll('div', {'class': ''})
# 	item_location = BeautifulSoup(scrape_text, 'html.parser').findAll('div', {'class': ''})
# 	item_description = BeautifulSoup(scrape_text, 'html.parser').findAll('div', {'class': ''})
# 	item_drop_percentage = BeautifulSoup(scrape_text, 'html.parser').findAll('div', {'class': ''})

base_url_for_item_list = 'https://www.roguard.net/db/items/'
get_latest_page = int(BeautifulSoup(requests.get(base_url_for_item_list).text, 'html.parser')\
	.findAll('a', {'class': 'page-link'})[-1]\
	.get_text())


def get_item_list():
	for index in range(1, get_latest_page): 
		if index == 1: base_url = base_url_for_item_list
		else:  base_url = base_url_for_item_list + '?page=' + str(index)
		list_of_scraped_item = set()
		for table_row in BeautifulSoup(requests.get(base_url).text, 'html.parser')\
			.findAll('div', {'style': 'font-size: 1.2em;'}):
				list_of_scraped_item.add(
					table_row
					.findAll('a')[0]\
					.get_text()\
					.encode(encoding='utf-8') + '\n'
				)

		with open('item_list.txt', 'a') as write_item:
			for item in list_of_scraped_item:
				write_item.write(item)


for index in range(1, get_latest_page):
	list_of_scraped_item = []
	if index == 1: base_url = base_url_for_item_list
	else:  base_url = base_url_for_item_list + '?page=' + str(index)
	for table_row in BeautifulSoup(requests.get(base_url).text, 'html.parser').findAll('div', {'style': 'font-size: 1.2em;'}):
		try : 
			item_details = {}
			item_details['item_name'] = table_row.get_text().encode(encoding='ascii')
			print('Processing ' + item_details['item_name'])
			item_url = 'https://www.roguard.net' + table_row.findAll('a')[0].get('href')
			item_url_scrape = BeautifulSoup(requests.get(item_url).text, 'html.parser')
			try: item_details['item_description'] = item_url_scrape.findAll('p', {'style': 'padding: 10px;'})[0].get_text()
			except: item_details['item_description'] = 'Not Available'
			item_information = item_url_scrape.findAll('td', {'class': 'text-right'})
			item_details['level'] = int(item_information[0].get_text())
			item_details['max_stack'] = int(item_information[1].get_text())
			item_details['is_sellable'] = True if item_information[2].get_text() == 'Yes' else False
			item_details['sell_price'] = str(item_information[3].get_text())
			item_details['is_auctionable'] = True if item_information[4].get_text() == 'Yes' else False
			item_details['is_storagable'] = True if item_information[5].get_text() == 'Yes' else False
			list_of_scraped_item.append(json.dumps(item_details))
		except UnicodeEncodeError: pass  # Not international item

	for item in list_of_scraped_item:
		with open('item_details.txt', 'a') as item_details:
			item_details.write(item + '\n')
