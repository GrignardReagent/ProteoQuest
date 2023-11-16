#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd

# define a function to get confirmation from the user as to whether they'd like to proceed (This function is universal to be used in different situations)
def get_confirmation():
    '''This function gets confirmation from the user as to whether they'd like to proceed. It returns True if the user would indeed like to proceed'''
    while True:
        # take an input from the user and turn it lowercase
        confirmation = input("Would you like to proceed with the current search term? (y/n)").lower()
        if confirmation == 'y':
            return True
        elif confirmation == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'")




##### STEP 2 PLOTTING THE LEVEL OF CONSERVATION BETWEEN THE PROTEIN SEQUENCES ####
##### STEP 2_1 PULLING THE PROTEIN SEQUENCES FROM FASTA FILE #####
# this is where we use pullseq to allow the user to limit the number of sequences

# Redefine esearch_result,file_name, seq_count
file_name = str(input("Please enter your UID again:"))
esearch_result = subprocess.getoutput("cat "+file_name+".fasta")
seq_count = subprocess.getoutput("cat "+file_name+".fasta | grep -c '>'")












# TODO: inform the user how many sequences there are in the fasta file generated from the last step



# TODO: ask the user whether they want to limit the number of sequences pulled from the fasta file

# TODO: allow the user to choose the number of sequences to pull from the fasta file
# to make life easier, we alias pullseq to /localdisk/data/BPSM/ICA2/pullseq
subprocess.call('alias pullseq='+'"/localdisk/data/BPSM/ICA2/pullseq"',shell= True)

    # TODO: Ask the user if they want to search for protein sequences of a specific length
subprocess.call("pullseq -i "+str(file_name)+".fasta -m "+int(min_seq_len)+" -a "+int(max_seq_len), shell = True)


# TODO: Ask the user if they want to search for a particular accession ID (not using pullseq)
# while read accession
#  do
#  echo -e "Downloading ${accession} ..."
#  wget -O ${accession}.fasta \
#  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=${accession}&strand=1&rettype=fasta&retmode=text"
#  done < myfileofaccessions.txt

##### PROCESS STEP 2_2 PLOTTING THE LEVEL OF CONSERVATION BETWEEN THE PROTEIN SEQUENCES #####
# the fasta sequence of the protein asked for is saved in esearch_result and the fasta file saved in file_name.fasta
def plot_conservation(file_name):
    '''This function plots the level of conservation between the protein sequences
    sequences: the fasta sequence of the protein asked for
    '''
    print("Preparing your plot, please wait...")

    subprocess.call("clustalo --infile="+str(file_name)+".fasta --outfile="+ str(file_name)+ ".msf --threads=200 --force", shell = True)
    # sprotein1 specifies whether the sequence is a protein
    subprocess.call("plotcon -sequences "+str(file_name)+".msf -sprotein1 True -winsize 4 -graph pdf -goutfile "+str(file_name), shell = True)
    # save as file_name.pdf and file_name.1.png .1 is added because only then it can be opened by eog
    subprocess.call("plotcon -sequences " + str(file_name) + ".msf -sprotein1 True -winsize 4 -graph png -goutfile " + str(file_name), shell=True)
    print('Opening a new window to show the plot, please close it after viewing to proceed.')
    subprocess.call("eog "+str(file_name)+".1.png", shell=True)

# use the plot_conservation() function to plot the level of conservation between the protein sequences
plot_conservation(file_name)


##### END OF STEP 2 #####

##### STEP 3 SCANNING THE PROTEIN SEQUENCE WITH MOTIFS FROM THE PROSITE DATABASE #####
# use patmatmotifs to scan a protein sequence with motifs from the PROSITE database
def scan_motifs(file_name):
    '''This function scans a protein sequence with motifs from the PROSITE database
    sequences: the fasta sequence of the protein asked for
    '''
    print("Preparing your plot, please wait...")

    subprocess.call("patmatmotifs -sequence "+str(file_name)+".fasta -outfile "+str(file_name)+".patmatmotifs.txt", shell = True)
    print('Opening a new window to show the plot, please close it after viewing to proceed.')
    subprocess.call("eog "+str(file_name)+".patmatmotifs.txt", shell=True)

scan_motifs(file_name)

##### END OF STEP 3 #####


##### STEP 4  #####