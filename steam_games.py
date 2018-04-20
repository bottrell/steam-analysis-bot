import json
import requests
import sqlite3
import sys
from bs4 import BeautifulSoup
from secrets import steam_api_key

DBNAME = 'steam.db'

CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

# User class ------------------------------------------------------------------------------------
class User(object):
	def __init__(self, steamid64 = '0', name="No Name", realname="No real name", profile_created = '2018', profile_state = 'private', location = "No location", json = None):
		self.games_library = {}
		self.top_five_friends = []
		self.full_friends_list = []
		self.steamid64 = steamid64
		self.name = name
		self.realname = realname
		self.profile_created = profile_created
		self.location = location
		self.profile_state = profile_state	
		if json != None:
			try:
				soup = BeautifulSoup(json, 'html.parser')
			except:
				pass
			try:
				panel = soup.find('div', class_ = "panel-body")
			except:
				pass
			try:
				profileinfo = panel.find_all('code')
			except:
				pass
			try:
				self.steamid = profileinfo[0].contents[0]
			except:
				pass
			try:
				self.steamid3 = profileinfo[1].contents[0]
			except:
				pass
			try:
				self.steamid64 = profileinfo[2].contents[0]
			except:
				pass
			try:
				self.customurl = profileinfo[3].contents[0].text
			except:
				pass
			try:
				self.profileurl = profileinfo[4].contents[0].text
			except:
				self.profileurl = "steamcommunity.com/profiles/" + str(steamid64)
			try:
				self.profile_state = profileinfo[5].contents[0]
			except:
				pass
			try:
				self.profile_created = profileinfo[6].contents[0]
			except:
				pass
			try:
				self.name = profileinfo[7].contents[0]
			except:
				pass
			try:
				self.realname = profileinfo[8].contents[0]
			except:
				pass
			try:
				self.location = profileinfo[9].contents[0]
			except:
				self.location = None

		#games library will be a dictionary of games and playtime
			self.games_library = self.get_games()
			self.top_five_friends = self.get_urls_for_top5_friends()
			self.full_friends_list = self.get_all_friends_urls()
	
	#returns the amount of games in the users steam library
	def __len__(self):
		return len(self.games_library)

	def __str__(self):
		return(str(self.steamid64) + " " +  self.name)

	# This function is to save space and time when gathering data
	# rather than retrieving every single one of the user's friends, will just
	# gather data on the top5 highest leveled players on the user's friends list.
	def get_urls_for_top5_friends(self):
		page_content = requests.get("https://steamcommunity.com/profiles/" + self.steamid64)
		page_content = page_content.text
		soup = BeautifulSoup(page_content, 'html5lib')
	
		nsoup = soup.find('div', class_="profile_topfriends profile_count_link_preview")
		#print(nsoup)
		nnsoup = nsoup.find_all('a', class_="friendBlockLinkOverlay")
		friendslist = []
		for x in nnsoup:
			friendslist.append(x["href"])
		friendsabbrev = []
		for x in friendslist:
			y = x.split("/")
			z = y[-1]
			friendsabbrev.append(z)

		#print(friendsabbrev)
		return friendsabbrev

	# This function will scrape from the steam website to get a list of all friend links
	# for the given user suffix. Suffix must be a valid id64 or customURL.
	# returns a list of abbreviations that correspond to the user's friends steam URLs
	def get_all_friends_urls(self):
		full_rul = "https://steamcommunity.com/profiles/" + self.steamid64 + "/friends/"
		if full_url not in CACHE_DICTION:
			page_content = requests.get(full_url)
			page_content = page_content.text
			CACHE_DICTION[full_url] = player_object
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME, 'w')
			fw.write(dumped_json_cache)
			fw.close()
		else:
			page_content = CACHE_DICTION[full_url]

		#print(page_content)
		soup = BeautifulSoup(page_content, 'html5lib')

		nnsoup = soup.find_all('a', class_='friendBlockLinkOverlay')
		#print(nnsoup)
		friendslist = []
		for x in nnsoup:
			friendslist.append(x["href"])
		friendsabbrev = []
		for x in friendslist:
			y = x.split("/")
			z = y[-1]
			friendsabbrev.append(z)

		return friendsabbrev

	# takes in a valid steamid and returns a dictionary of {appid:playtime}
	# pairs, cacheing is very important here
	def get_games(self):
		#games lib will be {appid:playtime}
		games_lib = {}

		full_url = ('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=67884AA4EAEA34CB6FDDDF9EE25680FD&steamid=' + self.steamid64 + '&format=json')
		if full_url not in CACHE_DICTION:
			player_result = requests.get(full_url)
			player_object = player_result.text
			CACHE_DICTION[full_url] = player_object
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME, 'w')
			fw.write(dumped_json_cache)
			fw.close()
		else:
			player_object = CACHE_DICTION[full_url]

		player_object = json.loads(player_object)

		for x in player_object["response"]["games"]:
			games_lib[(x["appid"])] = x["playtime_forever"]

		return games_lib


