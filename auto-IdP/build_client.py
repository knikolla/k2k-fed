import os

from keystoneclient import session as ksc_session
from keystoneclient.auth.identity import v3
from keystoneclient.v3 import client as keystone_v3

try:
    OS_AUTH_URL = os.environ['OS_AUTH_URL']
    OS_PROJECT_ID = os.environ['OS_PROJECT_ID']
    OS_USER_ID = os.environ['OS_USER_ID']
    OS_PASSWORD = os.environ['OS_PASSWORD']
except KeyError as e:
    raise SystemExit('%s environment variable not set.' % e)

def client_for_admin_user():
    auth = v3.Password(auth_url=OS_AUTH_URL,
                       user_id=OS_USER_ID,
                       password=OS_PASSWORD,
                       project_id=OS_PROJECT_ID)
    session = ksc_session.Session(auth=auth)
    return keystone_v3.Client(session=session)

# Used to execute all admin actions
client = client_for_admin_user()
print client.users.list()
