#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd

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
                  '*Note: This may not be the exact name of the taxonomic group as NCBI allows room for typo in the search term.*')
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