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

for line in sample_list:
	#if line[0] == "File1":
	#	continue
	print(line[0])
