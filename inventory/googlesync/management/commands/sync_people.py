# pip install --upgrade google-api-python-client google-auth google-auth-httplib2
from google.oauth2 import service_account
import googleapiclient.discovery
from googlesync.models import *

#from exceptions import ConfigNotFound

google_config = GoogleConfig.objects.first()

# if not google_config:
#    raise ConfigNotFound(config_name="Google Sync")

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly']
SERVICE_ACCOUNT_FILE = 'service_account_credentials.json'

# Service account will impersonate this user. Must have proper admin privileges in G Suite.
DELEGATE = 'matt.henry.admin@owensboro.kyschools.us'
# Service account wants to access data from this.
TARGET = 'owensboro.kyschools.us'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
credentials_delegated = credentials.with_subject(DELEGATE)

service = googleapiclient.discovery.build(
    'admin', 'directory_v1', credentials=credentials_delegated)
response = service.users().list(domain=TARGET).execute()

print(response)
