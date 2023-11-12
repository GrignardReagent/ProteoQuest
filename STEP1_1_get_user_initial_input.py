#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd
# the following script takes an input from the user, asking them which database they'd like to search from
# and then asks them which search item they'd like to search for and what search type this search item is.
# then it asks whether they'd like to search for a partial match or not.

# TODO: Intro to the programme
# Welcome the user to the programme, introduce what the programme does and what input it will take from the user
print("Welcome to the E-Search programme!"
      "\nThis programme is used for searching protein sequences within the protein database"
      "\nIt will start by asking the user to specify their search terms, and this can be either of the following:"
      "\n1) The taxonomic group name, "
      "\n2) A refined search term, OR"
      "\n3) The UID of the protein of interest"
      "\nIf you need to redefine the search terms, you can use CTRL + C to abort the programme")
#TODO: WHAT IS UID.....
#TODO: WHAT IS REFINED SEARCH TERMS
print("Text search strings entered into the Entrez system are converted into Entrez queries with the following format:"
      "\n   term1[field1] Op term2[field2] Op term3[field3] Op ..."
      "\nwhere the terms are search terms, each limited to a particular Entrez field in square brackets, "
      "combined using one of three Boolean operators: Op = AND, OR, or NOT. "
      "\nThese Boolean operators must be typed in all capital letters."
      "\n   Example: human[organism] AND topoisomerase[protein name]"
      "\nEntrez initially splits the query into a series of items that were originally separated by spaces in the query;"
      "therefore it is critical that spaces separate each term and Boolean operator. "
      "If the query consists only of a list of UID numbers (unique identifiers) or accession numbers, "
      "the Entrez system simply returns the corresponding records and no further parsing is performed. "
      "If the query contains any Boolean operators (AND, OR, or NOT), the query is split into the terms separated by these operators, "
      "and then each term is parsed independently. The results of these searches are then combined according to the Boolean operators.")


##### PROCESS STEP 1: GET USER INITIAL INPUT #####
## This step takes the user's input and store it as a variable so that it can be fed into the esearch commandline

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

# define a function to check the quality of the user's input
def quality_check_user_input(user_input):
    '''This function checks the quality of the user's input. It checks whether the user has specified a valid taxonomic group or not.
    If the user has specified a valid taxonomic group, then the function returns True, otherwise it returns False.'''
    # screen for invalid inputs
    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again
    if re.search("^$", user_input):  # using re, search for anything that contains nothing betweent the start and end of the string
        print("No input was given.")
        return False

    try:
        # run esearch on the commandline and save it to esearch_user_input
        esearch_user_input = subprocess.getoutput("esearch -db taxonomy -spell -query "+'"' + user_input +'"'+ "| efetch")
    except subprocess.CalledProcessError as e:
        print(
            f"Error executing subprocess: {e}, please run the programme again and provide an appropriate taxonomic group name.")
        # handle the error or exit the programme
        sys.exit(1)

    # if esearch returns an empty line on NCBI, return False
    if re.search("^$", esearch_user_input):
        print("No result was found with that input")
        return False

    # if esearch returns a warning or error on NCBI, return False, else True
    if "FAILURE" in esearch_user_input or "WARNING" in esearch_user_input or "ERROR" in esearch_user_input:
        print("Failure, warning or error was returned")
        return False
    else:
        return True

# define a function to check the quality of the user's UID input
def quality_check_user_uid(user_input):
    '''This function checks the quality of the user's UID input. It checks whether the user has specified a valid UID or not.
    If the user has specified a valid taxonomic group, then the function returns True, otherwise it returns False.'''
    # screen for invalid inputs
    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again
    if re.search("^$", user_input):  # using re, search for anything that contains nothing betweent the start and end of the string
        print("No input was given.")
        return False

    try:
        # run esearch on the commandline and save it to esearch_user_input
        esearch_user_input = subprocess.getoutput("esearch -db protein -spell -query "+'"' + user_input +'"'+ "| efetch")
    except subprocess.CalledProcessError as e:
        print(
            f"Error executing subprocess: {e}, please run the programme again and provide an appropriate UID.")
        # handle the error or exit the programme
        sys.exit(1)

    # if esearch returns an empty line on NCBI, return False
    if re.search("^$", esearch_user_input):
        print("No result was found with that input")
        return False

    # if esearch returns a warning or error on NCBI, return False, else True
    if "FAILURE" in esearch_user_input or "WARNING" in esearch_user_input or "ERROR" in esearch_user_input:
        print("Failure, warning or error was returned")
        return False
    else:
        return True

