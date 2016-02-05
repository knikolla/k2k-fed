import json
import os
import time
import sys

from keystoneclient import session as ksc_session
from keystoneclient.auth.identity import v3
from keystoneclient.v3 import client as keystone_v3
from keystoneclient.v3.contrib.federation.saml import SamlManager

try:
    OS_AUTH_URL = os.environ['OS_AUTH_URL']
    OS_PROJECT_ID = os.environ['OS_PROJECT_ID']
    OS_USER_ID = os.environ['OS_USER_ID']
    OS_PASSWORD = os.environ['OS_PASSWORD']
except KeyError as e:
    raise SystemExit('%s environment variable not set.' % e)

sp_ip = sys.argv[1]

class K2KClient(object):
    def __init__(self):
        self.sp_id = 'keystone-sp'
        self.sp_ip = sp_ip
        self.auth_url = OS_AUTH_URL
        self.project_id = OS_PROJECT_ID
        self.user_id = OS_USER_ID
        self.password = OS_PASSWORD

    def v3_authenticate(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_id=self.user_id,
                           password=self.password,
                           project_id=self.project_id)
        self.session = ksc_session.Session(auth=auth, verify=False)
        self.token = self.session.auth.get_token(self.session)
        self.client = keystone_v3.Client(session=self.session)

    def _check_response(self, response):
        if not response.ok:
            raise Exception("Something went wrong, %s" % response.__dict__)

    def get_saml2_ecp_assertion(self):
        sm = SamlManager(self.client)
        self.assertion = sm.create_ecp_assertion(self.sp_id, self.token)

    def _handle_http_302_ecp_redirect(self, response, location, **kwargs):
        return self.session.get(location, authenticated=False, **kwargs)

    def exchange_assertion(self):
        """Send assertion to a Keystone SP and get token."""
	sp = self.client.federation.service_providers.get(self.sp_id)

        r = self.session.post(
            sp.sp_url,
            headers={'Content-Type': 'application/vnd.paos+xml'},
            data=self.assertion,
            authenticated=False,
            redirect=False)

        self._check_response(r)

        r = self._handle_http_302_ecp_redirect(r, sp.auth_url,
                                               headers={'Content-Type':
                                               'application/vnd.paos+xml'})
        self.fed_token_id = r.headers['X-Subject-Token']
        self.fed_token = r.text

    def list_federated_projects(self):
        url = 'http://' + self.sp_ip + ':5000/v3/OS-FEDERATION/projects'
        headers = {'x-auth-token': self.fed_token_id}
        print headers
        r = self.session.get(url=url, headers=headers, verify=False)
        print json.loads(str(r.text))
        self._check_response(r)
        return json.loads(str(r.text))

    def _get_scoped_token_json(self, project_id):
        return {
            "auth": {
                "identity": {
                    "methods": [
                        "token"
                    ],
                    "token": {
                        "id": self.fed_token_id
                    }
                },
                "scope": {
                    "project": {
                        "id": project_id
                    }
                }
            }
        }

    def scope_token(self, project_id):
        # project_id can be select from the list in the previous step
        token = json.dumps(self._get_scoped_token_json(project_id))
        print token
        url = 'http://' + self.sp_ip + ':5000/v3/auth/tokens'
        headers = {'x-auth-token': self.fed_token_id,
        'Content-Type': 'application/json'}
        r = self.session.post(url=url, headers=headers, data=token,
        verify=False)
        self._check_response(r)
        self.r = r
        self.scoped_token_id = r.headers['X-Subject-Token']
        self.scoped_token_ref = str(r.text)

def main():
    client = K2KClient()
    client.v3_authenticate()
    client.get_saml2_ecp_assertion()
    print('ECP wrapped SAML assertion: %s' % client.assertion)
    client.exchange_assertion()
    print('Unscoped token id: %s' % client.fed_token_id)
    print "==================SCOPE TOKEN================="
    project_list = client.list_federated_projects()
    project_id = str(project_list[u'projects'][0][u'id'])
    print('scope to project [%s]' % project_list[u'projects'][0]['name'])
    print ('project id: %s' % project_id)
    client.scope_token(project_id=project_id)
    print('Scoped token id: %s' % client.scoped_token_id)
#    client.scoped_auth_ref = client.r.json()
#    client.scoped_auth = v3.Token(auth_url="http://128.52.183.216:5000/v3",
#                                token=client.scoped_token_id)
#    client.scoped_auth.auth_ref = client.scoped_auth_ref
#    client.scoped_session = ksc_session.Session(auth=client.scoped_auth, verify=False)
#    client.unscoped_auth = v3.Token(auth_url="http://128.52.183.216:5000/v3",
#                                token=client.fed_token_id)
#    client.unscoped_session = ksc_session.Session(auth=client.unscoped_auth, verify=False)

if __name__ == "__main__":
    main()
