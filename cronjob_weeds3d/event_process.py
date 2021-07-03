import subprocess
import pandas as pd 

"""
    Author: Shilpa Kancharla
    Last Updated: June 26, 2021
"""

STATE_DICTIONARY = {'NC': 'North Carolina',
                    'MD': 'Maryland',
                    'ML': 'Maryland',
                    'TX': 'Texas',
                    'DE': 'Delaware',
                    'LA': 'Louisiana',
                    'BLACKSTONE': 'Virginia',
                    'VA': 'Virginia',
                    'LAZORO104': 'Virginia',
                    'LAZORO202': 'Virginia',
                    'KENT202': 'Virginia',
                    'KENT103': 'Virginia',
                    'KENTLAND 103': 'Virginia',
                    'OEX-B2': 'Virginia',
                    'OEX-CC2': 'Virginia',
                    'NVC-BT1-CC1': 'Virginia',
                    'NVC-BT1-B1': 'Virginia',
                    'VT': 'Vermont',
                    'MAGNANT': 'Vermont',
                    'MAGNANT2': 'Vermont',
                    'MACHIA': 'Vermont',
                    'GERVAIS': 'Vermont',
                    'GERVAIS2': 'Vermont',
                    'IA': 'Iowa',
                    'C1I': 'Iowa',
                    'C2I': 'Iowa',
                    'C3I': 'Iowa',
                    'C4I': 'Iowa',
                    'C5I': 'Iowa',
                    'C6I': 'Iowa',
                    'MN': 'Minnesota'}

CALIBRATION_DICTIONARY = {'DE': 'GP51471258-CALIB-01-GX010002.npz',
                        'IA': 'GP51457457-CALIB-01-GX010001.npz',
                        'C1I': 'GP51457457-CALIB-01-GX010001.npz',
                        'C2I': 'GP51457457-CALIB-01-GX010001.npz',
                        'C3I': 'GP51457457-CALIB-01-GX010001.npz',
                        'C4I': 'GP51457457-CALIB-01-GX010001.npz',
                        'C5I': 'GP51457457-CALIB-01-GX010001.npz',
                        'C6I': 'GP51457457-CALIB-01-GX010001.npz',
                        'LA': 'GP51451516-CALIB-01-GX010001.npz',
                        'MN': 'GP51451853-CALIB-01-GX010001.npz',
                        'TX': 'GP51451840-CALIB-01-GX010001.npz',
                        'VT': 'GP51450357-CALIB-01-GX010001.npz',
                        'MAGNANT': 'GP51450357-CALIB-01-GX010001.npz',
                        'MAGNANT2': 'GP51450357-CALIB-01-GX010001.npz',
                        'MACHIA': 'GP51450357-CALIB-01-GX010001.npz',
                        'GERVAIS': 'GP51450357-CALIB-01-GX010001.npz',
                        'GERVAIS2': 'GP51450357-CALIB-01-GX010001.npz',
                        'MD': 'GP51457925-CALIB-01-GX010001.npz',
                        'ML': 'GP51457925-CALIB-01-GX010001.npz',
                        'VA': 'GP51451671-CALIB-01-GX010001.npz',
                        'BLACKSTONE': 'GP51451671-CALIB-01-GX010001.npz',
                        'LAZORO104': 'GP51451671-CALIB-01-GX010001.npz',
                        'LAZORO202': 'GP51451671-CALIB-01-GX010001.npz',
                        'KENT202': 'GP51451671-CALIB-01-GX010001.npz',
                        'KENT103': 'GP51451671-CALIB-01-GX010001.npz',
                        'KENTLAND 103': 'GP51451671-CALIB-01-GX010001.npz',
                        'OEX-B2': 'GP51451671-CALIB-01-GX010001.npz',
                        'OEX-CC2': 'GP51451671-CALIB-01-GX010001.npz',
                        'NVC-BT1-CC1': 'GP51451671-CALIB-01-GX010001.npz',
                        'NVC-BT1-B1': 'GP51451671-CALIB-01-GX010001.npz',
                        'NC': 'GP24667519-CALIB-02-GX010170.npz'}

"""
    Run the clustering and analysis process on the blob.

    @param blob_name: name of the blob file that needs to removed from unprocessed blob list to processed file list
    @param src: source of blob added to container
    @param dest: where the blob should be copied to
"""
def run_process(blob_name, src, dest):
    # Copy the blob into the appropriate folder
    subprocess.call('sudo azcopy copy ' + "\"" + src + "\"" + " " + "\"" + dest + blob_name + ".mp4" + "\"" + " --recursive", 
                    shell = True)

    # Match the video to the calibration file (makes the assumption calibration file is on VM)
    key_name = ""
    calibration_file = '/home/azureuser/data/calibration_files/'
    for name in CALIBRATION_DICTIONARY.keys():
        if name in blob_name:
            key_name = name
            calibration_file = calibration_file + CALIBRATION_DICTIONARY[name]
    
    # Activate the environment for preparing frames for SfM part
    subprocess.call('source ~/.venv/python3-cv/bin/activate', shell = True)
    
    # Copy SelectUndistort.py into your video path
    subprocess.call('cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/SelectUndistort.py ' + dest + "/" + key_name,
                    shell = True)

    # Run the next over into your video path
    subprocess.call('python3 SelectUndistort.py -fname ' + blob_name + ".mp4 -dst "  + dest + "/" + key_name + "/" + blob_name +
                    " -calib " + calibration_file + " -imwidth IMGWIDTH -imgap IMAGEGAP",
                    shell = True)

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
    dest = '/home/azureuser/data/videos/'
    run_process(first_line, src, dest)