from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=100)
    short_form = models.CharField(max_length=4)
    logo = models.CharField(max_length=150,default="https://theundefeated.com/wp-content/uploads/2017/06/nbalogo.jpg?w=700")
    def __str__(self):
        return "id: " + str(self.id) + " name: " + self.team_name

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, default='NA')
    picture = models.CharField(max_length = 150, default="https://i.imgur.com/fFDjSjA.jpg")
    def __str__(self):
        return self.first_name + " " + self.last_name

class TeamSeasonStats(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    season = models.CharField(default='NA',max_length=10)
    wins = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    pace = models.FloatField(null=True)
    offensive_rating = models.FloatField(null=True)
    defensive_rating = models.FloatField(null=True)
    coach = models.CharField(max_length=100)
    playoffs = models.CharField(max_length=100, default='NA')
    def __str__(self):
        return "wins: " + str(self.wins) + ", losses: " + str(self.losses) + "\nCoach: " + self.coach 

class PlayerSeasonStats(models.Model):
    #I want this to refer to player (but have multiple instances of player_ID)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    #I want this to refer to the team they were playing for for that current season
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    
    #stats for the player during the season
    season = models.CharField(default='NA',max_length=10)
    Age = models.IntegerField(default=19)
    position = models.CharField(default='NA',max_length=10)
    PPG = models.FloatField(null=True)
    APG = models.FloatField(null=True)
    ORB = models.FloatField(null=True)
    TRB = models.FloatField(null=True)
    SPG = models.FloatField(null=True)
    BPG = models.FloatField(null=True)
    TOV = models.FloatField(null=True)
    GP = models.IntegerField(null=True)
    MPG = models.FloatField(null=True)
    FG = models.FloatField(null=True)
    FGA = models.FloatField(null=True)
    FG_percentage = models.FloatField(null=True)
    team_name = models.CharField(max_length = 4,default="NAN")
    three_points_made = models.FloatField(null=True)
    three_points_attempted = models.FloatField(null=True)
    three_point_percentage = models.FloatField(null=True)
    two_points_made = models.FloatField(null=True)
    two_points_attempted = models.FloatField(null=True)
    two_point_percentage = models.FloatField(null=True)
    FT = models.FloatField(null=True)
    FTA = models.FloatField(null=True)
    FT_percentage = models.FloatField(null=True)
    PF = models.FloatField(null=True)
    def __str__(self) -> str:
        #see if you can access the object references
        return "season: " + self.season + " player: " + str(self.player)

class teamovr(models.Model):
    id = models.BigIntegerField(primary_key=True)
    team = models.ForeignKey(Team,on_delete=models.DO_NOTHING)
    winningSeasons = models.IntegerField()
    losingSeasons = models.IntegerField()
    championshipsWon = models.IntegerField()
    championshipApps = models.IntegerField()
    yearsInLeague = models.IntegerField()
class Meta:
    managed = False
    db_table = "mySport_teamovr"

class playerovr(models.Model):
    id = models.BigIntegerField(primary_key=True)
    player = models.ForeignKey(Player,on_delete=models.DO_NOTHING)
    averageAssits = models.IntegerField()
    averageTOV = models.IntegerField()
    averageSteals = models.IntegerField()
    averageBlocks = models.IntegerField()
    averagePoints = models.IntegerField()
class Meta:
    managed = False
    db_table = "mySport_playerovr"