import json
import requests
import sqlite3
import bs4
from secrets import steam_api_key

DBNAME = 'steam.db'

CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

playerid = '76561198035655245'
url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=67884AA4EAEA34CB6FDDDF9EE25680FD&steamids=' + str(playerid)
if url not in CACHE_DICTION:
    html = requests.get(url)
    CACHE_DICTION[url] = html.text
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME, 'w')
    fw.write(dumped_json_cache)
    fw.close()
    #soup = BeautifulSoup(html.text, 'html.parser')              
else:
    html = CACHE_DICTION[url]

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
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'communityId' TEXT,
    'Username' TEXT,
    'RealName' TEXT,
    'GameCount' TEXT,
    'Country' TEXT
    );
    '''
    cur.execute(create_statement2)
    conn.commit()
    conn.close()

init_users()

def populate_users():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    for x in CACHE_DICTION:
        y = json.loads(CACHE_DICTION[x])
        response = y["response"]
        #gamecount = response["game_count"]
        players = response["players"][0]
        print(players)
        username = players['personaname']
        steamid = players['steamid']
        country = players["loccountrycode"]
        try:
            realname = players['realname']
        except:
            realname = "No name found"
        insertion = (None, steamid, username, realname, None, country)
        statement = '''INSERT INTO "Users" VALUES(?,?,?,?,?,?)'''
        cur.execute(statement, insertion)
    """with open('countries.json') as json_data:
        d = json.load(json_data)
        for x in d:
            #print(x,end="\n\n\n\n\n\n\n\n\n\n\n")
            #ID = x["alpha2Code"]
            username = x["alpha3Code"]
            realname = x["name"]
            gamecount = x["region"]
            country = x["subregion"]
            insertion = (None, username, realname, gamecount, country)
            statement = '''INSERT INTO "Users"
            VALUES(?,?,?,?,?,?,?,?)
            '''
            cur.execute(statement, insertion)
"""
    conn.commit()
    conn.close()

populate_users()

def chooseGame(playerid):
    games_lib = []
    player_result = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=67884AA4EAEA34CB6FDDDF9EE25680FD&steamid=' + playerid + '&format=json')
    player_object = json.loads(player_result.text)
    print("\n\nGame Count: ")
    print(player_object["response"]["game_count"])
    
    print("--------------------------------------------------------------")
    
    for x in player_object["response"]["games"]:
        games_lib.append(str(x["appid"]))
    #chooses random game from your library
    appid = (random.choice(games_lib))
    return appid



def getGameInfo(appid):
    game_result = requests.get('http://store.steampowered.com/api/appdetails?appids=' + appid)
    game_object = json.loads(game_result.text)
    print("You should play: " + game_object[appid]['data']["name"])
    print("--------------------------------------------------------------")
    print("Release Date: " + game_object[appid]['data']['release_date']["date"])
    print("-------------------------------------------------------------- \n \n")
    return