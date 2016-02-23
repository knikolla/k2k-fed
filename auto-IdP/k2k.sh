IDP_IP=$(cat /etc/hosts | grep idp | awk '{print $1}')
SP_IP=$(cat /etc/hosts | grep sp | awk '{print $1}')
echo "SP IP is ${SP_IP}"
echo "IDP IP is ${IDP_IP}"

python k2kclient.py $SP_IP
