import os
import json
import redis
from espn_api.football import League
from game_time_remaining import game_time_remaining


# Getting values from environment variables
LEAGUE_ID = os.environ.get('LEAGUE_ID')
ESPN_S2 = os.environ.get('ESPN_S2')
SWID = os.environ.get('SWID')
REDIS_URL = os.environ.get('REDIS_URL')

# Setting up the Redis client
redis_client = redis.Redis.from_url(REDIS_URL)


league = League(league_id=int(LEAGUE_ID), year=2023,
                espn_s2=ESPN_S2, swid=SWID)


# Get week with date
current_week = 7
week_start_date = '20231019'
week_end_date = '20231026'

box_scores = league.box_scores(current_week)
time_remaining_map = game_time_remaining(week_start_date, week_end_date)

live_positions = {'QB', 'RB', 'WR', 'RB/WR/TE', 'TE', 'D/ST', 'K'}


snapshot = []
for matchup in box_scores:
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
            "team_id": matchup.home_team.team_id,
            "name": matchup.home_team.team_name,
            "time_remaining": home_time_remaining,
            "score": home_current_score
        },
        "away": {
            "team_id": matchup.away_team.team_id,
            "name": matchup.away_team.team_name,
            "time_remaining": away_time_remaining,
            "score": away_current_score
        }
    })

base_key = "fantasy-dashboard"
for matchup in snapshot:
    matchup_key = f"{matchup['home']['team_id']}-{matchup['away']['team_id']}"
    for team in ["home", "away"]:
        team_key = ':'.join([base_key, matchup_key, team])

        # Get last element of list at team_key
        last_element_json = redis_client.lindex(team_key, -1)
        last_element = json.loads(
            last_element_json) if last_element_json else None

        if not last_element or last_element['time_remaining'] != matchup[team]['time_remaining']:
            # Create a new snapshot entry
            new_entry = {
                'time_remaining': matchup[team]['time_remaining'],
                'score': matchup[team]['score']
            }
            # Append the new entry to the list in Redis
            redis_client.rpush(team_key, json.dumps(new_entry))
