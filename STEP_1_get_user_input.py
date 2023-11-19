#!/usr/bin/python3
import os
import subprocess
import sys
import re
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
##### STEP 1: GET USER INPUT ####
# the following script takes an input from the user, asking them which database they'd like to search from
# and then asks them which search item they'd like to search for and what search type this search item is.
# then it asks whether they'd like to search for a partial match or not.

# welcome the user to the programme, introduce what the programme does and what input it will take from the user
print("Welcome to the E-Search programme!"
      "\nThis programme is used for searching protein sequences within the protein database"
      "\nIt will start by asking the user to specify their search terms step by step:"
      "\n1) The taxonomic group name"
      "\n2) The protein group"
      "\n3) Partial or not partial search"
      "\nThe user will be given an opportunity to refine the whole search term before any protein sequence is analysed."
      "\nYou can use CTRL + C to abort the programme at any point and restart the programme.")


##### PROCESS STEP 1_1: GET USER INITIAL INPUT OF TAXONOMY #####
## This step takes the user's TAXONOMY input and store it as a variable

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
            time.sleep(1)
            print("This is either more than 1000 results or did not return any result. Please refine your search term."
                  "\nYour search term was", search_term)
            time.sleep(0.5)
            search_term = input("The search term should be in the format of "
                                "\nOrganism[ORGN] AND Protein[PROT]"
                                "\nYou can also specify a non-partial search term, e.g., Organism[ORGN] AND Protein[PROT] NOT PARTIAL"
                                "\nPlease enter a new search term:")
        else:
            break
    # run esearch in the protein database on the commandline and save it to user_result
    esearch_result = subprocess.getoutput("esearch -db protein -spell -query " + '"' + str(search_term) + '"' + "| efetch -format fasta")

    # save the output to a file
    print("Your search term returned ", seq_count, " results.")

    # the file_name cannot contain any special characters or spaces, so remove any from the search term
    file_name = search_term.replace(" ", "_")
    file_name = (file_name.replace("[", "").replace("]", "").replace("'", "")
                 .replace(",", "").replace(".", "").replace("-", "")
                 .replace("*", ""))

    # give the user a choice to open a new folder to save any outputs from the search result
    print(f"Would you like to proceed to open a new folder called {file_name} from now on?")
    confirmation = get_confirmation()
    # if the user does want to proceed, then we make a new folder called file_name and change directory to it
    if confirmation == True:
        os.makedirs(f"{file_name}",exist_ok=True)
        os.chdir(f"{file_name}")
        os.getcwd()

    # save the output to a file
    with open(f"{file_name}.fasta", "w") as f:
        f.write(esearch_result)
        f.close()
        print(f"Output saved to {file_name}.fasta in your current working directory.")
    return esearch_result,file_name, seq_count

# define a function to get user_input as taxonomic group
def get_input():
    '''This function collects the user input.'''
    # ask the user to start from defining a taxonomic group
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
                  "\nNow you can choose to proceed further using the current search term OR refine your search further."
                  "\nTo start over, use CTRL + C")
            time.sleep(0.5)
            print('To proceed further with the current search term, please enter \'y\', or refine your search term further by entering \'n\'')
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
                    result_name = result_name_dict[0]
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
    esearch_result,file_name, seq_count = protein_esearch(search_term)
except KeyboardInterrupt:
    print("\nProgramme interrupted by the user.")
    sys.exit(0)
##### END OF PROCESS STEP 1_2 REFINE SEARCH TERMS #####
##### END OF STEP 1 #####

##### STEP 2 DETERMINING AND PLOTTING THE LEVEL OF CONSERVATION BETWEEN THE PROTEIN SEQUENCES ####
##### PROCESS STEP 2_1 LIMIT PROTEIN SEQUENCE NUMBERS FROM FASTA FILE #####

