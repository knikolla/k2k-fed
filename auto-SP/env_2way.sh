IDP_IP=$(/bin/cat /etc/hosts | grep sp | awk '{print $1}')

echo "IDP ip address is ${IDP_IP}"
echo "install shibboleth"
sudo apt-get install -y libapache2-mod-shib2
echo "run insert.py to setup etc keystone.conf and apache2 keystone.conf"
python insert_etc_keyconf.py
sudo python insert_apache_keyconf.py

sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo pip install lxml
echo "Configuring shibboleth for k2k"
sudo python configure_shibboleth.py $IDP_IP

echo "generate shibboleth key"
sudo shib-keygen -f
echo "restart service - shibd and apache2"
sudo service shibd restart
sudo service apache2 restart
echo "make sure that shib2 is enabled"
sudo a2enmod shib2
echo "run python script to register entities, make mapping and protocols and a bunch of other stuff"
python setupk2k_sp.py idp_ip
