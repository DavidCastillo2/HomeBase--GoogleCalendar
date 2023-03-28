class Event:
    def __init__(self, title, startTime, endTime, location):
        self.event = {
            'summary': title,
            'location': location,
            'description': 'Automated Event - David Castillo',
            'start': {
                'dateTime': startTime.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': endTime.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/New_York',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
