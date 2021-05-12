from django import template
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.template import loader


from .models import Player, PlayerSeasonStats, Team, TeamSeasonStats, teamovr, playerovr



def index(request):
    highest_season_list = PlayerSeasonStats.objects.order_by('-PPG')[:5]
    highest_assist_list = PlayerSeasonStats.objects.order_by('-APG')[:5]
    #I think i can include more information (key value array in context)
    context={
        'highest_season_list': highest_season_list,
        'highest_assisted_list': highest_assist_list
    }
    return render(request,'mySport/index.html',context)


#this is for URL
def detail(request, player_id):
    #check if request.get('searchQuery') == player
    player = get_object_or_404(Player, pk=player_id)
    playerAgg = playerovr.objects.filter(player_id=player_id)[0]
    print("IN DETAIL")
    return render(request, 'mySport/player_detail.html', {'player': player, 'playerAgg': playerAgg})

#this is for homepage searches
def searchResults(request):
    searchQ = request.GET.get('searchQuery')
    if request.GET.get('selectPicker') == 'Players':

        players = Player.objects.filter(full_name__icontains=searchQ)[:5]
        if len(players) == 1:
            playerAgg = playerovr.objects.filter(player_id=players[0].id)
            return render(request,'mySport/player_detail.html', {'player' : players[0], 'playerAgg': playerAgg[0]})
        elif(len(players) == 0):
            return render(request,'mySport/search_suggestion.html', {'error_message': "No results found"})
        else:
            return render(request,'mySport/search_suggestion.html', {'players': players})
    else:
        teams = Team.objects.filter(team_name__icontains=searchQ)[:5]
        if len(teams) == 1:
            teamAgg = teamovr.objects.filter(team_id = teams[0].id)
            return render(request,'mySport/team_detail.html', {'team' : teams[0], 'teamStats': teams[0].teamseasonstats_set.all(), 'teamAgg' : teamAgg[0]})
        elif len(teams) == 0: 
            return render(request,'mySport/search_suggestion.html', {'error_message': "No results found"})
        else:
            return render(request,'mySport/search_suggestion.html', {'teams': teams})

def teamDetail(request,team_id):
    team = get_object_or_404(Team, pk = team_id)
    teamAgg = teamovr.objects.filter(team_id=team_id)
    if len(teamAgg) == 0:
        return render(request, 'mySport/team_detail.html', {'team':team,'teamStats': team.teamseasonstats_set.all()})
    else:
        return render(request, 'mySport/team_detail.html', {'team':team,'teamStats': team.teamseasonstats_set.all(), 'teamAgg':teamAgg[0]})

