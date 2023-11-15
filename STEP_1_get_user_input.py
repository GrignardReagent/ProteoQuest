#!/usr/bin/python3
import os
import subprocess
import sys
import re
import numpy as np
import pandas as pd
##### STEP 1: GET USER INPUT ####
# the following script takes an input from the user, asking them which database they'd like to search from
# and then asks them which search item they'd like to search for and what search type this search item is.
# then it asks whether they'd like to search for a partial match or not.

# TODO: Intro to the programme
# welcome the user to the programme, introduce what the programme does and what input it will take from the user
print("Welcome to the E-Search programme!"
      "\nThis programme is used for searching protein sequences within the protein database"
      "\nIt will start by asking the user to specify their search terms, and this can be either of the following:"
      "\n1) The taxonomic group name, OR"
      "\n2) The UID of the protein of interest, if you know it."
      "\nYou can use CTRL + C to abort the programme at any point and restart the programme.")
#TODO: WHAT IS UID.....

##### PROCESS STEP 1_1: GET USER INITIAL INPUT OF TAXONOMY #####
## This step takes the user's TAXONOMY input and store it as a variable

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

# define a function to check the quality of the user's input
def quality_check_user_input(user_input):
    '''This function checks the quality of the user's input. It checks whether the user has specified a valid taxonomic group or not.
    If the user has specified a valid taxonomic group, then the function returns True, otherwise it returns False.'''
    # screen for invalid inputs
    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again
    if re.search("^$", user_input):  # using re, search for anything that contains nothing betweent the start and end of the string
        print("No input was given.")
        return False

    # run esearch in the taxonomy database on the commandline and save it to esearch_user_input
    esearch_user_input = subprocess.getoutput("esearch -db taxonomy -spell -query "+'"' + str(user_input) +'"'+"| efetch")

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

# define a function to check the quality of the user's input
def quality_check_search_term(search_term):
    '''This function checks the quality of the user's search term. It checks whether the user has specified a valid
    search term. If the user has specified a valid taxonomic group, then the function returns True, otherwise it returns False.'''
    # screen for invalid inputs
    # if the user_input is empty, then the user has not specified a taxonomic group and they need to specify the input again
    if re.search("^$", search_term):  # using re, search for anything that contains nothing betweent the start and end of the string
        print("No input was given.")
        return False

    # run esearch in the protein database on the commandline and save its Count number to esearch_user_input
    esearch_search_term = subprocess.getoutput("esearch -db protein -spell -query "+'"' + str(search_term) +'"'+"| grep 'Count'")

    # if esearch returns an empty line on NCBI, return False
    if re.search("^$", esearch_search_term):
        print("No result was found with that input")
        return False

    # if esearch returns a warning or error on NCBI, return False, else True
    if "FAILURE" in esearch_search_term or "WARNING" in esearch_search_term or "ERROR" in esearch_search_term or "0" in esearch_search_term:
        print("Failure, warning or error was returned")
        return False
    else:
        return True

file_name = ""
# define a function to perform an esearch within the NCBI protein database given a valid input and outputs the fasta sequence of the protein specified.
def protein_esearch(search_term):
    '''This function performs an esearch within the NCBI protein database given a valid input and outputs the fasta
    sequence of the protein specified.'''
    while True:
        # count the number of results or sequences found using search_term, use this to quality check the search term
        seq_count = subprocess.getoutput("esearch -db protein -spell -query " +'"'+ str(search_term)+'"'+ "| grep 'Count'")
        # the esearch result for the number of sequences found is typically in the form of <Count>1234</Count>
        seq_count = seq_count.replace("<Count>", "")
        seq_count = seq_count.replace("</Count>", "")
        # if seq_count is more than 1000, then the user needs to refine their search term
        if int(seq_count) > 1000 or int(seq_count) == 0:
            print("Your search term returned ",seq_count, " results.")
            print("This is either more than 1000 results or did not return any result. Please refine your search term."
                  "\nYour search term was", search_term)
            search_term = input("The search term should be in the format of "
                                "\nOrganism[ORGN] AND Protein[PROT]"
                                "\nYou can also specify a non-partial search term, e.g., Organism[ORGN] AND Protein[PROT] NOT PARTIAL"
                                "\nPlease enter a new search term:")
        else:
            break
    # run esearch in the protein database on the commandline and save it to user_result
    esearch_result = subprocess.getoutput("esearch -db protein -spell -query " + '"' + str(search_term) + '"' + "| efetch -format fasta")

    # this will print all the fasta sequences found to the screen
    print(esearch_result)

    # save the output to a file
    print("Your search term returned ", seq_count, " results.")

    # the file_name cannot contain any special characters or spaces, so remove any from the search term
    file_name = search_term.replace(" ", "_")
    file_name = (file_name.replace("[", "").replace("]", "").replace("'", "")
                 .replace(",", "").replace(".", "").replace("-", "")
                 .replace("*", ""))
    # save the output to a file
    with open(f"{file_name}.fasta", "w") as f:
        f.write(esearch_result)
        f.close()
        print(f"Output saved to {file_name}.fasta in your current working directory.")
    return esearch_result,file_name

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

