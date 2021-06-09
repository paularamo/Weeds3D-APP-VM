import subprocess
import pandas as pd 

"""
    Run the clustering and analysis process on the blob.

    @param blob_name: name of the blob file that needs to removed from unprocessed blob list to processed file list
    @param src: source of blob added to container
    @param dest: where the blob should be copied to
"""
def run_process(blob_name, src, dest):
    # Copy the blob into the appropriate folder
    subprocess.call('sudo azcopy copy ' + "\"" + src + "\"" + " " + "\"" + dest + blob_name + "\"" + " --recursive", 
                    shell = True)
    
    # TODO: how to handle password prompt? --> pexecpt library

    # Run the bash script

    # Once process is finished running, add blob_name to processed_blobs.txt
    with open("processed_blobs.txt", "w") as file:
        file.write(blob_name)
        file.write("\n")
    
    # Remove blob name from blob_list.txt
    delete_blob_from_list(blob_name)

"""
    Once the blob has been processed, remove it from the unprocessed blob list. Add the name of the blob file to the list
    of processed files.

    @param blob_name: name of the blob file that needs to removed from unprocessed blob list to processed file list
"""
def delete_blob_from_list(blob_name):
    blob_file = open("blob_list.txt", "r")
    lines = blob_file.readlines()
    blob_file.close()

    new_blob_file = open("blob_list.txt", "w")
    for line in lines:
        if line.strip("\n") != blob_name:
            new_blob_file.write(line)

if __name__ == "__main__":
    # Get the blob at the top of the blob_list.txt
    first_line = ""
    with open("blob_list.txt", "r") as file:
        first_line = file.readline()

    first_line = first_line.replace("\n", "")
    # Convert blobs.csv to dataframe
    blob_df = pd.read_csv('blobs.csv', sep = ',', names = ['Name', 'URL'])
    blob_df = blob_df.astype({'Name': "str"})
    blob_df = blob_df.astype({'URL': "str"})

    # Get the URL that corresponds to the name of the blob
    src = blob_df[blob_df['Name'] == first_line]['URL'].values[0]

    run_process(first_line, src, dest)