import pandas as pd
import os
import re
from sklearn.model_selection import train_test_split
import shutil
import requests
import time
#-- This File is Step 2 of the LaArt Pipeline --
# 1 Input: (1) latinamerican_art.csv
# 2 Output: (1) latinamerican_art.csv (2) la_image_fpaths.csv (3) validLa_image_fpaths.csv
#import the metadata for La Art (this is a result of a MySql Database query script) with minor modifications
la_image_metadata = pd.read_csv('../../../data_samples/LaArt/latinamerican_art.csv')
shape_initial = la_image_metadata.shape
#dropping unneccessary rows (1 removed)
la_image_metadata = la_image_metadata.drop_duplicates()
la_image_metadata = la_image_metadata.where(la_image_metadata.title.apply(pd.notna)).dropna(how='all')
la_image_metadata = la_image_metadata.where(la_image_metadata.forwarddisplayname.apply(pd.notna)).dropna(how='all')
la_image_metadata = la_image_metadata.where(la_image_metadata.objectid.apply(pd.notna)).dropna(how='all')
# adding expected file name (limiting title to 100 characters and concatenating it with forwardisplayname and objectid to create UUID filepath)
la_image_metadata['file_name'] = la_image_metadata['title'].apply(lambda x: x.replace(' ','_').replace('/', '&')).apply(lambda x: x[:100]) + '_' + la_image_metadata['forwarddisplayname'].apply(lambda x: x.replace(' ', '_').replace('/', '&')) + '_' + la_image_metadata['objectid'].apply(lambda x: str(int(x)) + '.jpg')
#adding the expected root directory of the image files
la_image_directory = '../../../data_samples/latinamerican-2-imagefolder-split/'
la_image_metadata['directory'] = [la_image_directory] * len(la_image_metadata)
#subfolder split (train 70% /test 30%) need to be identified randomly
train_data, test_data = train_test_split(la_image_metadata, test_size=0.3)
train_data['subfolder'] = ['train'] * len(train_data)
test_data['subfolder'] = ['test'] * len(test_data)
#adding new split (subfolder) column to la_image_metadata
la_image_metadata = pd.concat([train_data, test_data]).reset_index(drop=True)
# adding expected filepath (directory + filename)
la_image_metadata['image_fp'] = la_image_metadata.directory + la_image_metadata.subfolder + '/' + la_image_metadata.file_name

#To verify data shape during process
shape_change_1 = la_image_metadata.shape
print('Shape starting: ', shape_initial)
print('Shape after edit 1: ', shape_change_1)

# selects the features relevant to run the download script
la_image_fpaths = la_image_metadata.loc[:, ['expanded_url', 'objectid', 'directory','subfolder','file_name', 'image_fp']]

## for next code section in notebook, images will be downloaded
## I assume no images are downloaded & image_fp/directory not created
def download_image(url, path, name, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(name, "wb") as f:
            f.write(response.content)
        shutil.move(name, path)
    else:
        print(response.status_code)
# Define HTTP Headers
ua_header = {
    "User-Agent": "Chrome/51.0.2704.103",
}

# this block now uses the la_image_fpaths table
print("Download starting... please wait :)")
# This block iterates over all the images
for i in range(0, len(la_image_fpaths)):
    # Define URL of an image
    expanded_url = la_image_fpaths.expanded_url[i]
    # Define image file name, file path to place
    file_name = la_image_fpaths.file_name[i]
    fp = la_image_fpaths.image_fp[i]
    # Download image
    # timer delay (15 seconds)
    time.sleep(15)
    download_image(expanded_url, fp, file_name, ua_header)
    
#checking that the filepath / naming conventions I used are consistent
from os.path import exists
file_exists = []
for i in range(len(la_image_fpaths)):
    file_exists.append(exists(la_image_fpaths.image_fp[i]))
la_image_fpaths['file_downloaded'] = file_exists

presentLa_image_fpaths = la_image_fpaths.where(la_image_fpaths.file_downloaded == True).dropna(how='all')

missingLa_image_fpaths = la_image_fpaths.where(la_image_fpaths.file_downloaded == False).dropna(how='all')

#saving the image fp data for use with the model
presentLa_image_fpaths.to_csv('../../../data_samples/LaArt/presentLa_image_fpaths.csv', index=False)
missingLa_image_fpaths.to_csv('../../../data_samples/LaArt/missingLa_image_fpaths.csv', index=False)
print('CSV Created: ../../../data_samples/LaArt/presentLa_image_fpaths.csv')
print('CSV Created: ../../../data_samples/LaArt/missingLa_image_fpaths.csv')
la_image_metadata.to_csv('../../../data_samples/LaArt/latinamerican_art.csv', index=False)
print('CSV Edited: ../../../data_samples/LaArt/latinamerican_art.csv')

perc_exists = la_image_fpaths.file_downloaded.sum()/len(file_exists)
total = la_image_fpaths.shape[0]
whole_num_exists = perc_exists * total
text = 'The amount of images downloaded is {} percent. Which means {} is amount downloaded, out of {} in latinamerican_art.csv'
print(text.format(perc_exists, whole_num_exists, total))
print("download_LaArt.py finished.")