# define a function to get user_input for the taxonomic group
def user_input_UID_False():
    '''This function gets user_input if the user is not inputting an UID as a search item'''
    user_input = input("Which taxonomic group would you like to search for? Enter its name to proceed:")
    # check the quality of the user's input
    while True:
        if quality_check_user_input(user_input):
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
            result = protein_esearch(user_input)
            return result
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

# save user_input as a global variable, but also allow the user to interrupt the programme
try:
    user_input = get_input()
    # print(str(user_input)) # debug line
except KeyboardInterrupt:
    print("\nProgramme interrupted by the user.")
    sys.exit(0)
##### END OF PROCESS STEP 1_1 GET USER INITIAL INPUT FOR TAXONOMY #####

##### PROCESS STEP 1_2 REFINE USER INPUT #####
# define a function to get the scientific names of the taxonomic groups
def get_scientific_names(user_input):
    '''The function takes user_input (taxonomic group) as an input and returns 4 outputs:
    result_name_list: a list of scientific names of the taxonomic groups
    result_len: the length of the scientific_name_list
    result_name: a string of scientific names of the taxonomic groups
    user_result: the output of the esearch command on NCBI
    '''
    # search for this taxonomic group on esearch and save the output in user_result
    user_result = subprocess.getoutput("esearch -db taxonomy -spell -query " + str(user_input) + "| efetch")

    # search for this taxonomic group on esearch and save the names of the possible taxonimic groups to a string variable
    result_name = subprocess.getoutput(
        "esearch -db taxonomy -spell -query " + str(user_input) +
        "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")
    # -spell performs spell check, 'efetch -format docsum' gets the DocSum of the query, and 'xtract -pattern
    # DocumentSummary -element ScientificName' extracts the scientific name

    # if esearch returns error or warning on NCBI, return False, else True (e.g. if user_input is a protein)
    if "FAILURE" in user_result or "WARNING" in user_result or "ERROR" in user_result:
        print("Failure, warning or error was returned, possibly due to input not being a taxonomic group..."
              "\nPlease check your input spelling and try again!"
              "\nYour input was",str(user_input))
        sys.exit(1)

    # saving every item within scientific_names into a list
    result_name = result_name.splitlines()  # splitting the list into a list of scientific names
    result_len = len(result_name)
    # use a dictionary to save each item in result_name_list as a value and its index as a key
    result_name_dict = {}
    for i in range(result_len):
        result_name_dict[i] = result_name[i]
    '''The following code could be used within a function to refine a search term'''
    # # allow the user to choose one value from the dictionary result_name_dict
    # print(result_name_dict)
    # # while loop to take a valid index from the dictionary result_name_dict
    # while True:
    #     try:
    #         result_name = result_name_dict[
    #             int(input("Please choose one taxnomic group from the above, enter its index:"))]
    #         break
    #     except:
    #         print("Please enter a valid index.")

    # print("The search term ", user_input, " returns the following results from NCBI:",
    #       user_result)
    return result_name_dict, result_len, result_name, user_result

# execute get_scientific_names to save the outputs as global variables,
# result_name_dict is the most important one as it will be used to select and refine search terms
result_name_dict, result_len, result_name, user_result = get_scientific_names(user_input)

# define a function to refine the taxonomy search term
def refine_tax_search_terms(user_input):
    result_name_dict, result_len, result_name, user_result = get_scientific_names(user_input)
    while True:
        # if the result_name_list is empty, then the user has not specified a valid taxonomic group and they need to specify the input again
        # (this should not happen, but a sanity check is always good!)
        if len(result_name_dict) == 0:
            print("It looks like you haven't yet provided a valid input.")
            # use the get_input function
            user_input = get_input()
            # once the condition for scientific_name_list != 0 is satisfied, continue to the next if statement
            return user_input

        # if there is only one result_name in result_name_dict, then the user has specified 1 valid taxonomic group
        if len(result_name_dict) == 1:
            print("You have specified the taxonomic group: ", result_name_dict,
                  #TODO: with x number of results on NCBI,
                  "\nNow you can choose to proceed further with the search OR refine your search further."
                  "\nTo start over, use CTRL + C")
            user_confirmation = get_confirmation()
            # if the user would like to proceed, then we can go ahead with the user_input
            if user_confirmation == True:
                result_name = result_name_dict[0]
                print("Thank you, proceeding with the taxonomic group ", result_name)
                return result_name

            # if the user does not want to proceed, then we can further refine the search
            elif user_confirmation == False:
                print("Let's refine your results further...")
                # refining the existing parameters
                # print_refining_instructions()
                print("Your initial search term was ", user_input,
                      "\nPlease update your search term (this will take you back to the start of the programme)")
                user_input = get_input()
                print("Your updated search term is ", user_input)
                # ask the user if they'd like to proceed with the updated search term
                user_confirmation = get_confirmation()
                result_name_dict, result_len, result_name, user_result = get_scientific_names(user_input)
                # if the user would like to proceed, then we can go ahead with the user_input
                if user_confirmation == True:
                    print("Thank you, proceeding with taxonomic group ", result_name)
                    return result_name
                # if the user does not want to proceed, then exit the programme.
                else:
                    print("Thank you for using the programme.")
                    sys.exit(0)

        # if there is more than one result_name in result_name_list, then the user has specified more than 1 valid taxonomic group
        # and the programme will recommend the user to choose between the results
        if len(result_name_dict) > 1:
            print("You have specified the taxonomic groups: ", result_name_dict,
                  "\nNow you should choose one of the taxonomic groups from the above.")
            # allow the user to choose one value from the dictionary result_name_dict
            print(result_name_dict)
            # while loop to take a valid index from the dictionary result_name_dict
            while True:
                try:
                    result_name = result_name_dict[int(input("Please choose one taxnomic group from the above, enter its index:"))]
                    break
                except:
                    print("Please enter a valid index.")
            print("Your updated search term is ", result_name)
            # ask the user if they'd like to proceed with the updated search term
            user_confirmation = get_confirmation()
            # print(user_confirmation)  # debug line
            # if the user would like to proceed, then we can go ahead with the user_input
            if user_confirmation == True:
                result_name = result_name_dict[0]
                print("Thank you, proceeding with taxonomic group ", result_name)
                return result_name
            # if the user does not want to proceed, then exit the programme.
            else:
                print("Thank you for using the programme.")
                sys.exit(0)
