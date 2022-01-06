from datetime import date
import urllib.request
from bs4 import BeautifulSoup


class Game(object):
	def __init__(self):
		self.Date = ''
		self.Location=''
		self.Opponent=''
		self.Played=0
		self.pts=None
		self.fg=None
		self.fga=None
		self.fg3=None
		self.fg3a=None
		self.ft=None
		self.fta=None
		self.orb=None
		self.trb=None
		self.ast=None
		self.stl=None
		self.blk=None
		self.tov=None
		self.pf=None
		self.opp_pts=None
		self.opp_fg=None
		self.opp_fga=None
		self.opp_fg3=None
		self.opp_fg3a=None
		self.opp_ft=None
		self.opp_fta=None
		self.opp_orb=None
		self.opp_trb=None
		self.opp_ast=None
		self.opp_stl=None
		self.opp_blk=None
		self.opp_tov=None
		self.opp_pf=None
		
	def AllGames(self,gamehtml):

		try:
			self.Date = gamehtml.find('td',{'data-stat' : ['date_self']})['csk']
			loc_temp = gamehtml.find('td',{'data-stat' : ['self_location']}).string
			opp = gamehtml.find('td',{'data-stat' : ['opp_name']})
			
			namet = opp.find('a')
			namet = namet['href']
	
			splitname= namet.split('/')
			name = splitname[3]
			self.Opponent = name
			
			if loc_temp is None:
				self.Location = 1
			elif loc_temp == '@':
				self.Location = -1
			else:
				self.Location = 0
				
			
			return 1
			
		except:
			pass

	def PlayedGames(self,gamehtml):

		try:

			tdate = gamehtml.find('td', {'data-stat': ['date_game']}).string
			dstr = tdate.split("-")
			self.Date = date(int(dstr[0]), int(dstr[1]), int(dstr[2]))

			loc_temp = gamehtml.find('td',
									 {'data-stat': ['game_location']}).string

			opp = gamehtml.find('td', {'data-stat': ['opp_id']})
			namet = opp.find('a')
			namet = namet['href']

			splitname = namet.split('/')
			name = splitname[3]

			self.Opponent = name
			
			if loc_temp is None:
				self.Location = 1
			elif loc_temp == '@':
				self.Location = -1
			else:
				self.Location = 0
			

			self.Played=1
			
			self.pts=int(gamehtml.find('td',{'data-stat' : ['pts']}).string)
			self.fg=int(gamehtml.find('td',{'data-stat' : ['fg']}).string)
			self.fga=int(gamehtml.find('td',{'data-stat' : ['fga']}).string)
			self.fg3=int(gamehtml.find('td',{'data-stat' : ['fg3']}).string)
			self.fg3a=int(gamehtml.find('td',{'data-stat' : ['fg3a']}).string)
			self.ft=int(gamehtml.find('td',{'data-stat' : ['ft']}).string)
			self.fta=int(gamehtml.find('td',{'data-stat' : ['fta']}).string)
			self.orb=int(gamehtml.find('td',{'data-stat' : ['orb']}).string)
			self.trb=int(gamehtml.find('td',{'data-stat' : ['trb']}).string)
			self.ast=int(gamehtml.find('td',{'data-stat' : ['ast']}).string)
			self.stl=int(gamehtml.find('td',{'data-stat' : ['stl']}).string)
			self.blk=int(gamehtml.find('td',{'data-stat' : ['blk']}).string)
			self.tov=int(gamehtml.find('td',{'data-stat' : ['tov']}).string)
			self.pf=int(gamehtml.find('td',{'data-stat' : ['pf']}).string)
			
			self.opp_pts=int(gamehtml.find('td',{'data-stat' : ['opp_pts']}).string)
			self.opp_fg=int(gamehtml.find('td',{'data-stat' : ['opp_fg']}).string)
			self.opp_fga=int(gamehtml.find('td',{'data-stat' : ['opp_fga']}).string)
			self.opp_fg3=int(gamehtml.find('td',{'data-stat' : ['opp_fg3']}).string)
			self.opp_fg3a=int(gamehtml.find('td',{'data-stat' : ['opp_fg3a']}).string)
			self.opp_ft=int(gamehtml.find('td',{'data-stat' : ['opp_ft']}).string)
			self.opp_fta=int(gamehtml.find('td',{'data-stat' : ['opp_fta']}).string)
			self.opp_orb=int(gamehtml.find('td',{'data-stat' : ['opp_orb']}).string)
			self.opp_trb=int(gamehtml.find('td',{'data-stat' : ['opp_trb']}).string)
			self.opp_ast=int(gamehtml.find('td',{'data-stat' : ['opp_ast']}).string)
			self.opp_stl=int(gamehtml.find('td',{'data-stat' : ['opp_stl']}).string)
			self.opp_blk=int(gamehtml.find('td',{'data-stat' : ['opp_blk']}).string)
			self.opp_tov=int(gamehtml.find('td',{'data-stat' : ['opp_tov']}).string)
			self.opp_pf=int(gamehtml.find('td',{'data-stat' : ['opp_pf']}).string)
			return 1
		except:
			pass

	def ConvertStates2Rates(self):
		#(FGA – OR) + TO + (Y * FTA) Y = 0.44
		self.possesions = self.fga - self.orb + self.tov + (0.44 * self.fta)
		self.opp_possesions = self.opp_fga - self.opp_orb + self.opp_tov + (
				0.44 * self.opp_fta)

		self.pts_rate  = self.pts/self.possesions
		self.fg_rate = self.fg/self.possesions
		self.fga_rate  = self.fga/self.possesions
		self.fg3_rate = self.fg3/self.possesions
		self.fg3a_rate = self.fg3a/self.possesions
		self.ft_rate = self.ft/self.possesions
		self.fta_rate = self.fta/self.possesions
		self.orb_rate = self.orb/self.possesions
		self.trb_rate = self.trb/self.possesions
		self.ast_rate = self.ast/self.possesions
		self.stl_rate = self.stl/self.possesions
		self.blk_rate = self.blk/self.possesions
		self.tov_rate = self.tov/self.possesions
		self.pf_rate = self.pf/self.possesions

		self.opp_pts_rate  = self.opp_pts/self.opp_possesions
		self.opp_fg_rate = self.opp_fg/self.opp_possesions
		self.opp_fga_rate  = self.opp_fga/self.opp_possesions
		self.opp_fg3_rate = self.opp_fg3/self.opp_possesions
		self.opp_fg3a_rate = self.opp_fg3a/self.opp_possesions
		self.opp_ft_rate = self.opp_ft/self.opp_possesions
		self.opp_fta_rate = self.opp_fta/self.opp_possesions
		self.opp_orb_rate = self.opp_orb/self.opp_possesions
		self.opp_trb_rate = self.opp_trb/self.opp_possesions
		self.opp_ast_rate = self.opp_ast/self.opp_possesions
		self.opp_stl_rate = self.opp_stl/self.opp_possesions
		self.opp_blk_rate = self.opp_blk/self.opp_possesions
		self.opp_tov_rate = self.opp_tov/self.opp_possesions
		self.opp_pf_rate = self.opp_pf/self.opp_possesions

		return

