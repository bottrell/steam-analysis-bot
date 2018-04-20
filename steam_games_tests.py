import unittest
import json
import requests
import steam_games as steam

class TestMedia(unittest.TestCase):

# ------------ TESTS FOR PART 1 ------------
    def testUserConstructor(self):
    	user1 = steam.User()
    	self.assertEqual(user1.steamid64, '0')
    	self.assertEqual(user1.name, "No Name")
    	self.assertEqual(user1.realname, "No real name")
    	self.assertEqual(user1.profile_created, "2018")
    	self.assertEqual(user1.location, "No location")
    	self.assertEqual(user1.profile_state, "private")

    def testGamesConstructor(self):
    	game1 = steam.Game()
    	self.assertEqual(game1.steamid64, 0 )
    	self.assertEqual(game1.appid,0 )
    	self.assertEqual(game1.playtime, 0)
    	self.assertEqual(game1.name, "No name" )
    	self.assertEqual(game1.price, 0)

    def testTop5Friends(self):
    	user1 = steam.User(steamid64 = '76561198072467455')
    	top5 = user1.get_urls_for_top5_friends()
    	self.assertEqual(top5[0], 'onlinekeystore')
    	self.assertEqual(top5[1], 'therealBEAST')
    	self.assertEqual(top5[2], 'Nipfip')
    	self.assertEqual(top5[3], 'Silversray')
    	self.assertEqual(top5[4], 'fedoratipper69')
    	self.assertEqual(top5[5], 'thepickleking')



unittest.main()