# get the user input (taxonomic group) and refine it
try:
    user_input = refine_tax_search_terms(user_input)
except KeyboardInterrupt:
    print("\nProgramme interrupted by the user.")
    sys.exit(0)

# define a function which takes the protein type as a further input before saving both user_input and protein_type
# as search_term to use in protein_esearch()
def get_search_term():
    '''This function takes the protein type as a further input before saving both user_input and protein_type into search_term
    It returns the search term as a string
    user_input: the taxonomic group
    protein_type: the protein type
    search_term: user_input AND protein_type
    '''
    # get the protein type from the user
    protein_type = input("Please enter the specific protein you'd like to search for: ")

    # ask the user if the protein is partial or not
    partial_protein = input("Is the protein partial? (y/n)").lower()
    # if the protein is partial, then we need to add "PARTIAL" at the end of search_term, elif not partial: "NOT PARTIAL"
    if partial_protein == 'y':
        partial_protein = "PARTIAL"
        search_term = str(str(user_input) + "[ORGN]" + " AND " + str(protein_type) + "[PROT] "+str(partial_protein))
        print("Your search term is ", search_term)  # debug line
        return search_term
    elif partial_protein == 'n':
        partial_protein = "NOT PARTIAL"
        search_term = str(str(user_input) + "[ORGN]" + " AND " + str(protein_type) + "[PROT] "+str(partial_protein))
        print("Your search term is ", search_term)  # debug line
        return search_term
    else:
        # get the user_input and protein_type as search_term
        search_term = str(str(user_input) + "[ORGN]" + " AND " + str(protein_type) + "[PROT]")
        print("Your search term is ",search_term)  # debug line
        return search_term

# get the search term
try:
    search_term = get_search_term()
except KeyboardInterrupt:
    print("\nProgramme interrupted by the user.")
    sys.exit(0)

# use protein_esearch() to search for the search term on NCBI
try:
    esearch_result,file_name = protein_esearch(search_term)
except KeyboardInterrupt:
    print("\nProgramme interrupted by the user.")
    sys.exit(0)
##### END OF PROCESS STEP 1_2 REFINE SEARCH TERMS #####
##### END OF STEP 1 #####

##### STEP 2 PLOTTING THE LEVEL OF CONSERVATION BETWEEN THE PROTEIN SEQUENCES ####

# the fasta sequence of the protein asked for is saved in esearch_result and the fasta file saved in file_name.fasta


def plot_conservation():
    '''This function plots the level of conservation between the protein sequences
    sequences: the fasta sequence of the protein asked for
    '''
    print("Preparing your plot, please wait...")

    subprocess.call("clustalo --infile="+str(file_name)+".fasta --outfile="+ str(file_name)+ ".msf --threads=200 --force", shell = True)
    # sprotein1 specifies whether the sequence is a protein
    subprocess.call("plotcon -sequences "+str(file_name)+".msf -sprotein1 True -winsize 4 -graph pdf -goutfile "+str(file_name), shell = True)
    # save as file_name.pdf and file_name.1.png .1 is added because only then it can be opened by eog
    subprocess.call("plotcon -sequences " + str(file_name) + ".msf -sprotein1 True -winsize 4 -graph png -goutfile " + str(file_name), shell=True)
    subprocess.call("eog "+str(file_name)+".1.png", shell=True)

# use the plot_conservation() function to plot the level of conservation between the protein sequences
plot_conservation()




#############################################################