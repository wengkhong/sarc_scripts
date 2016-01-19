#!/usr/bin/python
import os.path
from subprocess import call
import subprocess
import csv
import shutil

with open('GS_Samples.txt','r') as tsv:
        sample_list = [line.strip().split('\t') for line in tsv]

print("Length", len(sample_list))

for line in sample_list:
        sample_name = str(line[2])
        file1 = str(line[0])
        if file1 == "File1":
                continue

        vcf_filename = sample_name + ".filtered.target.vcf"
        rename_command = "awk 'BEGIN {OFS=\"\\t\"} {FS=\"\\t\"} {$7=\"" + sample_name + "\";print}' " + vcf_filename + " > " + sample_name + ".filtered.target.name.vcf"
        print rename_command
        call(rename_command, shell = True)
