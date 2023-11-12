### PROCESS STEP 0: INPUT AND INPUT PRE-PROCESSING ###
## This step takes the user's input and store it as a variable so that it can be fed into the esearch commandline
## via subprocess in the next step
#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd

### PROCESS STEP 0: INPUT AND INPUT PRE-PROCESSING ###
## This step takes the user's input and store it as a variable so that it can be fed into the esearch commandline
## via subprocess in the next step

# define a function to check the quality of the user's input
def quality_check_user_input(input):
    '''This function checks the quality of the user's input. It checks whether the user has specified a valid taxonomic group or not.
    If the user has specified a valid taxonomic group, then the function returns True, otherwise it returns False.'''

    # brackets produces a syntax error in bash when running esearch
    if "(" in input or ")" in input:
        return False

    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again
    if re.search("^$",input):  # using re, search for anything that contains nothing betweent the start and end of the string
        return False
    try:
        # run esearch on the commandline and save it to esearch_user_input
        esearch_user_input = subprocess.getoutput("esearch -db taxonomy -spell -query " + input + "| efetch")
    except subprocess.CalledProcessError as e:
        print(
            f"Error executing subprocess: {e}, please run the programme again and provide an appropriate taxonomic group name.")
        # handle the error or exit the programme
        sys.exit(1)
    # if user_input returns an empty line, warning or error on NCBI, return False
    if re.search("^$", esearch_user_input):
        return False

    if "FAILURE" in esearch_user_input or "WARNING" in esearch_user_input or "ERROR" in esearch_user_input:
    # print("HERE") # debug line
        return False
    else:
        return True

# define a function to get the user's input
def get_input():
    '''This function collects the user input. Input quality check is also performed.'''
    user_input = input("Which taxonomic group would you like to search for? Enter its name to proceed. ")
    # while loop to make sure user_input passes the quality check, this will run until it passes!
    while True:
        if quality_check_user_input(user_input):
            print("The following search term will be used in NCBI: ", user_input, '\n',
                  'Note: This may not be the exact name of the taxonomic group as NCBI allows room for typo in the search term.')
            return user_input
        else:
            print("The taxonomic group you have specified is not valid. Please try again.")
            # ask user to specify the taxonomic group they'd like to search for AGAIN
            user_input = input("Which taxonomic group would you like to search for? Enter its name to proceed. ")
            continue

# save the input as a variable, but also allow the user to interrupt the programme
try:
    user_input = get_input()
except KeyboardInterrupt:
    print("\nProgramme interrupted by the user.")
    sys.exit(0)

### END OF FIRST PART ####

# define a function to get the scientific names of the taxonomic groups
def get_scientific_names():
    '''The function collects the scientific names from user_input. Quality check is also performed'''
    # search for this taxonomic group on esearch and save the output in user_result
    user_result = subprocess.getoutput("esearch -db taxonomy -spell -query " + user_input + "| efetch")
    # search for this taxonomic group on esearch and save the names of the possible taxonimic groups to a list
    print("")
    scientific_names = subprocess.getoutput("esearch -db taxonomy -spell -query " + user_input + "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")  # -spell performs spell check, 'efetch -format docsum' gets the DocSum of the query, and 'xtract -pattern DocumentSummary -element ScientificName' extracts the scientific name
    # saving every item within scientific_names into a list
    scientific_name_list = scientific_names.split("\n")  # splitting the list into a list of scientific names
    return scientific_name_list, scientific_names, user_result
#
# #TODO: define a function to perform a search within the NCBI protein database
# def protein_esearch(search_term):
#     '''This function performs an esearch within the NCBI protein database given a valid input and outputs the fasta sequence of the protein specified.'''
#     user_result = subprocess.getoutput("esearch -db protein -spell -query " + search_term + "| efetch")
#     ...

# define a function to get confirmation from the user as to whether they'd like to proceed
def get_confirmation():
    '''This function gets confirmation from the user as to whether they'd like to proceed'''
    while True:
        # take an input from the user and turn it lowercase
        confirmation = input("Would you like to proceed? (y/n)").lower()
        if confirmation == 'y':
            return True
        elif confirmation == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'")

# execute get_scientific_names to save the outputs as global variables
scientific_name_list, scientific_names, user_result = get_scientific_names()

#TODO: quality check scientific_name_list (low priority)
# if the scientific_name_list is empty, then the user has not specified a valid taxonomic group and they need to specify the input again
# (this should not happen, but a sanity check is always good!)
if len(scientific_name_list) == 0:
    # use the get_input function
    user_input = get_input()
    # use the get_scientific_names function
    scientific_name_list, scientific_names, user_result = get_scientific_names()
    # once the condition for scientific_name_list != 0 is satisfied, continue to the next if statement
    exit()

