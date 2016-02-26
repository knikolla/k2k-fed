# Insert Auth_uri in [cinder]
import configparser

config = configparser.ConfigParser()
config.read('/etc/nova/nova.conf')

config['cinder']['auth_url'] = config['keystone_authtoken']['auth_url']

with open('/etc/nova/nova.conf', 'w') as configfile:
    config.write(configfile)

