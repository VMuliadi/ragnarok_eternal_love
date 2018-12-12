# /usr/bin/python3

# Created by Vinsen Muliadi <vmuliadi@max-metal.us>
# Scraping data from Ragnarok Online Mobile : Eternal Love Wiki

from bs4 import BeautifulSoup
import json
import requests
import os
requests.packages.urllib3.disable_warnings()
# import pymongo

base_url_for_item_list = 'https://www.roguard.net/db/items/'
get_latest_page = int(
	BeautifulSoup(requests.get(base_url_for_item_list, verify=False).text, 'html.parser')\
		.findAll('a', {'class': 'page-link'})[-1]\
		.get_text())


def get_item_list():
	for index in range(1, get_latest_page): 
		if index == 1: base_url = base_url_for_item_list
		else:  base_url = base_url_for_item_list + '?page=' + str(index)
		list_of_scraped_item = set()
		for table_row in BeautifulSoup(requests.get(base_url, verify=False).text, 'html.parser')\
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


def write_item_details_to_file():
	for index in range(1, get_latest_page):
		list_of_scraped_item = []
		if index == 1: base_url = base_url_for_item_list
		else:  base_url = base_url_for_item_list + '?page=' + str(index)
		for table_row in BeautifulSoup(requests.get(base_url, verify=False).text, 'html.parser').findAll('div', {'style': 'font-size: 1.2em;'}):
			try : 
				item_details = {}
				item_details['item_name'] = table_row.get_text().encode(encoding='ascii')
				print('Processing ' + item_details['item_name'])
				item_url = 'https://www.roguard.net' + table_row.findAll('a')[0].get('href')
				item_url_scrape = BeautifulSoup(requests.get(item_url, verify=False).text, 'html.parser')
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
			except UnicodeEncodeError: pass  # Not an international item

		for item in list_of_scraped_item:
			with open('item_details.txt', 'a') as item_details:
				item_details.write(item + '\n')

