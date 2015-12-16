#!/usr/bin/python
import os.path
from subprocess import call
import subprocess
import csv
import shutil
import mygene
from collections import defaultdict
with open('../Selected_Muts.txt','r') as tsv:
	mut_list = [line.strip().split('\t') for line in tsv]

print("Length", len(mut_list))

#Load mutations into dict
genes = defaultdict(list)
for line in mut_list:
	gene = str(line[0])
	mut = str(line[1])
        print gene + "\t" + mut
        genes[gene].append(mut)

mygene = mygene.MyGeneInfo()
for gene in genes:
    #print gene + "\t" + str(genes[gene])
    uniprot_id = mygene.query(gene, fields = 'uniprot')
    #print gene + "\t" + str(uniprot_id) 
    prot_results = uniprot_id['hits'][0]['uniprot']['Swiss-Prot'] 
    uniprot_res = ''
    #print(len(prot_results))
    #print(type(prot_results))
    if(type(prot_results) == unicode):
        uniprot_res = uniprot_id['hits'][0]['uniprot']['Swiss-Prot']
    else:
        uniprot_res = uniprot_id['hits'][0]['uniprot']['Swiss-Prot'][0]
    #print uniprot_res + "\t" + str(prot_results)
    mutations = genes[gene]
    mut_string = ''
    for mut in mutations:
        mut_string += mut[2:] + " "
        #print gene + "\t" + mut
    #print mut_string
    command_string = "/home/ec2-user/lollipops-v1.0-linux64/lollipops -f /usr/share/fonts/msttcore/arial.ttf -o=" + gene + "_lollipop.png -U " + uniprot_res + " " + mut_string
    print command_string
    call(command_string, shell = True)

