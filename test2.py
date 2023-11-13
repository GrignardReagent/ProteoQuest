#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd


def protein_esearch(search_term):
    '''This function performs an esearch within the NCBI protein database given a valid input and outputs the fasta
    sequence of the protein specified.'''
    user_result = subprocess.getoutput("esearch -db protein -spell -query " + '"' + str(search_term) + '"' + "| efetch -format fasta")
    # this will print all the fasta sequences found to the screen
    print(user_result)
    # save the output to a file
    while True:
        save_output = input("Would you like to save this output to your local directory? (y/n)").lower()
        if save_output == 'y':
            # save the output to a file
            with open(f"{search_term}.fasta", "w") as f:
                f.write(user_result)
                f.close()
                print(f"Output saved to {search_term}.fasta")
            return user_result
        elif save_output == 'n':
            print("Output not saved")
            return user_result


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
def user_input_UID_True():
    '''This function gets user_input if the user is inputting an UID as a search item.
     This function will return a fasta sequence for the UID requested'''
    user_input = input("Please enter a UID: ")
    # check the quality of the user's input
    while True:
        if quality_check_user_uid(user_input):
            print("The UID you have specified is valid.")
            print(f"The UID you have specified is: {user_input}")
            print("Please wait...")
            result = protein_esearch(user_input)
            return result
        # if the user has not specified a valid taxonomic group then they need to specify the input again
        else:
            print("The UID you have specified is not valid. Please try again.")
            # ask user to specify the taxonomic group they'd like to search for AGAIN
            user_input = input("Please enter a UID: ")
            continue
    return user_input

user_input_UID_True()
# #TODO: define a function to refine search result
# def refine_search_term():
#     '''This function collects a further user input to refine our search result. Input quality check is also performed.'''
#     # ask the user if they'd like to search for a UID or start from a taxonomy group
#     while True:
#         # ask the user if the search term is a UID or a defined search term
#         user_search_type = input("Is your further search term a UID? (y/n)").lower()
#         # if the search term entered by the user is a TAXONOMIC GROUP i.e. not UID
#         if user_search_type == 'n':
#             # pass through the function to check the quality of the user's input
#             user_input = user_input_UID_False()
#             return user_input
#
#         # if the search type is not properly defined
#         else:
#             print("Invalid input. Please enter 'y' or 'n'")
#
#         refined_input = input("How would you like to refine your search term? Enter its name to proceed: ")
#         refined_input_type = input("What is the search term type?")
#         # while loop to make sure user_input passes the quality check, this will run until it passes!
#         while True:
#             if quality_check_user_input(user_input):
#                 print("The following search term will be used in NCBI: ", user_input, '\n',
#                       '*Note: This may not be the exact name of the taxonomic group as NCBI allows room for typo in the search term.*')
#                 return user_input
#             else:
#                 print("The taxonomic group you have specified is not valid. Please try again.")
#                 # ask user to specify the taxonomic group they'd like to search for AGAIN
#                 user_input = input("Which taxonomic group would you like to search for? Enter its name to proceed: ")
#                 continue