# Games class ---------------------------------------------------------------------------------
class Game(object):
	def __init__(self, json= None, steamid64 = 0, appid = 0, playtime = 0, name = "No name", price = 0, developer = "No developer", publisher = "No publisher", metacritic = 0):
		self.steamid64 = steamid64
		self.playtime = playtime
		self.appid = appid
		self.name = name
		self.developer = developer
		self.price = price

		if json != None:
			#print("there is something here")
			#print(json,end="\n\n\n")
			#print(json[str(appid)]['data'])
			self.steamid64 = steamid64
			self.playtime = playtime
			self.appid = appid
			self.name = name
			self.developer = developer
			try:
				if json[str(appid)]['success'] != True:
					pass
				else:
					content = json[str(appid)]['data']
					#print(content)
					try:
						self.name = content["name"]
					except:
						self.name = "No Name"
					#print(self.name)
					try:
						priceoverview = content["price_overview"]
						self.price = priceoverview["initial"]
						#print(self.price)
					except:
						self.price = None
					try:
						self.developer = content["developers"][0]
						#print(self.developer)
					except:
						self.developer = None
					try:
						self.publisher = content["publishers"][0]
						#print(self.publisher)
					except:
						self.publisher = None
					try:
						self.metacritic = content["metacritic"]['score']
						#print(self.metacritic)
					except:
						self.metacritic = None
					#print(self.playtime)
					#print(self.steamid64)


			except:
				print("an error occured")
	
	def add_to_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		game_list = (self.steamid64, self.appid, self.playtime, self.name, self.price, self.developer, self.publisher, self.metacritic)
		statement = '''INSERT INTO "Games" VALUES(Null,?,?,?,?,?,?,?,?)'''
		cur.execute(statement, game_list)
		conn.commit()
		update1 = '''
		UPDATE Games SET owner = (SELECT name FROM Users WHERE Games.steamid64 = Users.steamid64)
		'''
		cur.execute(update1)
		conn.commit()
		conn.close()


#-------------- INITIALIZATION FUNCTIONS ----------------------------
def init_users():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    drop_statement = '''
    DROP TABLE IF EXISTS 'Users';
    '''
    cur.execute(drop_statement)
    conn.commit()
    create_statement2 = '''

    CREATE TABLE 'Users' (
    'steamid64' INTEGER PRIMARY KEY,
    'customurl' TEXT,
    'profileurl' TEXT,
    'profile_state' TEXT,
    'profile_created' TEXT,
    'name' TEXT NOT NULL,
    'realname' TEXT,
    'location' TEXT
    );
    '''
    cur.execute(create_statement2)
    conn.commit()
    conn.close()

def init_games():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	drop_statement = '''
	DROP TABLE IF EXISTS 'Games';
	'''
	cur.execute(drop_statement)
	conn.commit()
	create_statement2 = '''
	CREATE TABLE 'Games' (
	'owner' TEXT,
	'steamid64' INTEGER ,
	'appid' INTEGER NOT NULL,
	'playtime' INTEGER,
	'name' TEXT,
	'price' INTEGER,
	'developer' TEXT,
	'publisher' TEXT,
	'metacritic' INTEGER,
	FOREIGN KEY (owner) REFERENCES Users(name)
	);
	'''
	cur.execute(create_statement2)
	conn.commit()
	conn.close()
