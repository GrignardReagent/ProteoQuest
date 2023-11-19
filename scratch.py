#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Sample PEPSTATS output
pepstats_output = """
Molecular weight = 72314.18          Residues = 655   
Average Residue Weight  = 110.403    Charge   = 16.0  
Isoelectric Point = 8.8678
A280 Molar Extinction Coefficients  = 60280 (reduced)   61030 (cystine bridges)
A280 Extinction Coefficients 1mg/ml = 0.834 (reduced)   0.844 (cystine bridges)
Improbability of expression in inclusion bodies = 0.852

Residue        Number      Mole%       DayhoffStat
A = Ala        47          7.176       0.834       
B = Asx        0           0.000       0.000       
C = Cys        12          1.832       0.632       
# ... (rest of the residues)

Property      Residues        Number      Mole%
Tiny          (A+C+G+S+T)     201         30.687
Small         (A+B+C+D+G+N+P+S+T+V) 323   49.313
# ... (rest of the properties)
"""

# get the list of all the sequences in the folder
seq_list = subprocess.getoutput("ls *.fasta").split('\n') #TODO:no need to do this again
new_file_name = 'MammaliaORGN_AND_ABC_transporterPROT_NOT_PARTIAL_min103_max1000'
# create a new directory to save the outfiles from patmatmotifs
new_dir = str("pepstats_"+str(new_file_name))

# 'exist_ok = True' makes sure no error is returned if the directory already exists
os.makedirs(f"{new_dir}",exist_ok=True)


# for loop to scan each sequence with pepstats
for seq in seq_list:
    # use pepstats to calculate the statistics of the protein properties and save the report as {seq}.pepstats
    subprocess.call("pepstats -sequence "+ str(seq)
                    +" -outfile "+str(seq)+".pepstats", shell = True)

# move every patmatmotifs report to the new directory
subprocess.call("mv *.pepstats ./"+str(new_dir), shell=True)

print('The protein statistics report for each sequenece in the fasta file'
      'is saved in a new folder called', f'{new_dir}', '.')

# change directory to {new_dir}:
os.chdir(str(new_dir))

time.sleep(1)
print('You are now in the new folder.')

##### END OF PROCESS STEP 4_1 #####

##### PROCESS STEP 4_2 EXTRACT THE STATISTICS FROM THE REPORTS INTO A CSV FILE ####
# define a dictionary to collect seq_name as the key and stat names and values as values (a nested dict)
seq_stats_dict = {}

# define regex for pattern matching (sigh... realising now that I could have done this for step 3...)
# . matching any character except newline \d for digits, \s for white space, + for 1 or more of the instance
pattern_mw = re.compile(r'Molecular weight = ([\d.]+)\s+Residues = (\d+)')
pattern_average_residue_weight = re.compile(r'Average Residue Weight\s+=\s+([\d.]+)')
pattern_charge = re.compile(r'Charge\s+=\s+([\d.]+)')
pattern_isoelectric_point = re.compile(r'Isoelectric Point\s+=\s+([\d.]+)')
pattern_a280_molar_extinction = re.compile(
    r'A280 Molar Extinction Coefficients\s+=\s+(\d+)\s+\(reduced\)\s+(\d+)\s+\(cystine bridges\)')
pattern_a280_extinction_1mgml = re.compile(
    r'A280 Extinction Coefficients 1mg/ml\s+=\s+([\d.]+)\s+\(reduced\)\s+([\d.]+)\s+\(cystine bridges\)')

