from datetime import datetime

WEEKS = [
    {"week": 1, "start": "20230907", "end": "20230912"},
    {"week": 2, "start": "20230913", "end": "20230919"},
    {"week": 3, "start": "20230920", "end": "20230926"},
    {"week": 4, "start": "20230927", "end": "20231003"},
    {"week": 5, "start": "20231004", "end": "20231010"},
    {"week": 6, "start": "20231011", "end": "20231017"},
    {"week": 7, "start": "20231018", "end": "20231024"},
    {"week": 8, "start": "20231025", "end": "20231031"},
    {"week": 9, "start": "20231101", "end": "20231107"},
    {"week": 10, "start": "20231108", "end": "20231114"},
    {"week": 11, "start": "20231115", "end": "20231121"},
    {"week": 12, "start": "20231122", "end": "20231128"},
    {"week": 13, "start": "20231129", "end": "20231205"},
    {"week": 14, "start": "20231206", "end": "20231212"},
    {"week": 15, "start": "20231213", "end": "20231219"},
    {"week": 16, "start": "20231220", "end": "20231226"},
    {"week": 17, "start": "20231227", "end": "20230102"},
    {"week": 18, "start": "20230103", "end": "20230112"},
]


def get_current_nfl_week():
    today = datetime.today().strftime('%Y%m%d')

    for week in WEEKS:
        if week['start'] <= today <= week['end']:
            return week['week'], week['start'], week['end']

    raise ValueError('Date out of NFL season range.')

# You can use the function like this:
# week_num, week_start, week_end = get_current_nfl_week()
# print(week_num, week_start, week_end)
