import requests


def _construct_map(response_json):
    time_remaining_map = {}

    # Iterate through each event in the response
    for event in response_json['events']:

        # Get necessary information from the event
        status = event['status']
        competition_id = event['competitionId']
        teams = [c['abbreviation'] for c in event['competitors']]
        date = event['date']

        # If there's a 'lastPlay' key in the event, get the period and clock

        # Calculate time remaining based on the status and other info
        if status == "pre":
            time_remaining = 60 * 60
        elif status == "in":
            if 'lastPlay' in event:
                period = event['lastPlay']['period']
                clock = event['lastPlay']['clock']

            if period < 4:
                time_remaining = (4 - period) * 15 * 60 + clock
            else:
                time_remaining = clock
        else:
            time_remaining = 0

        # Add the result to the map
        time_remaining_map[competition_id] = (date, int(time_remaining))
        for team in teams:
            time_remaining_map[team] = int(time_remaining)

    # Patch for Oakland's move to LV
    time_remaining_map['OAK'] = time_remaining_map.get('LV', None)

    return time_remaining_map


def game_time_remaining(start_date, end_date):
    try:
        url = f"https://site.api.espn.com/apis/fantasy/v2/games/ffl/games?useMap=true&dates={start_date}-{end_date}"
        # Perform a GET request to fetch the data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Load response content as JSON
        response_json = response.json()

        # Create and return the map using the get_time_remaining_map function
        return _construct_map(response_json)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the data: {e}")
        return None


# Usage example:
# time_remaining_map = fetch_and_create_map("20231012", "20231017")
# print(time_remaining_map)

UPDATED_PRO_TEAM_MAP = {
    0: 'None',
    1: 'ATL',
    2: 'BUF',
    3: 'CHI',
    4: 'CIN',
    5: 'CLE',
    6: 'DAL',
    7: 'DEN',
    8: 'DET',
    9: 'GB',
    10: 'TEN',
    11: 'IND',
    12: 'KC',
    13: 'OAK',
    14: 'LAR',
    15: 'MIA',
    16: 'MIN',
    17: 'NE',
    18: 'NO',
    19: 'NYG',
    20: 'NYJ',
    21: 'PHI',
    22: 'ARI',
    23: 'PIT',
    24: 'LAC',
    25: 'SF',
    26: 'SEA',
    27: 'TB',
    28: 'WSH',
    29: 'CAR',
    30: 'JAX',
    33: 'BAL',
    34: 'HOU'
}
