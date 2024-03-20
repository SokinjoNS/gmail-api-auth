from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import logging

# Define the Gmail API scope.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail_api():
    creds = None
    # Attempt to load existing credentials from 'token.pickle'.
    try:
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
    except Exception as e:
        logging.error(f"Error loading token.pickle: {e}")
        # Set creds to None if there's an error loading it.
        creds = None

    # Check if credentials are valid, and refresh or generate them if necessary.
    if not creds or not creds.valid:
        try:
            # Refresh credentials if they are expired and a refresh token is available.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Generate new credentials if no valid credentials are found.
                if not os.path.exists('credentials.json'):
                    logging.error('credentials.json file does not exist.')
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run.
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        except Exception as e:
            logging.error(f"Failed to authenticate with Gmail API: {e}")
            # Return None if authentication fails.
            return None

    # Return the credentials.
    return creds
