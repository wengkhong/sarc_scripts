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

#Download FASTQs
#Check for BAM
#Align FASTQs (upload bam)
#Send email notification
#Check for VCF
#Call variants (upload vcfs)
#Send email notification