class Player(object):

	def _init_(self):
		Player.Name = []
		Player.Class = []
		Player.Position = []
		Player.Height = []
		Player.Weight = []

class Team(object):

	def __init__(self, school, year):
		self.team_name = school
		self.year = year
		self.Roster = []
		self.Schedule = []
		self.PlayedGames = []

	def getRoster(self):


		urltemplate = 'https://www.sports-reference.com/cbb/schools/' + school + '/' + year + '.html#roster::none'
		openedpage = urllib.request.urlopen(urltemplate)
		teampage = BeautifulSoup(openedpage, "html.parser")

		i = 0
		for rostertable in teampage.findAll('div', {'id': ['all_roster']}):
			for tbodys in rostertable.findAll('tbody'):
				for trs in tbodys.findAll('tr'):
					names = trs.find('th', {'data-stat': ['player']})
					numbers = trs.find('td', {'data-stat': ['number']})
					heights = trs.find('td', {'data-stat': ['height']})
					classes = trs.find('td', {'data-stat': ['class']})
					weights = trs.find('td', {'data-stat': ['weight']})
					positions = trs.find('td', {'data-stat': ['pos']})

					self.Roster.append(Player())
					self.Roster[i].Name = (names['csk'])
					self.Roster[i].Numbers = (numbers.string)
					self.Roster[i].Class = (classes.string)
					self.Roster[i].Position = (positions.string)
					self.Roster[i].Weight = (weights.string)
					self.Roster[i].Height = (heights.string)
					i = i + 1

	def getSchedule(self):


		urltemplate = 'https://www.sports-reference.com/cbb/schools/' + self.team_name + '/' + self.year + '-schedule.html'
		openedpage = urllib.request.urlopen(urltemplate)
		gamespage = BeautifulSoup(openedpage, "html.parser")

		bitable = gamespage.find('table', {'id': ['schedule']})
		gametable = bitable.find('tbody')
		for games in gametable.findAll('tr'):
			Game_temp = Game_lite()
			suc = Game_temp.AllGames(games)
			if suc:
				self.Schedule.append(Game_temp)
			suc = 0

	def getPlayedGames(self):

		urltemplate = 'https://www.sports-reference.com/cbb/schools/' + self.team_name + '/' + self.year + '-gamelogs.html'
		openedpage = urllib.request.urlopen(urltemplate)
		gamespage = BeautifulSoup(openedpage, "html.parser")

		bitable = gamespage.find('table', {'id': ['sgl-basic']})

		try:
			gametable = bitable.find('tbody')

			for games in gametable.findAll('tr'):
				Game_temp = Game()
				suc = Game_temp.PlayedGames(games)

				if suc:
					self.PlayedGames.append(Game_temp)
		except:
			pass


if __name__== '__main__':

	import dill
	import sys
	from tqdm import tqdm

	# Get inputs
	year = '2021'
	save_name = 'Database_20_21'
	save_name = save_name + '.pkl'

	# Setting to allow saving
	sys.setrecursionlimit(50000)

	school_list = []

	# Take data from sports reference
	url_template = 'https://www.sports-reference.com/cbb/seasons/' + year + '-school-stats.html'
	opened_page = urllib.request.urlopen(url_template)
	webpage = BeautifulSoup(opened_page, "html.parser")

	# Parse all D1 schools and get school names
	main_table = webpage.find('table', {'id': ['basic_school_stats']})
	elements = main_table.find('tbody')

	for schools in elements.findAll('td', {'data-stat': ['school_name']}):
		namet = schools.find('a')
		namet = namet['href']
		split_name = namet.split('/')
		name = split_name[3]
		school_list.append(name)

	# Initialize Data structure
	Data = []

	# Loop though every D1 school and fill data structure with played games
	team_counter = 0
	for i, team in enumerate(tqdm(school_list)):
		Data.append(Team(team, year))
		Data[i].getPlayedGames()
		for Game in Data[i].PlayedGames:
			Game.ConvertStates2Rates()

	# Save data structure
	with open(save_name, 'wb') as f:
		dill.dump(Data, f)
		print('')

	print('Data Assembled')

