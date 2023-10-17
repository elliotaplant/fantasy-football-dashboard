import os
from pprint import pprint
from espn_api.football import League
from game_time_remaining import game_time_remaining
from datetime import datetime


# Getting values from environment variables
LEAGUE_ID = os.environ.get('LEAGUE_ID')
ESPN_S2 = os.environ.get('ESPN_S2')
SWID = os.environ.get('SWID')

league = League(league_id=int(LEAGUE_ID), year=2023,
                espn_s2=ESPN_S2, swid=SWID)


# Get week with date
current_week = 6
week_start_date = '20231012'
week_end_date = '20231017'

box_scores = league.box_scores(current_week)
time_remaining_map = game_time_remaining(week_start_date, week_end_date)

print('time_remaining_map', time_remaining_map)
live_positions = {'QB', 'RB', 'WR', 'RB/WR/TE', 'TE', 'D/ST', 'K'}


snapshot = []
for matchup in box_scores:
    if 'Kirk' in matchup.away_team.team_name:
        print([(player, player.slot_position)
              for player in matchup.away_lineup])
    home_time_remaining = 0
    home_current_score = 0
    home_live_players = [
        player for player in matchup.home_lineup if player.slot_position in live_positions]
    for player in home_live_players:
        time_remaining = time_remaining_map.get(player.proTeam, 0)
        home_time_remaining += time_remaining
        home_current_score += player.points

    away_time_remaining = 0
    away_current_score = 0
    away_live_players = [
        player for player in matchup.away_lineup if player.slot_position in live_positions]
    for player in away_live_players:
        time_remaining = time_remaining_map.get(player.proTeam, 0)
        away_time_remaining += time_remaining
        away_current_score += player.points

    snapshot.append({
        "home": {
            "name": matchup.home_team.team_name,
            "time_remaining": home_time_remaining,
            "score": home_current_score
        },
        "away": {
            "name": matchup.away_team.team_name,
            "time_remaining": away_time_remaining,
            "score": away_current_score
        }
    })

print(datetime.now().isoformat(), snapshot)
# Append to reddis key fantasy_dashboard:{week} [timestamp, snapshot]
# Or maybe  fantasy_dashboard:{week} [{team: [{ time_remaining, points }]}]
# https://site.api.espn.com/apis/fantasy/v2/games/ffl/games?useMap=true&dates=20231012-20231017&pbpOnly=true
