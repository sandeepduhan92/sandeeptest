#!/bin/bash
ip=172.31.9.141
ARRAY=(ec2-user root centos)
ARRAY2=(us-east-1a.pem ap-southeast-1a.pem us-west-1c.pem ap-south-1a.pem us-west-2a.pem)
echo ${ARRAY[0]}
echo ${ARRAY2[0]}
login1= /usr/bin/ssh -i /etc/ansible/${ARRAY2[0]} ${ARRAY[0]}@$ip exit;
rcode1=$?
echo $rcode1
if [ "$rcode1" -eq "0" ]; then
ansible-playbook -u "${ARRAY[0]}" --limit=$ip /etc/ansible/check.yml 
else
echo ${ARRAY[1]}
login2= /usr/bin/ssh -i /etc/ansible/${ARRAY2[1]} ${ARRAY[1]}@$ip exit;
rcode2=$?
echo $rcode2
if [ "$rcode2" -eq "0" ]; then
ansible-playbook -u "${ARRAY[1]}" --limit=$ip /etc/ansible/check.yml
else
echo ${ARRAY[2]}
login2= /usr/bin/ssh -i /etc/ansible/${ARRAY2[2]} ${ARRAY[2]}@$ip exit;
rcode2=$?
echo $rcode3
if [ "$rcode3" -eq "0" ]; then
ansible-playbook -u "${ARRAY[2]}" --limit=$ip /etc/ansible/check.yml
else 
echo "User does not exist"
fi
fi
fi
exit;
