import json
import requests


def get_bet_from_fonbet(sports,events,custom_factors, ID):
	"""
		функция возвращает параметры событий,
		категория, названия события, игроки, коэффиценты,
		которые входят список категорий ID

	"""

	turnirs,list_category = {},{}
	curent_args = 'id','parentId','name'
	parent_args = ('name',)
	# всписке  sports по параметру parenrId, выделяем соревнования и
	# категории, которые входят в список ID?
	# для категорий сохраняем id,name
	# для соревнования id,name, parentId,
	# по parentId соревнования можно получить name категории
	 
	for i in sports:
		curent_id = i.get('id')
		parent_id = i.get('parentId')
		if not parent_id and curent_id in ID:
			list_category[curent_id] = {j:i.get(j) for j in parent_args}
		elif parent_id in ID:
			turnirs[curent_id] = {j:i.get(j) for j in curent_args}

	list_action = turnirs.keys()
	# print(list_action)
	list_events= {}
	args = ['name','team1','team2','sportId','id','parentId']
	# если событие входит внужную нам категорию, запоминаем нужные параметры 
	for i in events:
		if i.get('sportId') not in list_action:
			continue
		list_events[i.get('id')] = {j:i.get(j) for j in args}
	# print(list_events)

	list_action_events = list_events.keys()
	rate_events={}
	curent_args = 'f','pt','v'

	# из списка коэффициентов запоминаем те, на которые ссылаются события 
	for i in custom_factors:
		event_id = i.get('e')
		if event_id in list_action_events:
			kof = '|,|'.join(str(i.get(j)) for j in curent_args if i.get(j))
			rate_events.setdefault(event_id,[]).append(kof)
		
	list_result = []
	
	# выбираю необхлдимые данные
	for i in list_events:
		rate = rate_events.get(i)
		if rate:
			id_fon = i
			category = list_category[turnirs[list_events[i]['sportId']]['parentId']]['name']
			event_name = turnirs[list_events[i]['sportId']]['name']
			event_name += ' ' + list_events[i].get('name')
			parent_id = list_events[i].get('parentId')
			curent_event = list_events[parent_id] if parent_id else list_events[i]
			gamer = curent_event.get('team1'),curent_event.get('team2')
			kof = ';|'.join(rate) + '|;|'
			# print(id_fon,category,event_name,gamer,kof)
			list_result.append({'category':category,'event_name':event_name,
								'id_fon':id_fon,'gamer':gamer,'kof':kof})
	return list_result


if __name__ == '__main__':
	ID = 29086,40479,40480,40481,44943,45827
	link_fonbet = 'https://line16.bkfon-resource.ru/live/currentLine/ru/'
	data = requests.get(link_fonbet,verify=False).json()
	# json.load(open('fonbet_ofline.json'))
	list_event_kof = get_bet_from_fonbet(data.get('sports'),data.get('events'),data.get('customFactors'),ID)
	with open('fonbet_kof.json','w') as f:
		json.dump(list_event_kof,f,indent=4)
	# print()

