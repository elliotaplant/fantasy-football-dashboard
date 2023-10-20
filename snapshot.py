from espn_api.football import League
from game_time_remaining import game_time_remaining
from config import LEAGUE_ID, ESPN_S2, SWID
from storage import get_last_element, append_to_redis


def generate_snapshot():
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

    return snapshot


def store_snapshot(snapshot):
    base_key = "fantasy-dashboard"
    for matchup in snapshot:
        matchup_key = f"{matchup['home']['team_id']}-{matchup['away']['team_id']}"
        for team in ["home", "away"]:
            team_key = ':'.join([base_key, matchup_key, team])
            last_element = get_last_element(team_key)

            if not last_element or last_element['time_remaining'] != matchup[team]['time_remaining']:
                new_entry = {
                    'time_remaining': matchup[team]['time_remaining'],
                    'score': matchup[team]['score']
                }
                append_to_redis(team_key, new_entry)
