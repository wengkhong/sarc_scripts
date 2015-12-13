#!/usr/bin/python
import os.path
from subprocess import call
import subprocess
import csv
import shutil

with open('Sarc_Samples.txt','r') as tsv:
        sample_list = [line.strip().split('\t') for line in tsv]

print("Length", len(sample_list))

for line in sample_list:
        sample_name = str(line[2])
        file1 = str(line[0])
        if file1 == "File1":
                continue

        vcf_filename = sample_name + ".filtered.vcf"
        isect_command = "docker run --rm=true -v /home/ec2-user:/home wengkhong/vcflib bedtools intersect -u -a /home/SarcomaPanel/vcfs/" + vcf_filename + " -b /home/SarcomaPanel/vcfs/Sarcoma.bed > " + sample_name + ".filtered.target.vcf"
        print isect_command
        call(isect_command, shell = True)
