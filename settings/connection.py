import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import CREDENTIALS_DATA, CREDENTIALS_FILE, SCOPES, TOKEN_FILE



class GoogleClient():
  def __init__(self):
    self.__credentials:Credentials = None
    self.__generate_credentials()

  def __make_credentials_file(self):
    """Make credentials file from .env
    """
    if not os.path.exists(CREDENTIALS_FILE):
      with open(CREDENTIALS_FILE, "w") as f:
          f.write(CREDENTIALS_DATA)

  def __make_token_file(self):
    """Save the credentials for the next run
    """
    with open(TOKEN_FILE, "w") as token:
      token.write(self.__credentials.to_json())

  def __generate_credentials(self):
    self.__make_credentials_file()
    if os.path.exists(TOKEN_FILE):
      self.__credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not self.__credentials or not self.__credentials.valid:
      if self.__credentials and self.__credentials.expired and self.__credentials.refresh_token:
        self.__credentials.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, SCOPES
        )
        self.__credentials = flow.run_local_server(port=0)
      self.__make_token_file()

  def get_resource(self):
    """Return a resource for interacting with google API
    """
    try:
      service = build("gmail", "v1", credentials=self.__credentials)
    except HttpError as error:
      print(f"An error occurred: {error}")
    else:
      return service
    

if __name__ == "__main__":
  client = GoogleClient()
  resource = client.get_resource()
  print("----")
