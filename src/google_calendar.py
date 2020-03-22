"""
Functionality for interacting with Google calendar.
"""
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleCalendar():
    """
    TODO
    """  # TODO
    credential_path = "conf/secrets/googletoken.pickle"
    client_secret_path = "conf/secrets/googlecredentials.json"
    credentials = None

    def __init__(self, calendar_id):
        """
        Ensure that we have credentials for accessing the calendar.
        """
        self.calendar_id = calendar_id

        if os.path.exists(self.credential_path):
            with open(self.credential_path, "rb") as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if (self.credentials and self.credentials.expired
                    and self.credentials.refresh_token):
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_path,
                    ["https://www.googleapis.com/auth/calendar"])
                self.credentials = flow.run_local_server(port=0)

            with open(self.credential_path, "wb") as token:
                pickle.dump(self.credentials, token)
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def _date_timestamp(self, date):
        """
        Return the string representation of a date, usable by Google calendar.
        """
        return date.strftime("%Y-%m-%d")

    def _datetime_timestamp(self, date):
        """
        Return RFC3339 representation of the midnight starting the date.
        """
        return "{}-{}-{}T00:00:00Z".format(date.year, date.month, date.day)


    def insert_fullday_event(self, summary, description, date):
        """
        Insert a new event to the calendar.

        :summary: Title of the event
        :description: Possibly longer description of the event
        :date: Date for which the event is inserted.
        """
        new_event = {
            "summary": summary,
            "description": description,
            "start": {
                "date": self._date_timestamp(date),
                },
            "end": {
                "date": self._date_timestamp(date),
                },
            }
        self.service.events().insert(calendarId=self.calendar_id,
                                     body=new_event).execute()

    def events_for_date(self, date):
        """
        Return a list of all events on a specific date.

        :date: Date for which the events are listed
        :returns: A list of event resources
        """
        next_page = None
        events = []
        while True:
            new_events = self.service.events().list(
                calendarId=self.calendar_id,
                pageToken=next_page,
                timeMin=self._datetime_timestamp(date),
                timeMax=self._datetime_timestamp(date + datetime.timedelta(days=1)),
                ).execute()
            events = events + new_events['items']

            next_page = new_events.get('nextPageToken')
            if not next_page:
                return events
