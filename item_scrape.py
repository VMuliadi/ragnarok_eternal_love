# /usr/bin/python

# Created by Vinsen Muliadi <vmuliadi@max-metal.us>
# Scraping data from Ragnarok Online Mobile : Eternal Love Wiki

from bs4 import BeautifulSoup
import requests
import os
import pymongo

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

list_of_scrapable_items = []
base_url_for_item_list = 'https://www.roguard.net/db/items/'
get_latest_page = int(BeautifulSoup(requests.get(base_url_for_item_list).text, 'html.parser').findAll('a', {'class': 'page-link'})[-1].get_text())


for index in range(1, get_latest_page): 
	if index == 1: base_url = base_url_for_item_list
	else:  base_url = base_url_for_item_list + '?page=' + str(index)
	list_of_scraped_item = set()
	for table_row in BeautifulSoup(requests.get(base_url).text, 'html.parser').findAll('div', {'style': 'font-size: 1.2em;'}):
		list_of_scraped_item.add(table_row.findAll('a')[0].get_text().encode(encoding='utf-8') + '\n')

	with open('item_list.txt', 'a') as write_item:
		for item in list_of_scraped_item:
			write_item.write(item)

