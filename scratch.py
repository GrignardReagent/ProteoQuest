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
    # TODO: USE REGULAR EXPRESSIONS TO CHECK USER INPUT
    # TODO: check if the user has specified a valid taxonomic group, explore different situations where the code could fail
    esearch_user_input = subprocess.getoutput("esearch -db taxonomy -spell -query " + input + "| efetch")
    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again
    if re.search("^$",
                 input):  # using re, search for anything that contains nothing betweent the start and end of the string
        return False
    # TODO: if the user_input returns a taxonomic group which returns error on NCBI, return False
    elif re.search("^$", esearch_user_input):
        return False
    elif "FAILURE" in esearch_user_input:
        return False
    else:
        return True


# define a function to get the user's input
def get_input():
    '''This function collects the user input. Input quality check is also performed.'''
    user_input = input("Which organism would you like to search for? ")
    # while loop to make sure user_input passes the quality check, this will run until it passes!
    while True:
        if quality_check_user_input(user_input):
            print("Organism specified: ", user_input)
            return user_input
        else:
            print("The taxonomic group you have specified is not valid. Please try again.")
            # ask user to specify the taxonomic group they'd like to search for AGAIN
            user_input = input("Which organism would you like to search for? ")
            continue


# save the input as a variable
user_input = get_input()