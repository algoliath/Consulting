from oauth2client import file
from oauth2client import tools
from oauth2client import client

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://mail.google.com/']


def get_credentials(scopes=SCOPES):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth 2.0 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = file.Storage('../tokens.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('../credentials.json', scopes)
        credentials = tools.run_flow(flow, store)

    return credentials
