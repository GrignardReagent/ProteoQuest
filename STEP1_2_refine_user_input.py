#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd
##### STEP 1.2 Refine User Input ####

# define a function to perform an esearch within the NCBI protein database given a valid input and outputs the fasta sequence of the protein specified.
def protein_esearch(search_term):
    '''This function performs an esearch within the NCBI protein database given a valid input and outputs the fasta sequence of the protein specified.'''
    user_result = subprocess.getoutput("esearch -db protein -spell -query " + search_term + "| efetch -format fasta")
    # This will print all the fasta sequences found to the screen
    print(user_result)

# define a function to get the scientific names of the taxonomic groups
def get_scientific_names(user_input):
    '''The function takes user_input as an input and returns 4 outputs:
    result_name_list: a list of scientific names of the taxonomic groups
    result_len: the length of the scientific_name_list
    result_names: a string of scientific names of the taxonomic groups
    user_result: the output of the esearch command on NCBI
    '''
    # search for this taxonomic group on esearch and save the output in user_result
    user_result = subprocess.getoutput("esearch -db taxonomy -spell -query " + user_input + "| efetch")
    # search for this taxonomic group on esearch and save the names of the possible taxonimic groups to a list
    result_names = subprocess.getoutput(
        "esearch -db taxonomy -spell -query " + user_input +
        "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")
    # -spell performs spell check, 'efetch -format docsum' gets the DocSum of the query, and 'xtract -pattern
    # DocumentSummary -element ScientificName' extracts the scientific name
    # saving every item within scientific_names into a list
    result_name_list = result_names.split("\n")  # splitting the list into a list of scientific names
    result_len = len(result_name_list)
    while True:
        # TODO: quality check scientific_name_list (low priority)
        # if the result_name_list is empty, then the user has not specified a valid taxonomic group and they need to specify the input again
        # (this should not happen, but a sanity check is always good!)
        if len(result_name_list) == 0:
            print("It looks like you haven't yet provided a valid input.")
            # use the get_input function
            user_input = get_input()
            # once the condition for scientific_name_list != 0 is satisfied, continue to the next if statement
            exit()

        # if there is only one scientific_name in scientific_name_list, then the user has specified 1 valid taxonomic group
        if len(result_name_list) == 1:
            print("You have specified the taxonomic group: ", result_name_list,
                  "\nLet's refine your results further...")
            user_confirmation = get_confirmation()
            print(user_confirmation)  # debug line
            # if the user would like to proceed, then we can further refine the search
            if user_confirmation == True:
                result_names=result_name_list[0]
                print("Thank you, proceeding with ", result_names)
                return result_names
            # if the user does not want to proceed, then the programme will exit
            elif user_confirmation == False:
                print("Exiting the programme...If you'd like")
                scientific_names = subprocess.getoutput(
                    "esearch -db taxonomy -spell -query " + user_input + "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")  # -spell performs spell check
                # splitting scientific_names into a list of scientific name
                scientific_name_list = scientific_names.split(
                    "\n")  # splitting the list into a list of scientific names
                # TODO: This will then take them to the beginning of this if statement
#CONTINUE HERE
        if len(result_name_list) > 1:

        # output to the screen asking the user which taxonomic group they'd like to search for
        input("Which of the following taxonomic group would you like to search for?", "\n", scientific_name_list)

    # TODO: Maybe put if statements here?
    # TODO: Return the more refined input.
    print("The search term ", user_input, " returns the following results from NCBI:",
          user_result, ".\nIts scientific name is: ", result_name_list)
    return result_name_list, result_len, result_names, user_result


# execute get_scientific_names to save the outputs as global variables
result_name_list, result_len, result_names, user_result = get_scientific_names()





#############################################################
# TODO: pass through the function to perform the search
# print out the number of user_results
user_result_len = subprocess.getoutput(
    "esearch -db protein -spell -query " + '"' + user_input + '"' + "| efetch -format uid | wc -l")

print("The number of results found is: ", len(user_result_uids))
# get confirmation from the user as to whether they'd like to proceed with the current search
confirmation = get_confirmation()
# if the user want to proceed with the search
if confirmation == True:
    print("Proceeding with the search...")
    user_result_uids = subprocess.getoutput(
        "esearch -db protein -spell -query " + user_input + "| efetch -format uid")
    print(user_result_uids)