import json
import csv
from PandasBasketball import pandasbasketball as pb
import pandas as pd
pd.set_option('display.max_columns',None)

TEAM_TO_ABRV = {'LAL':"Los Angeles Lakers","GSW":"Golden State Warriors","BRK":"Brooklyn Nets","BOS":"Boston Celtics","NYK":"New York Knicks","TOR":"Toronto Raptors","UTA":"Utah Jazz","CHA":"Charlotte Hornets",\
    "DAL":"Dallas Mavericks","HOU":"Houston Rockets","LAC":"Los Angeles Clipers","SAS":"San Antonio Spurs","POR":"Portland Trailblazers","DEN":"Denver Nuggets","CHI":"Chicago Bulls","PHO":"Phoenix Suns","MIL":"Milwaukee Bucks", \
    "MIA":"Miami Heat","NOP":"New Orleans Pelicans","WAS":"Washington Wizards", "MIN":"Minnesota Timberwolves","ATL":"Atlanta Hawks","CLE":"Cleveland Caviliers","OKC":"Oklahoma City Thunder", "IND":"Indiana Pacers","SAC":"Sacramento Kings",\
    "DET":"Detroit Pistons","MEM":"Memphis Grizzlies","ORL":"Orlando Magic", "PHI":"Philadelphia 76ers"}
'''
#this creates a JSON file to populate the DB table: mySport_team
data = []
count = 1
for key in TEAM_TO_ABRV:
    data.append({
        "model":"mySport.Team",
        "pk": count,
        "fields": {
            'team_name': TEAM_TO_ABRV[key]
        }
    })
    count+=1

with open("teams.json","w") as outfile:
    json.dump(data,outfile)
# python manage.py loaddata teams.json
'''


#print(constants.TEAM_TO_TEAM_ABBR)
#fg = pb.get_player("jamesle01","per-game",False,True)
playersData = []
playerSeasons = []
'''
with open("players.txt",encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'columns: {", ".join(row)}')
            line_count= 1
        else:
            playerInfo = row[0].split("\\")
            player_names = playerInfo[0].split()
            player_code = playerInfo[1]
            playersData.append({
                "model":"mySport.Player",
                "pk": line_count,
                "fields":{
                    "first_name": player_names[0],
                    "last_name": player_names[1]
                }
            })
            
            #playerStats = pb.get_player(player_code,"per_game",False,True)
            
            playerSeasons.append({
                "model":"mySport.models.PlayerSeasonStats",
                "pk": line_count,
                "fields":{
                    "first_name": player_name.split[0],
                    "last_name": player_name.split[1]
                }
            })
            

            line_count += 1
            # I should write to player.json and playerSeason.json in this loop for runtime reasons
            print(f"player: {player_names} played until: {row[2]}")
with open("players.json","w") as outfile:
    json.dump(playersData,outfile)       
'''

#STILL NEED TO GET PLAYER SEASON




with open("playerSeasons.json","w") as outfile2:
    json.dump(playerSeasons,outfile2)
code = pb.generate_code("Alaa Abdelnaby")
print(code)
df = pb.get_player(code, "per_game",False,True)
#df = pb.get_player(pb.generate_code("Zaid Abdul-Aziz"), "per_game",False,True)
#print(df.head())
print(df['image'].values[0])
#newDf = pb.get_team("TOR")
#print(newDf.head())
#a = newDf.iloc[1]
#print(df.head())
#a = df.iloc[0]
#print(a.name)
#print(a.STL)

#0=age,1=team,3=position,4=games played,5=games started,6=minutes played,7=fg,8=fga,9=fg%,10=3pm,11=3pa,12=3p%,13=2pm,14=2pa,15= 2p%, 17=ft,18=fta,19=FT%,20=ORB,21=DRB,22=TRB,23=AST,24=STL,25=BLK,26=TOV,27=PF,28=pts
#






#if adding items to list then writing them to file is too long cut out the middle man and write directly to file    

    
