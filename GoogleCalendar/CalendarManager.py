from __future__ import print_function
import datetime
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class CalendarManager:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def _login(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    def upcomingEvents(self, max=30):
        service = self._login()

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=max, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events, service

    def updateCalendar(self, HomeBase, name):
        HomeBaseEvents = HomeBase.PersonManager.getEventsByName(name)
        upcomingEvents, service = self.upcomingEvents()

        newEvents = sortEvents(upcomingEvents, HomeBaseEvents)
        for e in newEvents:
            service.events().insert(calendarId='primary', body=e.event).execute()

        if len(newEvents) == 0:
            print("No new events found")
        else:
            print(str(len(newEvents)) + " Google events added successfully!")
        return

    def clear(self):
        toDel, service = self.upcomingEvents(80)
        print("Events Pending Death: " + str(len(toDel)))
        for event in toDel:
            if event['description'] == 'Automated Event - David Castillo':
                service.events().delete(calendarId="primary", eventId=event['id']).execute()

        print("Calendar Cleared!")


def sortEvents(upComingEvents, HomeBaseEvents):
    retVal = []

    for new in HomeBaseEvents:
        addMe = True
        for curr in upComingEvents:
            if curr['start'].get('dateTime', curr['start'].get('date'))[0:-6] == \
                    new.event['start'].get('dateTime', new.event['start'].get('date')):
                addMe = False
                break
        if addMe:
            retVal.append(new)
    return retVal



