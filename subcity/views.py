from django.shortcuts import render
from django.http import HttpResponse
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from subcity.models import ScheduleEvent

def index(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    min = datetime.datetime(now.year,now.month,now.day,00,00,00).isoformat() + 'Z'
    max = datetime.datetime(now.year,now.month,now.day,23,59,59).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=min, timeMax=max,
                                        maxResults=24, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    #bad_chars = "Z T '' "
    shows = []

    for event in events[1:]:
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')
        shows.append((start[11:16].strip("Z")) + " - " + (end[11:16].strip("Z") + ": " + (event['summary'].strip(''))))
        #ScheduleEvent(name=event['summary'],time=event['start'].get('dateTime'))

    #show_list = ScheduleEvent.objects.order_by('-time')
    context_dict = {'shows':shows}
    return render(request,'subcity/index.html',context_dict)

def about(request):
    return render(request,'subcity/about.html')

def contact(request):
    return render(request,'subcity/contact.html')

def schedule(request):
    

    return render(request,'subcity/schedule.html')