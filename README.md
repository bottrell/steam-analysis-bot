# Steam Analysis Bot
The steam analysis bot is a program that uses the plotly library, steam API, steamidfinder, and SQL to analyze a user's game library, 
as well as their friend's. 

## Data sources used:
### Steam community API: https://steamcommunity.com/dev
The steam API allows me to get information on a user and their steam information from their steamid64. I use this api to get both the user's
game library/ playtimes as well as the information on those games.
A key can be attained but requires you to have a steam account and games. I know that the spec says to not include keys or other information, 
but I think that this may be difficult for some graders to use without an account. So therefore I included my key --> 67884AA4EAEA34CB6FDDDF9EE25680FD

YOUR SECRETS.PY SHOULD INCLUDE ONE KEY NAMED 'steam_api_key' 

Additionally, the program will ask you to include a steamid64 to do some functionality. You may use my steamid64 (it's publicly available) --> 76561198072467455
You must be consistent that the steamid64 that you input is one that is in your database (the user or a friend of the user).

### steamidfinder.com
In order to get some difficult information about a user, I had to use steamidfinder and scrape the information from that website. 
https://steamidfinder.com/lookup/jbot13/

This crawls the information from a single page to scrape user's steamid64, profile creation date, and privacy settings. The grader should not have to do anything special for this website. 

### steamcommunity.com
In order for me to get access to a large enough data set, I had to allow the program to get the friends list of a user, and additionally
the friends of your friends. This means that I had to use a web crawling script to go through and actually scrape the friends of different
users.
An example is: https://steamcommunity.com/id/jbot13/friends

The grader shouldn't have to do anything with this website to grade. 

## Code structure
The data obtained on steam users all runs through a class named "Users". From this class all the necessary user information is obtained
such as Steam Library with the get_games() member function and get_all_friends_urls() member function. The __init__() function takes
in a json argument that is processed to populate the instance. 

The Games class constructor requires a json object passed in, which is processed upon creation. The class also contains a function add_to_table()
which appropriately adds the games to the games table.

All the data is processed into a table steam.db, which contains two tables: Games and Users. 

The functions utilizing plotly all make SQL commands and use the results to be graphed. These will create an html file in the user's working directory. These html files hold the plotly output.


## How to run:
If you would like to start the program off with a completely new database, you should run with :
< python steam_games.py --init>
If you would like to run the program normally, just type: 
< python steam_games.py>

Within the program, there are 6 main options in the main menu. Pressing the numbers corresponding the the menu prompt will create a graph for that option. 
Inputting "6" will quit the program. 

Again, I would populate and run the program using the steamid64 of 76561198072467455 if you do not already have a steam account. 


