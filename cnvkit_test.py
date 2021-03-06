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

command = "docker pull etal/cnvkit"
call(command, shell = True)
#command = "docker pull wengkhong/vcflib"
#call(command, shell = True)

