#!/usr/bin/python
import os.path
from subprocess import call
import subprocess
import csv
import shutil

print("Hello World")

#Get reference sequences
if not os.path.isfile("/home/ec2-user/ref/hs37d5.fa.gz"):
	command = "aws s3 cp s3://takomaticsdata/reference_genomes/hg19/ /home/ec2-user/ref --recursive --exclude \"*\" --include \"hs37d5*\""
	print(command)
	call(command, shell = True)

command = "docker pull wengkhong/speedseq"
call(command, shell = True)
command = "docker pull wengkhong/vcflib"
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
	print "Currently processing " + sample_name
	#Create folder
        if not os.path.isdir(sample_name):
            os.mkdir(sample_name)
            
	#Goto folder
        os.chdir(sample_name)
        #Get fastq files
        print "Getting fastq files"
        command = "aws s3 cp s3://takomaticsdata/SarcomaPanel/" + file1 + " ."
        call(command, shell = True)
        command = "aws s3 cp s3://takomaticsdata/SarcomaPanel/" + file2 + " ."
        call(command, shell = True)
	#Align and call variants
        print "Aligning for " + sample_name
        command = "docker run --rm=true -v /home/ec2-user:/home wengkhong/speedseq code/speedseq/bin/speedseq align -o /home/" + sample_name + "/" + sample_name + " -R \"@RG\\tID:" + sample_name + "\\tSM:" + sample_name + "\\tLB:lib1\" -t16 -T /home/" + sample_name + "/" + sample_name + "_temp -M 10 /home/ref/hs37d5.fa /home/" + sample_name + "/" + file1 + " /home/" + sample_name + "/" + file2
        print command
        call(command, shell = True)
        print "Calling variants for " + sample_name
        print "Filtering variants for " + sample_name
	#Upload results
        print "Uploading results for " + sample_name
	#Delete folder
        os.chdir('..')
        print "Cleaning up folder for " + sample_name
        #shutil.rmtree(sample_name)
        break

#for line in sample_list:
	#if line[0] == "File1":
	#	continue
	#print(line[0])
#For each sample
#Check if already done (look for vcf in S3)
#If not, run
#	Upload results
#Else next
