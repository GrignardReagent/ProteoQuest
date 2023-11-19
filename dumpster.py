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
print("Welcome to the E-Search programme! \n"
      "This programme is used for searching protein sequences within the protein database\n"
      "It will start by asking the user to specify their search terms, \n")
### PROCESS STEP 0: INPUT AND INPUT PRE-PROCESSING ###
## This step takes the user's input and store it as a variable so that it can be fed into the esearch commandline
## via subprocess in the next step

# define a function to check the quality of the user's input
def quality_check_user_input(input):
    '''This function checks the quality of the user's input. It checks whether the user has specified a valid taxonomic group or not.
    If the user has specified a valid taxonomic group, then the function returns True, otherwise it returns False.'''
    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again, using re
    if re.search("^$", input):
        return False
    # TODO:if the user_input returns a taxonomic group which returns error, warning or if there's no output from NCBI, return False

    # esearch_user_input = subprocess.getoutput("esearch -db taxonomy -spell -query " + user_input + "| efetch")
    # if esearch_user_input == "ERROR":
    #     return False
    # elif esearch_user_input == "WARNING":

    # elif ...:

    #     return False

    else:
        return True

# def get_id():
#     while True:
#
#         user_input=int(input("Input"))
#         if quality_check(user_input):
#             return str(user_input)


# define a function to get the user's input
# TODO: USE REGULAR EXPRESSIONS TO CHECK USER INPUT
def get_input():
    '''This function collects the user input. Input quality check is also performed.'''
    while True:
        user_input = input("Which organism would you like to search for? ")
        if quality_check_user_input(user_input):
            return user_input
        else:
            print("The taxonomic group you have specified is not valid. Please try again.")
            continue
    # # ask user to specify the taxonomic group they'd like to search for
    # user_input = input("Which organism would you like to search for? ")
    # # TODO: quality check user_input
    # # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again, using re
    # if re.search("^$", user_input):
    #     print("The taxonomic group you have specified is not valid. Please try again.")
    #     user_input = input("Which organism would you like to search for? ")
    #     exit()
    return user_input
# save the input as a variable
user_input = get_input()

# define a function to get the scientific names of the taxonomic groups
def get_scientific_names():
    '''The function collects the scientific names from user_input. Quality check is also performed'''
    # search for this taxonomic group on esearch and save the names of the possible taxonimic groups to a list
    scientific_names = subprocess.getoutput("esearch -db taxonomy -spell -query " + user_input + "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")  # -spell performs spell check
    # splitting scientific_names into a list of scientific name
    scientific_name_list = scientific_names.split("\n")  # splitting the list into a list of scientific names

#TODO: quality check scientific_name_list
# if the scientific_name_list is empty, then the user has not specified a valid taxonomic group and they need to specify the input again
if len(scientific_name_list) == 0:
    print("The taxonomic group you have specified is not valid. Please try again.")
    user_input = input("Which organism would you like to search for? ")
    scientific_names = subprocess.getoutput("esearch -db taxonomy -spell -query "+user_input+ "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")  # -spell performs spell check
    # splitting scientific_names into a list of scientific name
    scientific_name_list = scientific_names.split("\n")  # splitting the list into a list of scientific names
    exit()
# if there is only one scientific_name in scientific_name_list, then the user has specified a valid taxonomic group
if len(scientific_name_list) == 1:
    scientific_name = scientific_name_list[0]
    print("You have specified the taxonomic group: ", scientific_name)
    input_confirmation=bool(input("Would you like to proceed? (y/n)"))
    # if the user would like to proceed, then the scientific_name is stored as scientific_name
    if input_confirmation == True:
        scientific_name = scientific_name_list[0]

    # if the user would like to change their organism name, then they have to specify the organism again
    if input_confirmation == False:
        scientific_name = input("Which organism would you like to search for? ")
        scientific_names = subprocess.getoutput("esearch -db taxonomy -spell -query "+user_input+ "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")  # -spell performs spell check
        # splitting scientific_names into a list of scientific name
        scientific_name_list = scientific_names.split("\n")  # splitting the list into a list of scientific names
        #TODO: This will then take them to the beginning of this if statement

        exit()


# output to the screen asking the user which organism they'd like to search for
print(input("Which o",scientific_name_list))



# # specify the database to search from, the user cannot specify the database they'd like to search from, or this will become too complicated...
# database = "protein"
# print("The search database is set to ", database)
#
# # ask user which search type they'd like to use
# SearchType1 = input("Which search type would you like to use? ")
# # ask user which search item they'd like to search for
# SearchItem2 = input("Which search item would you like to search for? ")
#
# # ask user which search type they'd like to use
# SearchType2 = input("Which search type would you like to use? ")
#
# # ask user whether they'd like to search for a partial match or not
# partial_or_not = input("Would you like to search for a partial match or not? ")
#
# # confirm with the user what they've entered by printing the input features to the screen
# print("You have entered: \n"
#       "Search database:", str(database))

# use subprocess to run the following esearch
# subprocess.call("esearch -db {database} -query "{SearchItem1}[{SearchType1}] AND {SearchItem2}[{SearchType2}] {partial_or_not}", shell=True) # should ask user whether they'd like it partial or not, default should be NOT PARTIAL
# for example: esearch -db nucleotide -query "Cosmoscarta[organism]"
# use of efetch for the sequence data:
# esearch -db protein -query "Homo sapiens" | efetch -format fasta >Homosapiens.fasta


def quality_check_user_uid(user_input):
    '''This function checks the quality of the user's UID input. It checks whether the user has specified a valid UID or not.
    If the user has specified a valid taxonomic group, then the function returns True, otherwise it returns False.'''
    # screen for invalid inputs
    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again
    if re.search("^$", user_input):  # using re, search for anything that contains nothing betweent the start and end of the string
        print("No input was given.")
        return False

    try:
        # run esearch in the protein database on the commandline and save it to esearch_user_input
        esearch_user_input = subprocess.getoutput("esearch -db protein -spell -query "+'"' + str(user_input) +'"'+"| efetch -format fasta")
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


# define a function to get user_input for UID
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
            esearch_result,file_name, seq_count = protein_esearch(user_input)
            return esearch_result
        # if the user has not specified a valid taxonomic group then they need to specify the input again
        else:
            print("The UID you have specified is not valid. Please try again.")
            # ask user to specify the taxonomic group they'd like to search for AGAIN
            user_input = input("Please enter a UID: ")
            continue
    return user_input

# define a function to get user_input
def get_input():
    '''This function collects the user input.'''
    # ask the user if they'd like to search for a UID or start from a taxonomy group
    while True:
        # ask the user if the search term is a UID or a defined search term
        user_search_type = input("Is your search term a protein UID? (y/n)").lower()
        # if the search term entered by the user is a TAXONOMIC GROUP i.e. not UID
        if user_search_type == 'n':
            # pass through the function to check the quality of the user's input
            user_input = user_input_UID_False()
            return user_input

        # if the search term entered by the user is a refined search term or a UID
        elif user_search_type == 'y':
            # pass through the function to check the quality of the user's input
            uid_input = user_input_UID_True()
            # we don't want to return the UID, because it would cause chaos!
            # exiting the programme so that UID input is not used for future functions
            sys.exit(0)

        # if the search type is not properly defined
        else:
            print("Invalid input. Please enter 'y' or 'n'")