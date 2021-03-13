import pickle
import os.path
from datetime import date
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from AutoBirthdayWish import sendTextMessage
from model import Person

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

def main():
    currentdate=date.today();

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
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    # Call the People API
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=500,
        personFields='names,birthdays,phoneNumbers,biographies').execute()
    connections = results.get('connections', [])
    birthday_people=[]

    #list [1,2,3,4] - unique
    #Dict[{"name":1,"rollno":2},{"name":2,"rollno:3"}]
    #set[1,2,3,4,4,] -- can contain same values

    for person in connections:

        names = person.get('names', [])
        birthdays = person.get('birthdays',[])
        notes = person.get('biographies',[])

        if names and birthdays:
            wish=None
            name = names[0].get('displayName')
            birthday = birthdays[0].get('date')
            if (currentdate.day == birthday['day'] and currentdate.month == birthday['month']):
                if notes:
                    wish=notes[0].get('value')
                birthday_person=Person(name,wish)
                birthday_people.append(birthday_person)
    if birthday_people:
        sendTextMessage(birthday_people)
    else:
        print('no birthdays today!')

if __name__ == '__main__':
    main()