from bs4 import BeautifulSoup
import json
import requests

BASE_URL = 'https://www.roguard.net/db/maps/'
list_of_ragnarok_maps = []
for ragnarok_map_list in BeautifulSoup(requests.get(BASE_URL).text, 'html.parser').findAll('table')[0].findAll('tr'):
	try :
		ragnarok_map = {}
		map_name = ragnarok_map_list.findAll('td')[0].findAll('div', {'style': 'font-size: 1.2em;'})[0].get_text().encode(encoding='ascii')
		map_level_range = ragnarok_map_list.findAll('td')[1].findAll('div')[1].get_text().encode(encoding='ascii')
		ragnarok_map['map_name'] = map_name[1:] if map_name.startswith(r'\s') else map_name
		ragnarok_map['level_range'] = 'Not Available' if map_level_range == '-' else map_level_range
		ragnarok_map['monster_list'] = []
		for ragnarok_monster_list in ragnarok_map_list.findAll('td')[2].findAll('div'):
			ragnarok_monster_details = {}
			ragnarok_monster_details['monster_name'] = ragnarok_monster_list.get_text().split(' (')[0][:-1].encode(encoding='ascii')
			ragnarok_monster_details['monster_level'] = ragnarok_monster_list.get_text().split(' (')[1].replace(')', '').encode(encoding='ascii')
			ragnarok_map['monster_list'].append(ragnarok_monster_details)
		list_of_ragnarok_maps.append(json.dumps(ragnarok_map))
	except UnicodeEncodeError: pass

with open('maps_details.json', 'a') as maps_details: maps_details.write('{\n"maps_details": [\n')
for ragnarok_map in list_of_ragnarok_maps: 
	with open('maps_details.json', 'a') as maps_details: 
		maps_details.write(str(ragnarok_map) + ',\n')
with open('maps_details.json', 'a') as maps_details: maps_details.write('\n]\n}')
