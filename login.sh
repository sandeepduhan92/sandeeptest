#!/bin/bash
ip=172.31.9.141
ARRAY=(ec2-user root centos)
echo ${ARRAY[0]}
login1= /usr/bin/ssh -i /etc/ansible/git2.pem ${ARRAY[0]}@$ip exit;
rcode1=$?
echo $rcode1
if [ "$rcode1" -eq "0" ]; then
ansible-playbook -u "${ARRAY[0]}" --extra-vars="hosts=$ip" /etc/ansible/check.yml 
else
echo ${ARRAY[1]}
login2= /usr/bin/ssh -i /etc/ansible/git2.pem ${ARRAY[1]}@$ip exit;
rcode2=$?
echo $rcode2
if [ "$rcode2" -eq "0" ]; then
ansible-playbook -u "${ARRAY[1]}" --extra-vars="hosts=$ip" /etc/ansible/check.yml
else
echo ${ARRAY[2]}
login2= /usr/bin/ssh -i /etc/ansible/git2.pem ${ARRAY[2]}@$ip exit;
rcode2=$?
echo $rcode3
if [ "$rcode3" -eq "0" ]; then
ansible-playbook -u "${ARRAY[2]}" --extra-vars="hosts=$ip" /etc/ansible/check.yml
else 
echo "User does not exist"
fi
fi
fi
exit;
