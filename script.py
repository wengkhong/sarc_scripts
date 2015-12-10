#!/usr/bin/python
import os.path
from subprocess import call
import csv

print("Hello World")

#Get reference sequences
if not os.path.isfile("/home/ec2-user/ref/hs37d5.fa.gz"):
	command = "aws s3 cp s3://takomaticsdata/reference_genomes/hg19/ /home/ec2-user/ref --recursive --exclude \"*\" --include \"hs37d5*\""
	print(command)
	call(command, shell = True)

command = "docker pull wengkhong/speedseq"
call(command, shell = True)

call("sudo pip install boto3", shell = True)
import boto3
#Get sample list
call("aws s3 cp s3://takomaticsdata/SarcomaPanel/Sarc_Samples.txt . ", shell = True)

with open('Sarc_Samples.txt','r') as tsv:
	sample_list = [line.strip().split('\t') for line in tsv]

print("Length", len(sample_list))

s3 = boto3.resource('s3')
bucket = s3.Bucket('takomaticsdata')
exists = True
try:
    s3.meta.client.head_bucket(Bucket='takomaticsdata')
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

for bucket in s3.buckets.all():
    print(bucket.name)

#proc = subprocess.Popen(["cat", "/etc/services"], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#print "program output:", out

#path=$1
#s3cmd info $path >/dev/null 2>&1

#if [[ $? -eq 0 ]]; then
#    echo "exist"
#else
#    echo "do not exist"
#fi


#for line in sample_list:
	#if line[0] == "File1":
	#	continue
	#print(line[0])
#For each sample
#Check if already done (look for vcf in S3)
#If not, run
#	Upload results
#Else next