#-------------------------------------------------------------------

# Scrapes steamidfinder for user's information, then populates the "Users" table in db
# I initially intended for this to function recursively, and gather data on every one of the
# user's friend's friends' and so on, but that ran for a long time as you can imagine.
#returns a User object
def get_user_info_and_populate_users(user_id):
	base_url = 'https://steamidfinder.com/lookup/'
	full_url = base_url + user_id
	if full_url not in CACHE_DICTION:
		html = requests.get(full_url)
		html = html.text
		CACHE_DICTION[full_url] = html
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME, 'w')
		fw.write(dumped_json_cache)
		fw.close()
	else:
		html = CACHE_DICTION[full_url]

	my_user = User(json= html)
	if my_user.profileurl == 'steamcommunity.com/profiles/0':
		return None
	else:
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		insertion = (my_user.steamid64, my_user.customurl, my_user.profileurl, my_user.profile_state, my_user.profile_created, my_user.name, my_user.realname, my_user.location)
		statement = '''INSERT INTO "Users" VALUES(?,?,?,?,?,?,?,?)'''
		cur.execute(statement, insertion)
		conn.commit()
		#print("Added item to db")
		conn.close()
	return my_user


# Makes a request to the steam api about a specific game id
# returns the json object returned from that API call
def get_game_info(appid):
	full_url = 'http://store.steampowered.com/api/appdetails?appids=' + str(appid)
	if full_url not in CACHE_DICTION:
		game_result = requests.get(full_url)
		game_object = game_result.text
		CACHE_DICTION[full_url] = game_object
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME, 'w')
		fw.write(dumped_json_cache)
		fw.close()
	else:
		game_object = CACHE_DICTION[full_url]

	game_object = json.loads(game_object)
	
	return game_object


# Goes through a user's games and graphs out the amount of time they 
# have played per game in their library
def graph_user_playtime(id64):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	statement = '''
	SELECT *
	FROM Games
	WHERE steamid64 = {}
	'''.format(id64)
	cur.execute(statement)
	lst = cur.fetchall()
	total_hours = 0
	hours_list = []
	titles_list = []
	for x in lst:
		titles_list.append(x[4])
		hours_played = x[3]
		hours_played = round(hours_played / 60,2)
		hours_list.append(hours_played)
		total_hours += hours_played

	import plotly.offline as py
	import plotly.graph_objs as go

	labels = titles_list
	values = hours_list

	trace = go.Pie(labels=labels, values=values)

	py.plot([trace], filename='basic_pie_chart')
	


# Will simply go through the 'Games' table and graph the most popular in your friend group
# based off of total playtime
def graph_games_by_popularity():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	statement = '''
	SELECT name, SUM(playtime), developer, publisher, metacritic
	FROM Games
	GROUP BY name
	ORDER BY SUM(playtime)
	DESC
	LIMIT 10
	'''
	cur.execute(statement)
	lst = cur.fetchall()
	total_hours = []
	names_list = []
	for x in lst:
		names_list.append(x[0])
		total_hours.append(round((x[1]/60),2))
	import plotly.offline as py
	import plotly.graph_objs as go
	data = [go.Bar(
            x=names_list,
            y=total_hours)]
	py.plot(data, filename='Distribution of playtime for steam friends')

# Will assign each user a "best friend score" for the user, 
# Based on the amount of similar games they play, location, 
# price spent on games, and total playtime of games
def arbitrary_best_steam_friend(user_id):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	statement = '''SELECT *
	FROM Games
	WHERE steamid64 = {}
	ORDER BY playtime
	DESC
	LIMIT 1
	'''.format(user_id)
	cur.execute(statement)
	my_top_game = cur.fetchone()
	playtime = my_top_game[3]
	lower_bound = playtime * .5
	upper_bound = playtime * 1.5
	statement2 = '''
	SELECT *
	FROM Games
	WHERE appid = {} and playtime > {} and playtime < {} and steamid64 != {}
	ORDER BY playtime
	DESC
	'''.format(my_top_game[2], lower_bound, upper_bound , user_id)
	cur.execute(statement2)
	all_potential_friends = cur.fetchall()
	friend_score = []
	name = []
	for x in all_potential_friends:
		name.append(x[0])
		score = playtime / x[3]
		friend_score.append(score)

	import plotly.offline as py
	import plotly.graph_objs as go

	labels = name
	values = friend_score
	if name == [] or friend_score == []:
		print("Couldn't find the right match!")
		return
	else:
		trace = go.Pie(labels=labels, values=values)

		py.plot([trace], filename='best_steam_friends')