# define a function to get the minimum and maximum length of the protein sequences within the fasta file
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
    print('\nThere are ',int(seq_count),' sequences in your fasta file (containing protein sequences found on NCBI according to your search term).')
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
            time.sleep(0.5)
            # remind the user of their input
            print("The minimum and maximum length of the protein sequences you'd like to use in the conservation analysis are "+ str(def_min_seq_len)+ " and "+ str(def_max_seq_len)+ ".")
            # get the sequence count after trimming the sequences
            try:
                trimmed_seq_count = subprocess.getoutput(
                    "/localdisk/data/BPSM/ICA2/pullseq -i " + str(file_name) + ".fasta -m " + str(
                        def_min_seq_len) + " -a " + str(def_max_seq_len)+"| grep -c '>'")
            except:
                print("The number of sequences in your trimmed fasta file is empty. Please enter a valid minimum and maximum length.")
                time.sleep(0.5)

            print("The number of sequences in your trimmed fasta file is ", trimmed_seq_count)
            time.sleep(0.5)
            # error trap: if max and min range is not appropriate
            if int(trimmed_seq_count) == 0 or "not found" in trimmed_seq_count or 'Error' in trimmed_seq_count:
                print("Please enter a valid minimum and maximum length. (Do NOT proceed!)")
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

##### END OF PROCESS STEP 2_1 LIMIT PROTEIN SEQUENCE NUMBERS FROM FASTA FILE #####

##### PROCESS STEP 2_2 PLOTTING THE LEVEL OF CONSERVATION BETWEEN THE PROTEIN SEQUENCES #####
# define a function to determine and plot the level of conservation between the protein sequences
def plot_conservation(file_name):
    '''This function plots the level of conservation between the protein sequences
    sequences: the fasta sequence of the protein asked for
    '''
    print("Preparing your plot, please wait...")
    # use clustalo to get sequence alignment
    try:
        subprocess.call("clustalo --infile="+str(file_name)+".fasta --outfile="+ str(file_name)+ ".msf --threads=200 --force", shell = True)
    except:
        print("Something went wrong, please try again.")
        sys.exit(1)
    # sprotein1 specifies whether the sequence is a protein
    subprocess.call("plotcon -sequences "+str(file_name)+".msf -sprotein1 True -winsize 4 -graph pdf -goutfile "+str(file_name), shell = True)
    # save as file_name.pdf and file_name.1.png .1 is added because only then it can be opened by eog
    subprocess.call("plotcon -sequences " + str(file_name) + ".msf -sprotein1 True -winsize 4 -graph png -goutfile " + str(file_name), shell=True)
    # tell the user where the plot is saved
    print('The conservation plot is saved in a pdf file and a png file called', file_name, '1.png and ', file_name, 'pdf respectively.')
    time.sleep(0.5)
    # open the plot
    print('Opening a new window to show the plot, please close it after viewing to proceed...')
    time.sleep(0.5)
    subprocess.call("eog "+str(file_name)+".1.png", shell=True)

# this is where we use pullseq to allow the user to limit the number of sequences
# make sure the user entered integers for min and max length of sequences
if type(def_min_seq_len) == int and type(def_max_seq_len) == int:
    trimmed_seq = subprocess.getoutput("/localdisk/data/BPSM/ICA2/pullseq -i "+str(file_name)+".fasta -m "+str(def_min_seq_len)+" -a "+str(def_max_seq_len))
    # save the trimmed sequence to a new file
    new_file_name = str(str(file_name) + "_min" + str(def_min_seq_len) + "_max" + str(def_max_seq_len))
    with open(f"{new_file_name}" + ".fasta", "w") as f:
        f.write(trimmed_seq)
        f.close()
    # plot the conservation of the trimmed sequence
    plot_conservation(new_file_name)
else:
    print("Please enter integers for the minimum and maximum length of the protein sequences you'd like to use in the conservation analysis.")
    sys.exit(1)



##### END OF STEP 2 #####

##### STEP 3 SCANNING THE PROTEIN SEQUENCE WITH MOTIFS FROM THE PROSITE DATABASE #####
##### PROCESS STEP 3_1 EXTRACTING SEQUENCES FROM THE FASTA FILE TO A FOLDER CONTAINING ALL SEQUENCES AS FASTA FILES #####

