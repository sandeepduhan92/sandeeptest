

import MySQLdb
import ConfigParser
import boto3
import json
import subprocess

Config = ConfigParser.ConfigParser()
Config.read("./config.ini")

# Read DB Config
db_host = Config.get('DB', 'host')
db_name = Config.get('DB', 'db')
db_user = Config.get('DB', 'user')
db_pass = Config.get('DB', 'password')

# Open database connection
#db = MySQLdb.connect("localhost","sshgwuser","sshgwp@sswd","ssh_gw" )
db = MySQLdb.connect(db_host, db_user, db_pass, db_name)

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "select public_ip from instances where zone like '%ap-southeast-1%' and public_ip != 'None' order by public_ip"

public_ip = open("keywords.txt", "w")
#try:
# Excute SQL
cursor.execute (sql)
# Fetch all rows in a list of lists
results = cursor.fetchall()
for row in cursor:
   print>>public_ip, row[0]

public_ip.close()

subprocess.call(["sed -i -e 's|$|/32|g' keywords.txt"] , shell=True)
#subprocess.call(["sed -i -e 's|^|"\"|g' keywords.txt"] , shell=True)
#subprocess.call(["sed -i -e 's|$|"\"|g' keywords.txt"] , shell=True)

#subprocess.call(["sed", "-i", "-e",  's/^/"/g', "keywords.txt"])
#subprocess.call(["sed", "-i", "-e",  's/$/"/g', "keywords.txt"])

#with open('data.json', 'w') as f:
#    json.dump(results, f)

#with open('result.json', 'w') as f:

 #   json.dump(result, f)
#print "ID".ljust(15), "NAME".ljust(35), "PUBLIC_IP".ljust(18), "PRIVATE_IP".ljust(18), "INSTANCE_TYPE".ljust(12), "ZONE".ljust(12), "AWS_REGION".ljust(15)
#print "-".ljust(130, '-')
#for col in results:
#  ID = col[0]
#  NAME = col[1]
#  PUBLIC_IP = str(col[2])
#  PRIVATE_IP = str(col[3])
#  INSTANCE_TYPE = col[4]
#  ZONE = col[5]
#  AWS_REGION = col[6]
  #print "%s\t%s%s%s%s%s%s" % (ID, NAME.ljust(50), PUBLIC_IP.ljust(20), PRIVATE_IP.ljust(20), INSTANCE_TYPE.ljust(18), ZONE.ljust(20), AWS_REGION)
#  print ID.ljust(15), NAME.ljust(35), PUBLIC_IP.ljust(18), PRIVATE_IP.ljust(18), INSTANCE_TYPE.ljust(12), ZONE.ljust(12), AWS_REGION.ljust(15)
#except:
 #   print "Error..."

# disconnect from server
db.close()



# Create an S3 client
s3 = boto3.client('s3')

bucket_name = 'policy11'

with open('keywords.txt', 'r') as f:
 content = f.read()
print content
#with open('keywords.txt', 'r') as f:
 #    data = csv.read(f)

# Create the bucket policy
bucket_policy = {
    "Id": "Policy1513748807987",
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1513748804047",
            "Action": "s3:*",
            "Effect": "Deny",
            "Resource": "arn:aws:s3:::%s" %bucket_name,
            "Condition": {
                "NotIpAddress": {
                "aws:SourceIp": [
                                 "%s" %content,
                ]}
            },
            "Principal": "*"
        }
    ]
}
# Convert the policy to a JSON string
bucket_policy = json.dumps(bucket_policy,content)

# Set the new policy on the given bucket
s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