# define a function to get user_input for the taxonomic group
def user_input_UID_False():
    '''This function gets user_input if the user is not inputting an UID as a search item'''
    user_input = input("Which taxonomic group would you like to search for? Enter its name to proceed:")
    # check the quality of the user's input
    while True:
        if quality_check_user_input(user_input) == True:
            print("The taxonomic group you have specified is valid.")
            print(f"The taxonomic group you have specified is: {user_input}")
            print("Please wait...")
            return user_input
        # if the user has not specified a valid taxonomic group then they need to specify the input again
        else:
            print("The taxonomic group you have specified is not valid. Please try again.")
            # ask user to specify the taxonomic group they'd like to search for AGAIN
            user_input = input("Which taxonomic group would you like to search for? Enter its name to proceed: ")
            continue
    return user_input

# define a function to get user_input for UIDs
def user_input_UID_True():
    '''This function gets user_input if the user is inputting an UID as a search item'''
    user_input = input("Please enter a UID: ")
    # check the quality of the user's input
    while True:
        if quality_check_user_uid(user_input) == True:
            print("The UID you have specified is valid.")
            print(f"The UID you have specified is: {user_input}")
            print("Please wait...")
            return user_input
        # if the user has not specified a valid taxonomic group then they need to specify the input again
        else:
            print("The UID you have specified is not valid. Please try again.")
            # ask user to specify the taxonomic group they'd like to search for AGAIN
            user_input = input("Please enter a UID: ")
            continue
    return user_input

#TODO: define a function to refine search result
def refine_search_term():
    '''This function collects a further user input to refine our search result. Input quality check is also performed.'''
    # ask the user if they'd like to search for a UID or start from a taxonomy group
    while True:
        # ask the user if the search term is a UID or a defined search term
        user_search_type = input("Is your search term a UID? (y/n)").lower()
        # if the search term entered by the user is a TAXONOMIC GROUP i.e. not UID
        if user_search_type == 'n':
            # pass through the function to check the quality of the user's input
            user_input = user_input_UID_False()
            return user_input

        # if the search type is not properly defined
        else:
            print("Invalid input. Please enter 'y' or 'n'")

        refined_input = input("How would you like to refine your search term? Enter its name to proceed: ")
        refined_input_type = input("What is the search term type?")
        # while loop to make sure user_input passes the quality check, this will run until it passes!
        while True:
            if quality_check_user_input(user_input):
                print("The following search term will be used in NCBI: ", user_input, '\n',
                      '*Note: This may not be the exact name of the taxonomic group as NCBI allows room for typo in the search term.*')
                return user_input
            else:
                print("The taxonomic group you have specified is not valid. Please try again.")
                # ask user to specify the taxonomic group they'd like to search for AGAIN
                user_input = input("Which taxonomic group would you like to search for? Enter its name to proceed: ")
                continue
# define a function to get user_input
def get_input():
    '''This function collects the user input.'''
    # ask the user if they'd like to search for a UID or start from a taxonomy group
    while True:
        # ask the user if the search term is a UID or a defined search term
        user_search_type = input("Is your search term a UID? (y/n)").lower()
        # if the search term entered by the user is a TAXONOMIC GROUP i.e. not UID
        if user_search_type == 'n':
            # pass through the function to check the quality of the user's input
            user_input = user_input_UID_False()
            # TODO: Would you like to refine your search term?

            return user_input

        # if the search term entered by the user is a refined search term or a UID
        elif user_search_type == 'y':
            # pass through the function to check the quality of the user's input
            user_input = user_input_UID_True()
            return user_input
        # if the search type is not properly defined
        else:
            print("Invalid input. Please enter 'y' or 'n'")


# save user_input as a global variable, but also allow the user to interrupt the programme
try:
    user_input = get_input()
    # print(str(user_input)) # debug line
except KeyboardInterrupt:
    print("\nProgramme interrupted by the user.")
    sys.exit(0)
##### END OF GET USER INITIAL INPUT #####
