#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt


# define a function to get confirmation from the user as to whether they'd like to proceed (This function is universal to be used in different situations)
def get_confirmation():
    '''This function gets confirmation from the user as to whether they'd like to proceed. It returns True if the user would indeed like to proceed'''
    while True:
        # take an input from the user and turn it lowercase
        confirmation = input("Would you like to proceed? (y/n)").lower()
        if confirmation == 'y':
            return True
        elif confirmation == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'")

file_name = "MammaliaORGN_AND_transporterPROT"

def get_min_and_max_seq_len():
    '''This function takes the minimum and maximum length of the protein sequences within the fasta file
    and returns the minimum and maximum length as a tuple'''
    # count the sequence length for each sequence in the fasta file
    # get the content of the fasta file into a variable and splitting the content into individual sequences
    sequences = subprocess.getoutput("cat "+str(file_name)+".fasta").split('>')[1:]
    # create a list to collect the sequence lengths
    seq_lens = []
    # count the length of each sequence and append seq_len into seq_lens
    for sequence in sequences:
        lines = sequence.split('\n')
        header = lines[0]
        seq_data = ''.join(lines[1:])
        # count the length of each sequence
        seq_len = len(seq_data)
        seq_lens.append(seq_len)

    # get the minimum and maximum length of the protein sequences within the fasta file
    min_seq_len = min(seq_lens)
    max_seq_len = max(seq_lens)
    # return the minimum and maximum length as a tuple
    return min_seq_len, max_seq_len

# ask the user whether they want to limit the number of sequences to use for the conervsation analysis
def define_min_and_max_seq_len():
    '''This function allows the user to decide whether they'd like to limit the number of sequences to use for the
    conservation analysis and to limit the seq num by defining a min and max sequence length.'''
    # inform the user how many sequences there are in the fasta file generated from the last step, so that they can make an informed decision
    print('\nWe will now determine and plot the level of conservation between the protein sequences.')
    time.sleep(0.5)
    print('\nBefore we do that, you may wish to limit the number of sequences used for the conservation analysis.')
    time.sleep(0.5)
    print('\nAn advantage of this is so that the analysis focuses on the most biologically meaningful data and that as little noise as possible is in the conservation plot.')
    time.sleep(0.5)
    # print('\nThere are ',int(seq_count),' sequences in your fasta file (containing protein sequences found on NCBI according to your search term).')
    # inform the user how long the shortest sequence is and the longest, so that they can make an informed decision
    min_seq_len, max_seq_len = get_min_and_max_seq_len()
    print('\nThe shortest sequence is ',min_seq_len,' amino acids long,'
                                                    '\nand the longest sequence is ', max_seq_len,' amino acids long.')
    time.sleep(0.5)
    print('\nEnter \'y\' if you\'d like to reduce the number of sequences to use in the conservation analysis, and \'n\' if you want to skip this.')
    time.sleep(0.5)
    # ask the user whether they'd like to proceed to reduce the number of sequences to use in the conservation analysis
    confirmation = get_confirmation()
    if confirmation == True:
        print("The programme will now prompt you to enter the minimum and maximum length of the protein sequences you'd like to use in the conservation analysis.")
        time.sleep(0.5)
        while True:
            while True:
                # get the minimum length of the protein sequences you'd like to use in the conservation analysis
                # error trap
                try:
                    def_min_seq_len = int(input(
                        'Please enter (in integer) the MINIMUM length of the protein sequences you\'d like to use in the conservation analysis:'))
                    break
                except ValueError:
                    print("Please enter an integer.")
            time.sleep(0.5)
            while True:
                # get the maximum length of the protein sequences you'd like to use in the conservation analysis
                # error trap
                try:
                    def_max_seq_len = int(input(
                        'Please enter (in integer) the MAXIMUM length of the protein sequences you\'d like to use in the conservation analysis:'))
                    break
                except:
                    print("Please enter an integer.")
                    continue
            # def_max_seq_len = int(input(
            #     'Please enter (in integer) the MAXIMUM length of the protein sequences you\'d like to use in the conservation analysis:'))
            time.sleep(0.5)
            # remind the user of their input
            print("The minimum and maximum length of the protein sequences you'd like to use in the conservation analysis are "+ str(def_min_seq_len)+ " and "+ str(def_max_seq_len)+ ".")
            # get the sequence count after trimming the sequences
            try:
                trimmed_seq_count = subprocess.getoutput(
                    "/localdisk/data/BPSM/ICA2/pullseq -i " + str(file_name) + ".fasta -m " + str(
                        def_min_seq_len) + " -a " + str(def_max_seq_len)+"| grep -c '>'")
                print("The number of sequences in your trimmed fasta file is ", trimmed_seq_count)
                time.sleep(0.5)
            except:
                print("The number of sequences in your trimmed fasta file is empty. Please enter a valid minimum and maximum length.")
                time.sleep(0.5)

            # ask whether the user would like to proceed with the entered values
            confirmation = get_confirmation()
            if confirmation == True:
                print("Thank you, proceeding with the analysis...")
                time.sleep(0.5)
                return def_min_seq_len,def_max_seq_len
            else:
                print("Taking you back to the last step...")
                time.sleep(0.5)
    # if the user does not want to apply any min or max length for sequences, then proceed with the analysis
    else:
        print("Thank you, proceeding with the analysis with default minimum and maxium sequence lengths...")
        # give def_min_seq_len and def_max_seq_len default values
        def_max_seq_len, def_min_seq_len = int(max_seq_len), int(min_seq_len)
        print("The minimum and maximum length of the protein sequences you'd like to use in the conservation analysis are " + str(
                def_min_seq_len) + " and " + str(def_max_seq_len) + ".")

        return def_min_seq_len,def_max_seq_len

# get the minimum and maximum length of the protein sequences to use in the conservation analysis
def_min_seq_len, def_max_seq_len = define_min_and_max_seq_len()






