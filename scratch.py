import subprocess
import pandas as pd
import sys
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
            return user_input

        # if the search term entered by the user is a refined search term or a UID
        elif user_search_type == 'y':
            # pass through the function to check the quality of the user's input
            user_input = user_input_UID_True()
            return user_input
        # if the search type is not properly defined
        else:
            print("Invalid input. Please enter 'y' or 'n'")

def get_scientific_names(user_input):
    '''The function takes user_input as an input and returns 4 outputs:
    result_name_list: a list of scientific names of the taxonomic groups
    result_len: the length of the scientific_name_list
    result_name: a string of scientific names of the taxonomic groups
    user_result: the output of the esearch command on NCBI
    '''
    # search for this taxonomic group on esearch and save the output in user_result
    user_result = subprocess.getoutput("esearch -db taxonomy -spell -query " + user_input + "| efetch")

    # search for this taxonomic group on esearch and save the names of the possible taxonimic groups to a string variable
    result_name = subprocess.getoutput(
        "esearch -db taxonomy -spell -query " + user_input +
        "| efetch -format docsum | xtract -pattern DocumentSummary -element ScientificName")
    # -spell performs spell check, 'efetch -format docsum' gets the DocSum of the query, and 'xtract -pattern
    # DocumentSummary -element ScientificName' extracts the scientific name
    # saving every item within scientific_names into a list
    result_name = result_name.splitlines()  # splitting the list into a list of scientific names
    result_len = len(result_name)
    # use a dictionary to save each item in result_name_list as a value and its index as a key
    result_name_dict = {}
    for i in range(result_len):
        result_name_dict[i] = result_name[i]

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

    print("The search term ", user_input, " returns the following results from NCBI:",
          user_result)
    return result_name_dict, result_len, result_name, user_result
user_input = 'elephants'
# execute get_scientific_names to save the outputs as global variables, result_name_dict is the most important one as it will be used to select and refine search terms
result_name_dict, result_len, result_name, user_result = get_scientific_names(user_input)

def refine_search_terms():
    while True:
        # if the result_name_list is empty, then the user has not specified a valid taxonomic group and they need to specify the input again
        # (this should not happen, but a sanity check is always good!)
        if len(result_name_dict) == 0:
            print("It looks like you haven't yet provided a valid input.")
            # use the get_input function
            user_input = get_input()
            # once the condition for scientific_name_list != 0 is satisfied, continue to the next if statement
            exit()

        # if there is only one result_name in result_name_dict, then the user has specified 1 valid taxonomic group
        if len(result_name_dict) == 1:
            print("You have specified the taxonomic group: ", result_name_dict,
                  #TODO: with x number of results on NCBI,
                  "\nNow you can choose to proceed further with the search OR refine your search further."
                  "\nTo start over, use CTRL + C")
            user_confirmation = get_confirmation()
            # print(user_confirmation)  # debug line
            # if the user would like to proceed, then we can go ahead with the user_input
            if user_confirmation == True:
                result_name = result_name_dict[0]
                print("Thank you, proceeding with ", result_name)
                return result_name
            # if the user does not want to proceed, then we can further refine the search
            elif user_confirmation == False:
                print("Let's refine your results further...")
                #TODO: Refining the existing parameters
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
                print("Your initial search term was ", user_input)
                user_input = get_input("Please update your search term (this will overwrite the initial search term):")
                print("Your updated search term is ", user_input)
                # ask the user if they'd like to proceed with the updated search term
                user_confirmation = get_confirmation()
                # print(user_confirmation)  # debug line
                # if the user would like to proceed, then we can go ahead with the user_input
                if user_confirmation == True:
                    result_name = result_name_dict[0]
                    print("Thank you, proceeding with ", result_name)
                    return result_name
                # if the user does not want to proceed, then exit the programme.
                else:
                    print("Thank you for using the programme.")
                    sys.exit(0)

        # if there is more than one result_name in result_name_list, then the user has specified more than 1 valid taxonomic group
        # and the programme will recommend the user to choose between the results
        if len(result_name_dict) > 1:
            print("You have specified the taxonomic groups: ", result_name_dict,
                  # TODO: with x number of results on NCBI,
                  "\nNow you can choose to proceed further with the search using multiple taxonomic groups OR refine your search further"
                  "\n(We recommend you to choose between the results,as using multiple taxonomic groups usually produce 'fluffy' results later on!")
            user_confirmation = get_confirmation()
            # print(user_confirmation)  # debug line
            # if the user would like to proceed, then we can go ahead with the user_input
            if user_confirmation == True:
                # result_name will be everything in result_name_dict
                result_name = result_name_dict
                print("Thank you, proceeding with ", result_name)
                return result_name
            # if the user does not want to proceed, then we can further refine the search
            elif user_confirmation == False:
                print("Let's refine your results further...")
                # allow the user to choose one value from the dictionary result_name_dict
                print(result_name_dict)
                # while loop to take a valid index from the dictionary result_name_dict
                while True:
                    try:
                        result_name = result_name_dict[int(input("Please choose one taxnomic group from the above, enter its index:"))]
                        break
                    except:
                        print("Please enter a valid index.")
                # refining the existing parameters
                print("Let's refine your results even further...")
                print(
                    "Text search strings entered into the Entrez system are converted into Entrez queries with the following format:"
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
                print("Your initial search term was ", user_input)
                user_input = get_input(
                    "Please update your search term (this will overwrite the initial search term):")
                print("Your updated search term is ", user_input)
                # ask the user if they'd like to proceed with the updated search term
                user_confirmation = get_confirmation()
                # print(user_confirmation)  # debug line
                # if the user would like to proceed, then we can go ahead with the user_input
                if user_confirmation == True:
                    result_name = result_name_dict[0]
                    print("Thank you, proceeding with ", result_name)
                    return result_name
                # if the user does not want to proceed, then exit the programme.
                else:
                    print("Thank you for using the programme.")
                    sys.exit(0)

user_input = refine_search_terms(user_input)
# result_names = input("Which of the following taxonomic group would you like to search for?", "\n", result_name_list)
#
# result_names = result_names.strip()  # removing the whitespace from the beginning and end of the string
# result_names = result_names.replace(" ", "_")  # replacing the whitespace with underscores
# result_names = result_names.replace(",", "")  # removing the commas from the scientific name
# result_names = result_names.replace(".", "")  # removing the periods from the scientific name
# result_names = result_names.replace("-", "")  # removing the dashes from the scientific name
# result_names = result_names.replace("(", "")  # removing the parentheses from the scientific name
# result_names = result_names.replace(")", "")  # removing the parentheses from the scientific name
# result_names = result_names.replace("/", "")  # removing the slashes from the scientific name

# # print all 5 variables
# print("The search term ", user_input, " returns the following results from NCBI:",
#       user_result, ".\nIts scientific name is: ", result_names)
#
# print(result_name_list)
# print(result_len)
