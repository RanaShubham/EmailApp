from decouple import config


SCOPES = config('SCOPES', default='', cast=str).split(',')
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
CREDENTIALS_DATA = config('CREDENTIALS', default='{}', cast=str)