# define a function to extract the sequences from the fasta file to a folder containing all sequences as fasta files
def extract_seq(file_name):
    '''This function takes the fasta sequence containing multiple sequences as an input and extracts the sequences to separate files.
    The separate files are saved in a new folder and each sequence is also saved as a dictionary item with their accession ID as their key
    '''
    # create a new directory to save the extracted sequences
    new_dir = str("sequences_"+str(file_name))
    # 'exist_ok = True' makes sure no error is returned if the directory already exists
    os.makedirs(f"{new_dir}",exist_ok=True)
    # split the sequences within the fasta file into individual sequences
    # get the content of the fasta file into a variable and splitting the content into individual sequences
    sequences = subprocess.getoutput("cat "+str(file_name)+".fasta").split('>')[1:]
    # define an empty dictionary to collect seq_data
    seq_data_dict = {}
    # extract the sequence data of each sequence in the fasta file
    for sequence in sequences:
        # split the sequence into individual
        lines = sequence.split('\n')
        # save the accession ID by taking the first line in lines and splitting it by space
        header = lines[0].split(' ')
        # the first item in header is the accession ID
        accession_id = header[0]
        # join all the lines together to get the whole sequence
        seq_data = ''.join(lines[1:])
        # use a dictionary to save each item in result_name_dict as a value and its header as a key
        seq_data_dict[accession_id] = seq_data
        # save the sequence data to a new file
        with open(f"./{new_dir}/{accession_id}" + ".fasta", "w") as f:
            f.write(">"+str(header)+"\n")
            f.write(seq_data)
            f.close()
    # inform the user where the files are saved
    print('The extracted sequences are saved in a new folder called', f'{new_dir}', '.')

    # return the dictionary of sequence data and the header
    return seq_data_dict

# executing seq_data_dict and saving the dictionary as a global variable
seq_data_dict = extract_seq(new_file_name)

##### END OF PROCESS STEP 3_1 ####

##### PROCESS STEP 3_2 SCANNING THE PROTEIN SEQUENCE WITH MOTIFS FROM THE PROSITE DATABASE #####
# now we need to scan the protein sequences with motifs from the PROSITE database
# inform the user that the report is being prepared
print('\nWe will now scan the protein sequences with motifs from the PROSITE database.'
      '\nPROSITE is a database of protein families and domains with annotated patterns. '
      '\nIt provides conserved motifs, functional insights, and cross-references to aid in protein analysis. '
      '\nIt is usually used for predicting protein functions and guiding experimental studies.')

time.sleep(0.5)
print("Preparing your report, please wait...")
time.sleep(0.5)
# change directory to sequence_{file_name}
os.chdir("./sequences_"+str(new_file_name))

# get the list of all the sequences in the folder
seq_list = subprocess.getoutput("ls *.fasta").split('\n')

# create a new directory to save the outfiles from patmatmotifs
new_dir = str("patmatmotifs_"+str(new_file_name))

# 'exist_ok = True' makes sure no error is returned if the directory already exists
os.makedirs(f"{new_dir}",exist_ok=True)

# allow the user to decide whether they'd like to scan simple post-translational modifications
print("Would you like to scan for simple post-translational modification sites? (y/n)"
      "\nIf you choose \'n\', then simple post-translational modification sites will not be reported:"
      "myristyl, asn_glycosylation,camp_phospho_site, pkc_phospho_site, ck2_phospho_site, and tyr_phospho_site.")
# ask the user if they'd like to scan simple post-translational modifications
confirmation = get_confirmation()
# if the user would like to scan for simple post-translational modifications, continue with the scan
if  confirmation == True:
    # for loop to scan each sequence with patmatmotifs
    for seq in seq_list:
        # use patmatmotifs to scan a protein sequence with motifs from the PROSITE database
        # scan the protein sequences with motifs form the PROSITE database and save the report as {seq}.patmatmotifs
        subprocess.call("patmatmotifs -sequence "+ str(seq)
                        +" -outfile "+str(seq)+".patmatmotifs", shell = True)
# if the user would not like to scan for simple post-translational modifications, pass in the additional argument -prune
else:
    for seq in seq_list:
        # use patmatmotifs to scan a protein sequence with motifs from the PROSITE database
        # scan the protein sequences with motifs form the PROSITE database and save the report as {seq}.patmatmotifs
        subprocess.call("patmatmotifs -sequence "+ str(seq)
                        +" -outfile "+str(seq)+".patmatmotifs -prune", shell = True)

