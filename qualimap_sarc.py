#!/usr/bin/python
import os.path
from subprocess import call
import subprocess
import csv
import shutil

#Get bed file
call("aws s3 cp s3://takomaticsdata/SarcomaPanel/Sarc_Samples.txt . ", shell = True)
call("aws s3 cp s3://takomaticsdata/Sarcoma.bed . ", shell = True)
call("aws s3 cp s3://takomaticsdata/SarcomaPanel/Sarcoma_Qualimap.bed . ", shell = True)

#Look for qualimap. If it's not there then download and unpack
if(os.path.isfile('/home/ec2-user/qualimap_v2.2/qualimap')):
    print("AOK")
else:
    call("wget https://bitbucket.org/kokonech/qualimap/downloads/qualimap_v2.2.zip", shell = True)
    call("unzip qualimap_v2.2.zip", shell = True)

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
        command = "aws s3 ls s3://takomaticsdata/SarcomaPanel/" + sample_name + "/" + sample_name + "_coverage.txt"
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
       
        #Download BAM file
        command = "aws s3 cp s3://takomaticsdata/SarcomaPanel/" + sample_name + "/" + sample_name + ".bam ."
        print command
        call(command, shell = True)
 
        #Run qualimap
        command = "~/qualimap_v2.2/qualimap bamqc -bam " + sample_name + ".bam -gff ../Sarcoma_Qualimap.bed -c "
        print command
        call(command, shell = True)
        
        #Upload stats to S3
        command = "aws s3 cp " + sample_name + "_stats/genome_results.txt s3://takomaticsdata/SarcomaPanel/" + sample_name + "/" + sample_name + "_coverage.txt"
        print command
        call(command, shell = True)

        #Delete folder
        os.chdir('..')
        print "Cleaning up folder for " + sample_name
        shutil.rmtree(sample_name)
        break
