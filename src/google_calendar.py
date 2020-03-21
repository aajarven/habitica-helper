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
    credential_path = "secrets/googletoken.pickle"
    client_secret_path = "secrets/googlecredentials.json"
    date_format = "%Y-%m-%d"
    credentials = None

    def __init__(self):
        """
        Ensure that we have credentials for accessing the calendar.
        """
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

    def insert_event(self, calendar_id, summary, description, date):
        """
        Insert a new event to the calendar.

        TODO write a new birthday addition method
        TODO how we determine if an event already exists? login name?
        TODO how we determine what to write in? Don't give summary and
             description but an user dict instead?
        PLAN write general google calendar things here, make some other class
             for doing the thinking

        :calendar_id: Unique identifier of the calendar
        :summary: Title of the event
        :description: Possibly longer description of the event
        :date: Date for which the event is inserted.
        """  # TODO
        new_event = {
            "summary": summary,
            "description": description,
            "start": {
                "date": date.strftime(self.date_format),
                },
            "end": {
                "date": date.strftime(self.date_format),
                },
            }
        self.service.events().insert(calendarId=calendar_id,
                                     body=new_event).execute()
