#!/usr/bin/python
import os.path
from subprocess import call
import subprocess
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

def checkFileInS3(command):
	proc = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
        (out,err) = proc.communicate()
        #print out
        if out:
		return True;
        if not out:
		return False;


for line in sample_list:
	file1 = str(line[0])
	file2 = str(line[1])
	sample_name = str(line[2])
	if file1 == "File1":
		continue
	#Check if output for this sample already exists. Skip if so
	vcf_filename = sample_name + ".vcf"
	filtered_vcf_filename = sample_name + ".filtered.vcf"
	command = "aws s3 ls s3://takomaticsdata/SarcomaPanel/" + vcf_filename
	if(checkFileInS3(command)):
		print "Sample " + sample_name + " already done. Skipping"
		continue
	############################################################



#for line in sample_list:
	#if line[0] == "File1":
	#	continue
	#print(line[0])
#For each sample
#Check if already done (look for vcf in S3)
#If not, run
#	Upload results
#Else next
