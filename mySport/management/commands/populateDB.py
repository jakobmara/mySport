from django.core.management.base import BaseCommand, CommandError
import requests
from mySport.models import Team, Player, PlayerSeasonStats, TeamSeasonStats
from PandasBasketball import pandasbasketball as pb
from PandasBasketball import stats as s
import pandas as pd
from requests import get
from bs4 import BeautifulSoup, NavigableString
from PandasBasketball.errors import TableNonExistent, StatusCode404
import csv

BASE_URL = "https://www.basketball-reference.com"


class Command(BaseCommand):
    TEAM_TO_ABRV = {'LAL':"Los Angeles Lakers","GSW":"Golden State Warriors","BOS":"Boston Celtics","NYK":"New York Knicks","TOR":"Toronto Raptors","UTA":"Utah Jazz","CHA":"Charlotte Hornets",\
    "DAL":"Dallas Mavericks","HOU":"Houston Rockets","LAC":"Los Angeles Clipers","SAS":"San Antonio Spurs","POR":"Portland Trailblazers","DEN":"Denver Nuggets","CHI":"Chicago Bulls","PHO":"Phoenix Suns","MIL":"Milwaukee Bucks", \
    "MIA":"Miami Heat","WAS":"Washington Wizards", "MIN":"Minnesota Timberwolves","ATL":"Atlanta Hawks","CLE":"Cleveland Caviliers","OKC":"Oklahoma City Thunder", "IND":"Indiana Pacers","SAC":"Sacramento Kings",\
    "DET":"Detroit Pistons","MEM":"Memphis Grizzlies","ORL":"Orlando Magic", "PHI":"Philadelphia 76ers", "NJN":"New Jersey Nets", "NOH": "New Orleans Hornets", "NOP":"New Orleans Pelicans", "BRK":"Brooklyn Nets", "CIN": "Cincinnati Royals", "SEA": "Seattle Supersonics", \
    "BUF":"Buffalo Braves", "VAN": "Vancouver Grizzlies", "SYR": "Syracuse Nationals", \
    "WSB": "Washington Bullets","SDR":"San Diego Rockets", \
    "CHH": "Charlotte Hornets", "NOJ":"New Orleans Jazz", "KCO":"Kansas City Kings", \
    "SFW":"San Francisco Warriors", "KCK":"Kansas City Kings", "NOK": "New Orleans/Oklahoma City", "SDC":"San Diego Clippers",\
    "STL":"St. Louis Hawks", "NYN": "New York Nets","PHW":"Philadelphia Warriors","FTW":"Fort Wayne Pistons","BLB":"Baltimore Bullets",\
    "BAL":"Baltimore Bullets", "CHO":"Charlotte Hornets","INO":"Indianapolis Olympians", "CHS":"Chicago Stags","DNN":"Denver Nuggets","WSC":"Washington Capitols",\
    "MNL":"Minneapolis Lakers", "TRI":"Tri-Cities Blackhawks","MLH":"Milwaukee Hawks","CHP":"Chicago Packers","CHZ":"Chicago Zephyrs", "AND":"Anderson Packers", "WAT": "Waterloo Hawks",\
        "SHE":"Sheboygan Red Skins", "ROC":"Rochester Royals", "CAP":"Capital Bullets", "STB":"St. Louis Bombers"
    }
    def handle(self, *args, **options):
        self.populateTeams()
        self.populatePlayerTables()

    def populateTeams(self):
        count = 1
        #empties the Table
        Team.objects.all().delete()
        used_keys = []
        for key in self.TEAM_TO_ABRV:
            if self.TEAM_TO_ABRV[key] not in used_keys:
                newT = Team(team_name=self.TEAM_TO_ABRV[key], short_form=key)
                used_keys.append(self.TEAM_TO_ABRV[key])

                print(f"KEY: {key}")

                url = BASE_URL + f"/teams/{key}/"
                r = requests.get(url)

                #teamInfo = pb.get_team(key)
                teamInfo = self.team_stats(r,key)
                if teamInfo.empty != True:
                    newT.logo = teamInfo['logo'].values[0]
                newT.save()

                for season_num in range(len(teamInfo)):
                    season = teamInfo.iloc[season_num]
                    tSeason = season.get('Season') or 'NA'
                    tWins = season.get('W') or None
                    tLoss = season.get('L') or None
                    tPace = season.get('Pace') or None
                    tORTG = season.get('ORtg') or None
                    tDRTG = season.get("DRtg") or None
                    tCoaches = season.get("Coaches") or 'NA'
                    tPlayoffs = season.get('Playoffs') or 'NA'
                    newTS = TeamSeasonStats(team_id=newT.id,season = tSeason, wins = tWins, losses=tLoss, pace=tPace,offensive_rating=tORTG,defensive_rating=tDRTG,coach=tCoaches,playoffs=tPlayoffs)
                    newTS.save()

            count+=1
    
    def getTeamID(self,name):
        q = Team.objects.filter(team_name=self.TEAM_TO_ABRV[name])
        
        if len(q) == 0:
            #Invalid Query
            return -1
        else:
            return q[0].id

    def populatePlayerTables(self):
        with open("./players.txt",encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            line_count = 0
            Player.objects.all().delete()
            PlayerSeasonStats.objects.all().delete()

            for row in csv_reader:
                if line_count == 0:
                    print(f'columns: {", ".join(row)}')
                    line_count= 1
                else:
                    playerInfo = row[0].split("\\")
                    player_names = playerInfo[0].split()
                    player_code = playerInfo[1]
                    #player_image = self.getPlayerImg(player_code)
                    newP = Player(first_name=player_names[0],last_name=player_names[1].rstrip("*"),full_name =playerInfo[0].rstrip("*"))

                    seasons_in_nba=0
                    
                    url = BASE_URL + f"/players/{player_code[0]}/{player_code}.html"
                    r = requests.get(url)
                    if r.status_code == 404:
                        raise StatusCode404
                    else:
                        playerStats = self.get_player_stats(r,"per_game", False, True)
                        if playerStats.empty == False:

                            if (playerStats['image'].values[0] != None):
                                newP.picture = playerStats['image'].values[0]
                            newP.save()
                    if playerStats.empty == False:
                        for season_num in range(len(playerStats)):
                            season = playerStats.iloc[season_num]
                            playerID = newP.id
                            #currently ignores total records for players
                            if season[1] != "TOT":
                                print(f"player: {newP.first_name} {newP.last_name}")
                                if season.get("Lg") == 'NBA':
                                    seasons_in_nba += 1
                                    #Had to add or -1 cuz .get()'s default wouldn't trigger if it returned an empty string
                                    teamID = self.getTeamID(season[1])
                                    playerPos = season.get('Pos') or "NA"
                                    playerFouls = season.get('PF') or None
                                    playerSeason = season.name
                                    playerPPG = season.get('PTS') or None
                                    playerAPG = season.get("AST") or None
                                    playerORB = season.get('ORB') or None
                                    playerTRB = season.get('TRB') or None
                                    player3p = season.get('3P') or None
                                    player3PA = season.get('3PA') or None
                                    player3Percentage = season.get("3P%") or None
                                    player2p = season.get('2P') or None
                                    player2PA = season.get('2PA') or None
                                    player2Percentage = season.get("2P%") or None
                                    #assuming playerAge is always given
                                    playerAge = season.get("Age")
                                    playerBlock = season.get("BLK") or None
                                    playerFG = season.get("FG") or None
                                    playerFGA = season.get("FGA") or None
                                    playerFGPercentage = season.get("FG%") or None
                                    playerFT = season.get("FT") or None
                                    playerFTA = season.get("FTA") or None
                                    playerFTPercentage = season.get("FT%") or None
                                    playerGP = season.get("G") or None
                                    playerMPG = season.get("MP") or None
                                    playerSPG = season.get("STL") or None
                                    playerTOV = season.get("TOV") or None
                                    newPs = PlayerSeasonStats(team_name=season.get('Tm'), position=playerPos,PF=playerFouls,season=playerSeason,PPG=playerPPG,APG=playerAPG,ORB=playerORB,TRB=playerTRB,three_points_made=player3p,three_points_attempted= player3PA,three_point_percentage=player3Percentage ,two_points_made=player2p ,two_points_attempted= player2PA,two_point_percentage= player2Percentage,Age=playerAge,BPG=playerBlock ,FG=playerFG,FGA=playerFGA,FG_percentage=playerFGPercentage ,FT=playerFT ,FTA=playerFTA ,FT_percentage= playerFTPercentage,GP=playerGP,MPG=playerMPG,SPG= playerSPG,TOV=playerTOV ,player_id=playerID,team_id=teamID)
                                    newPs.save()
                        if seasons_in_nba == 0:
                            newP.delete()
                    

                    line_count += 1

    def get_playerInfo(self, code):
        
        return pb.get_player(code,"per_game",False,True)

    def populate_team_info(self):
        return 'hi'

    def team_stats(self, request, team):
        data = []
        
        soup = BeautifulSoup(request.text, "html.parser")
        table = soup.find("table", id=team)
        if table == None:
            return pd.DataFrame(data)
        df = s.get_data_master(table, "team")

        newSoup = BeautifulSoup(request.content, 'html.parser')
        #outerDiv = newSoup.find("div", {"class":"media-item logo"})
        outerDiv = newSoup.find("div", {"id":"info"})

        if outerDiv == None:
            logo = None
        else:
            myDivs = outerDiv.find("img", {"class":"teamlogo"})
            if myDivs == None:
                logo = None
            else:
                logo = myDivs['src']
        
        
        del df["\xa0"]

        df['logo'] = logo

        return df




    #modified function from pandasBasketball Library
    #I modified it so that I wouldn't need to make 2 seperate API requests 1 for player image 1 for player stats now this function does both
    #this will reduce runtime for DB population
    def get_player_stats(self,request,stat,is_numeric=False,s_index=False):
        supported_tables = ["totals", "per_minute", "per_poss", "advanced",
                            "playoffs_per_game", "playoffs_totals", "playoffs_per_minute",
                            "playoffs_per_poss", "playoffs_advanced"]

        if stat == "per_game":
            soup = BeautifulSoup(request.text, "html.parser")
            table = soup.find("table", id="per_game")
        elif stat in supported_tables:
            soup = BeautifulSoup(request.text, "html.parser")
            comment_table = soup.find(text=lambda x: isinstance(x, NavigableString) and stat in x)
            soup = BeautifulSoup(comment_table, "html.parser")
            table = soup.find("table", id=stat)
        else:
            raise TableNonExistent

        # Get the whole data frame
        if table == None:
            print("NO TABLE FOUND")
            data = []

            return pd.DataFrame(data)
        df = s.get_data_master(table, "player")


        

        if stat == "per_poss" or stat == "playoffs_per_poss":
            del df[None]
        elif stat == "advanced" or stat == "playoffs_advanced":
            del df["\xa0"]
        
        if is_numeric:
            df[df.columns] = df[df.columns].apply(pd.to_numeric, errors="ignore")
        if s_index:
            df.set_index("Season", inplace=True)

        #created this so I don't need to make 2 seperate get requests for every player
        soup = BeautifulSoup(request.content, 'html.parser')
        outerDiv = soup.find("div", {"id":"meta"})
        if outerDiv == None:
            image = None
        else:
            myDivs = outerDiv.find("img", {"itemscope":"image"})
            if myDivs == None:
                image = None
            else:
                image = myDivs['src']
        df['image'] = image
        return df