# for each sequence in the folder, read the patmatmotifs report and extract the motif names and counts
for seq in seq_list:
    with open(str(seq)+".pepstats",'r') as f:
        # initialise seq_name outside the loop and a dictionary to collect seq_name as the key and
        # basic statistics as values
        seq_name = None
        # initialise motif_name outside the loop, this is our inner dictionary
        stats_data = {}
        # same as splitlines (ish)
        lines = f.readlines()
        for line in lines:
            # if the line starts with 'PEPSTATS of', then extract the sequence name
            if line.startswith('PEPSTATS of'):
                seq_name = line.split(' ')[2]
                seq_name = seq_name.replace("'","").replace("[","")
                seq_name = seq_name.rstrip('_')

            # extract information regarding pep statistics by the patterns defined
            match_mw = pattern_mw.search(line)
            match_average_residue_weight = pattern_average_residue_weight.search(line)
            match_charge = pattern_charge.search(line)
            match_isoelectric_point = pattern_isoelectric_point.search(line)
            match_a280_molar_extinction = pattern_a280_molar_extinction.search(line)
            match_a280_extinction_1mgml = pattern_a280_extinction_1mgml.search(line)

            # collect the basic statistics in the dictionary stats_data
            if match_mw:
                stats_data['Molecular Weight'] = float(match_mw.group(1))
                stats_data['Number of Residues'] = int(match_mw.group(2))
            if match_average_residue_weight:
                stats_data['Average Residue Weight'] = float(match_average_residue_weight.group(1))
            if match_charge:
                stats_data['Charge'] = float(match_charge.group(1))
            if match_isoelectric_point:
                stats_data['Isoelectric Point'] = float(match_isoelectric_point.group(1))
            if match_a280_molar_extinction:
                stats_data['A280 Molar Extinction (Reduced)'] = int(match_a280_molar_extinction.group(1))
                stats_data['A280 Molar Extinction (Cysteine Bridges)'] = int(match_a280_molar_extinction.group(2))
            if match_a280_extinction_1mgml:
                stats_data['A280 Extinction 1mg/ml (Reduced)'] = float(match_a280_extinction_1mgml.group(1))
                stats_data['A280 Extinction 1mg/ml (Cysteine Bridges)'] = float(match_a280_extinction_1mgml.group(2))

        # create a nested dictionary to collect the stats_data names and values for each sequence
        seq_stats_dict[seq_name] = stats_data

        # remember to close the file connection
        f.close()

# convert the seq_stats_dict dictionary to a dataframe, with index as the column
stats_df = pd.DataFrame.from_dict(seq_stats_dict, orient='index')
# save the dataframe as a csv file
stats_df.to_csv(f'{new_file_name}_stats.csv',index=True)

print('These are the protein statistics:')
print(stats_df)
print('A summary file for all the sequence statistics is saved'
      'in a csv file called '+str(new_file_name)+'_stats.csv.')
time.sleep(0.5)

##### END OF PROCESS STEP 4_2 #####

##### PROCESS STEP 4_3 PLOT THE STATISTICS IN BAR PLOTS ####
print('Plotting this in bar plots...')
# plotting this csv file
plt.subplot(2, 3, 1)
stats_df['Molecular Weight'].plot(kind='bar', title='Molecular Weight')
plt.xlabel('Proteins')
plt.ylabel('Molecular Weight')
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better visibility

plt.subplot(2, 3, 2)
stats_df['Number of Residues'].plot(kind='bar', title='Number of Residues')
plt.xlabel('Proteins')
plt.ylabel('Number of Residues')
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better visibility

plt.subplot(2, 3, 3)
stats_df['Average Residue Weight'].plot(kind='bar', title='Average Residue Weight')
plt.xlabel('Proteins')
plt.ylabel('Average Residue Weight')
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better visibility

plt.subplot(2, 3, 4)
stats_df['Charge'].plot(kind='bar', title='Charge')
plt.xlabel('Proteins')
plt.ylabel('Charge')
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better visibility

plt.subplot(2, 3, 5)
stats_df['Isoelectric Point'].plot(kind='bar', title='Isoelectric Point')
plt.xlabel('Proteins')
plt.ylabel('Isoelectric Point')
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better visibility

plt.subplot(2, 3, 6)
stats_df['A280 Molar Extinction (Reduced)'].plot(kind='bar', title='A280 Molar Extinction (Reduced)')
plt.xlabel('Proteins')
plt.ylabel('A280 Molar Extinction (Reduced)')
plt.grid(True, axis='y')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better visibility

# add a title to the figure
plt.suptitle("Protein Statistics", fontsize = 16)
# adjust the subplot parameters so that they dont overlap each other
plt.tight_layout()
print('Opening the plot in a new window to show the plot, please close it after viewing to proceed...')
plt.show()
plt.savefig(f"{new_file_name}_stats.png", transparent=True)