# move every patmatmotifs report to the new directory
subprocess.call("mv *.patmatmotifs ./"+new_dir, shell=True)

# change directory to {new_dir}:
os.chdir(str(new_dir))
df = pd.DataFrame(columns=['sequence', 'motif_name', 'motif_count'])
# define a dictionary to collect seq_name as the key and motif names and count as values (a nested dict)
seq_motif_dict = {}
# for each sequence in the folder, read the patmatmotifs report and extract the motif names and counts
for seq in seq_list:
    with open(str(seq)+".patmatmotifs",'r') as f:
        # initialise seq_name outside the loop and a dictionary to collect seq_name as the key and
        # motif names and count as values
        seq_name = None
        # initialise motif_name outside the loop, this is our inner dictionary
        motif_name_count = {}
        # same as splitlines (ish)
        lines = f.readlines()
        for line in lines:
            # if the line starts with '#    -sequence', then extract the sequence name
            if line.startswith('#    -sequence'):
                seq_name = line.split('-sequence')[1]
                seq_name= seq_name.strip(".fasta\n")

            # if 'Motif' is found, then extract the motif name and count of that motif
            if 'Motif' in line:
                # split the line into two parts: motif name and the count of it (+1 each time it's found)
                motif_name = line.split(' = ')[1].strip()
                # collect motif_name and increment the count in a dictionary,
                # if the name does not exist, then insert the key with the value 0, which is the count for that motif
                motif_name_count.setdefault(motif_name,0)
                # increment by 1 for that motif_name
                motif_name_count[motif_name] += 1
        seq_motif_dict[seq_name] = motif_name_count
        # remember to close the file connection
        f.close()

print('The reports for each sequenece in the fasta file with motifs from the PROSITE database'
      'are saved in a new folder called', f'{new_dir}', '.')
time.sleep(1)
print('You are now in the new folder.')
# convert the dictionary to a dataframe, with index as the column
df = pd.DataFrame.from_dict(seq_motif_dict, orient='index')
# fill the NaN values with 0
df = df.fillna(0)
# convert the dataframe to a csv file
df.to_csv(f'{new_file_name}_motif_counts.csv',index=False)
print('A summary file for all the sequences scanned with motifs from the PROSITE data base is saved'
      'in a csv file called '+str(new_file_name)+'_motif_count.csv.')
time.sleep(0.5)
print('Plotting this in a bar plot...')
# plotting this csv file
df.plot.bar(stacked = True)
plt.xlabel('Sequence Name')
plt.ylabel('Motif Count')
plt.title('Motif Counts in Each Sequence')
plt.legend(title='Motif',bbox_to_anchor=(0.8, 1), loc='upper right',fontsize='small')
plt.savefig(f"{new_file_name}.png", transparent=True)
plt.show()
# inform the user where the report is saved
print('The report is saved in a png file called '+str(new_file_name)+'.png.')
time.sleep(0.5)
print('Going back to the directory where we started...')

# delete all the fasta files in the sequences_{new_file_name} folder
os.chdir("..") # PWD = sequence_{new_file_name}
subprocess.call("rm -f *.fasta", shell=True)
# go back to the original directory
os.chdir("..") # PWD = where this script is stored.

##### END OF PROCESS STEP 3_2 #####
##### END OF STEP 3 #####

##### STEP 4  #####
##### PROCESS STEP 4_1  ####




# TODO: ask the user if they want to save all the files into a new directory
# if true, save all the files into a new directory

#############################################################

#### TRASH BIN ####

# header = (lines[0].replace(' ', '').replace("(", "").replace(")", "").replace("\'", "").
#           replace(":", "").replace(",", "").replace("-", "").replace(":", "").replace("[","").replace("]","")
#           )


    # TODO: print and save 1) the names of any known motifs found with the sequence (header) 2) HitCount 3) the number of times each motif was found (if applicable)
    # TODO: 4) the positions of each motif found in the sequence 5) the length of the motif found
    # TODO: save 1-5 in a pandas dataframe and save the dataframe as file_name.patmatmotifs.csv