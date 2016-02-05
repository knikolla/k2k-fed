import os, sys

from keystoneclient import session as ksc_session
from keystoneclient.auth.identity import v3
from keystoneclient.v3 import client as keystone_v3

sp_ip = sys.argv[1]

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
                       project_id=OS_PROJECT_ID
    session = ksc_session.Session(auth=auth)
    return keystone_v3.Client(session=session)

# Used to execute all admin actions
client = client_for_admin_user()
print "print user list to verify client object"
print client.users.list()

SP_url="http://" + sp_ip + ":5000/Shibboleth.sso/SAML2/ECP"
AUTH_url="http://" + sp_ip + ":35357/v3/OS-FEDERATION/identity_providers/keystone-idp/protocols/saml2/auth"


def create_sp(client, sp_id, sp_url, auth_url):
        sp_ref = {'id': sp_id,
                  'sp_url': sp_url,
                  'auth_url': auth_url,
                  'enabled': True}
        return client.federation.service_providers.create(**sp_ref)

print('\nCreate SP')
create_sp(client,
          'keystone-sp',
          SP_url,
          AUTH_url)
