#!/usr/bin/python
import os.path
from subprocess import call
print("Hello World")

#Get reference sequences
if not os.path.isfile("/home/ec2-user/ref/hs37d5.fa"):
	command = "aws s3 cp s3://takomaticsdata/reference_genomes/hg19/ ref --recursive --exclude \"*\" --include \"hs37d5*\""
	print(command)
	call(command)