# Will graph games based on the total amount of hours played % total price
# A scatterplot would probably look very nice for this one
def best_game_for_price():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	statement = '''
	SELECT name, AVG(playtime/60),SUM((playtime/60)) / SUM(price/100), price
	FROM Games
	GROUP BY name
	ORDER BY SUM((playtime/60)) / SUM(price/100)
	DESC
	LIMIT 15'''
	cur.execute(statement)
	lst = cur.fetchall()
	name_list = []
	total_hours_played = []
	price_list = []
	hours_per_dollar = []
	for x in lst:
		name_list.append(x[0])
		total_hours_played.append(x[1])
		hours_per_dollar.append(x[2])
		price_list.append(x[-1])

	for cost in range(len(price_list)):
		price_list[cost] = price_list[cost] / 100
	import plotly.offline as py
	import plotly.graph_objs as go

	trace0 = go.Scatter(
		x=price_list,
		y=total_hours_played,
		marker=dict(
        color='purple',
        size=20),
		mode='markers',
		text=name_list)
	layout = go.Layout(
    	title="Best Steam Games by Hours Played Per Dollar",
    	xaxis = dict(
    	range=[0, 50]),
    	yaxis = dict(
        range=[0, 1200]),
        height=1000,
        width=2000)
	data=[trace0]
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'basic-line')



def initialize_and_populate():
	init_users()
	init_games()
	user_name = input("Please enter a steam ID, url, customurl, or steamid64: ")
	my_user = get_user_info_and_populate_users(user_name)
	user_list = [my_user]
	for x in my_user.full_friends_list:
		try:
			user_list.append(get_user_info_and_populate_users(x))
		except:
			pass
	

	games = []
	for x in user_list:
		if x == None:
			pass
		else:
			for y in x.games_library:
				owner_id = x.steamid64
				my_game = Game(appid = y, steamid64 = owner_id, json = get_game_info(y), playtime = x.games_library[y])
				try:
					my_game.add_to_table()
				except:
					pass

def main():
	if (len(sys.argv) > 1):
		initialize_and_populate()
	
	print("Welcome to the Steam Analyzer bot!")
	print("Main Menu: ",end= "\n----------\n")
	print(
		'''
		1.) Graph friend's playtime\n
		2.) Graph the most popular games in your friend group\n
		3.) Find out who your best steam friend is!\n
		4.) Find out the best game for the price\n
		5.) Reinitialize the database\n
		6.) Quit the program
		''')
	user_input = input("Enter a choice: ")
	
	while user_input != '6':
		if user_input == '5':
			initialize_and_populate()

		#all of our plotly commands will go here
		elif user_input == '1':
			input_name = input("What is the id64 of the player you would like to graph? --> ")
			graph_user_playtime(input_name)
		elif user_input == '2':
			graph_games_by_popularity()
		elif user_input == '3':
			user_name = input("What is your steamid64? --> ")
			arbitrary_best_steam_friend(user_name)
		elif user_input == '4':
			best_game_for_price()
		else:
			print("Sorry that is not a valid command. Please try again...")

		print(
		'''
		1.) Graph friend's playtime\n
		2.) Graph the most popular games in your friend group\n
		3.) Find out who your best steam friend is!\n
		4.) Find out the best game for the price\n
		5.) Reinitialize the database\n
		6.) Quit the program
		''')
		user_input = input("Enter a choice: ")

	print("Thanks for using the Steam Analyzer bot!")
	return 
	





if __name__ == "__main__":
	main()