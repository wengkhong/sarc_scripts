#!/usr/bin/python

print("Hello World")

#Get reference sequences
command = "aws s3 cp s3://takomaticsdata/reference_genomes/hg19/ ref --recursive --exclude \"*\" --include \"hs37d5*\""
print(command)
