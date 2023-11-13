import subprocess
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
        if int(seq_count) > 1000:
            print("Your search term resulted in more than 1000 results. Please refine your search term."
                  "\nYour search term was", search_term)
            search_term = input("Please enter a new search term: ")
        else:
            break
    # run esearch in the protein database on the commandline and save it to user_result
    esearch_result = subprocess.getoutput("esearch -db protein -spell -query " + '"' + str(search_term) + '"' + "| efetch -format fasta")

    # this will print all the fasta sequences found to the screen
    print(esearch_result)
    # ask the user if they'd like to save the output to a file
    while True:
        save_output = input("Would you like to save this output to your local directory? (y/n)").lower()
        if save_output == 'y':
            # the file_name cannot contain any special characters or spaces, so remove any from the search term
            file_name = search_term.replace(" ", "_")
            file_name = (file_name.replace("[", "").replace("]", "").replace("'", "")
                         .replace(",", "").replace(".", "").replace("-", "")
                         .replace("*", ""))
            # save the output to a file
            with open(f"{file_name}.fasta", "w") as f:
                f.write(esearch_result)
                f.close()
                print(f"Output saved to {file_name}.fasta")
            return esearch_result
        elif save_output == 'n':
            print("Output not saved")
            return esearch_result

protein_esearch(search_term="birds[ORGN] AND kinase[PROT]")