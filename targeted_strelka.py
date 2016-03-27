#!/usr/bin/python
import os.path
from subprocess import call
import subprocess
import csv
import shutil

#Get reference sequences
if not os.path.isfile("/home/ec2-user/ref/hs37d5.fa.gz"):
        command = "aws s3 cp s3://takomaticsdata/reference_genomes/hg19/ /home/ec2-user/ref --recursive --exclude \"*\" --include \"hs37d5*\""
        print(command)
        call(command, shell = True)


command = "docker pull wengkhong/speedseq-manual"
call(command, shell = True)
command = "docker pull wengkhong/vcflib"
call(command, shell = True)


def checkFileInS3(command):
        proc = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
        (out,err) = proc.communicate()
        #print out
        if out:
                return True;
        if not out:
                return False;

#Get sample list
call("aws s3 cp s3://takomaticsdata/Cedric_FEL/SampleSheet.csv . ", shell = True)
#Get target region
call("aws s3 cp s3://takomaticsdata/SureSelect_V5_plusUTRs_hs37d5.bed.tar.gz . ", shell = True)
call("tar xzvf SureSelect_V5_plusUTRs_hs37d5.bed.tar.gz", shell = True)


with open('SampleSheet.csv','r') as tsv:
	sample_list = [line.strip().split(',') for line in tsv]

for line in sample_list:
    print(line)
