# modify nova codebase
cd /opt/stack/nova
echo "adding moc remote repo"
git remote add moc git://github.com/knikolla/nova
echo "fetch moc repo"
git fetch moc
echo "checkout k2k-liberty branch"
git checkout moc/k2k-liberty

# modify python-novaclient
echo "clone the moc python-novaclient repo"
cd ~ && git clone https://github.com/knikolla/python-novaclient.git
echo "checkout k2k branch"
cd ~/python-novaclient && git checkout k2k
echo "uninstall original python-novaclient"
sudo pip uninstall -y python-novaclient
echo "install the modified python-novaclient"
cd ~/python-novaclient && sudo python setup.py install

# restart nova-api and nova-cpu
echo "restart keystone-api, nova-api, nova-cpu"
screen -p 2 -X stuff "^C^[OA\n"
screen -p 7 -X stuff "^C^[OA\n"
screen -p 14 -X stuff "^C^[OA\n"
