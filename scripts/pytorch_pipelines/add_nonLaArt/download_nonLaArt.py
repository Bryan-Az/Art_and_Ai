import pandas as pd
from os.path import exists
import os
import re
from sklearn.model_selection import train_test_split
import shutil
import requests
import time
import numpy as np
import shutil
import requests
#using a premade subset/sample that is representative in diversity in country origin as parent dataset (excluding latin america)
nonLa_image_metadata_sample = pd.read_csv('../../../data_samples/results/processed_subset_results/non_latinamericanart_sample.csv', low_memory=False)
#dropping unneccessary rows (1 removed)
nonLa_image_metadata_sample = nonLa_image_metadata_sample.where(nonLa_image_metadata_sample.title.apply(pd.notna)).dropna(how='all')
nonLa_image_metadata_sample = nonLa_image_metadata_sample.where(nonLa_image_metadata_sample.forwarddisplayname.apply(pd.notna)).dropna(how='all')
nonLa_image_metadata_sample = nonLa_image_metadata_sample.where(nonLa_image_metadata_sample.objectid.apply(pd.notna)).dropna(how='all')
### Image Scraping
shape_initial = nonLa_image_metadata_sample.shape
#### Adding Columns
#### adding expected file name (limiting title to 100 characters and concatenating it with forwardisplayname and objectid to create UUID filepath)
nonLa_image_metadata_sample['file_name'] = nonLa_image_metadata_sample['title'].apply(lambda x: x.replace(' ','_').replace('/', '&')).apply(lambda x: x[:100]) + '_' + nonLa_image_metadata_sample['forwarddisplayname'].apply(lambda x: x.replace(' ', '_').replace('/', '&')) + '_' + nonLa_image_metadata_sample['objectid'].apply(lambda x: str(int(x)) + '.jpg')
#### adding the expected root directory of the image files
la_image_directory = '../../../data_samples/latinamerican-2-imagefolder-split/'
nonLa_image_metadata_sample['directory'] = [la_image_directory] * len(nonLa_image_metadata_sample)
#### subfolder split (train 80% /test 20%) need to be identified randomly
train_data, test_data = train_test_split(nonLa_image_metadata_sample, test_size=0.2)
train_data['subfolder'] = ['train'] * len(train_data)
test_data['subfolder'] = ['test'] * len(test_data)
#### adding new split (subfolder) column to la_image_metadata
nonLa_image_metadata_sample = pd.concat([train_data, test_data]).reset_index(drop=True)
#### adding expected filepath (directory + filename)
nonLa_image_metadata_sample.title = nonLa_image_metadata_sample.title.fillna('missing')
nonLa_image_metadata_sample.forwarddisplayname = nonLa_image_metadata_sample.forwarddisplayname.fillna('missing')
nonLa_image_metadata_sample['image_fp'] = nonLa_image_metadata_sample.directory + nonLa_image_metadata_sample.subfolder + '/' + nonLa_image_metadata_sample.file_name
#### Check the change in shape for input in M.L algs.
#To verify data shape during process
shape_change_1 = nonLa_image_metadata_sample.shape
print('Shape starting: ', shape_initial)
print('Shape after edit 1: ', shape_change_1)
# selects the features relevant to run the download script
nonLa_image_fpaths = nonLa_image_metadata_sample.loc[:, ['objectid','directory','subfolder', 'file_name', 'image_fp']]

def download_image(url, path, name, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(name, "wb") as f:
            f.write(response.content)
        shutil.move(name, path)
    else:
        print(response.status_code)
        
#Define HTTP Headers
ua_header = {
    "User-Agent": "Chrome/51.0.2704.103",
}
# this block now uses the la_image_fpaths table
print("Download starting... please wait :)")
for i in range(0, len(nonLa_image_metadata_sample)):
    # Define URL of an image
    expanded_url = nonLa_image_metadata_sample.expanded_url[i]
    # Define image file name, file path to place
    file_name = nonLa_image_metadata_sample.file_name[i]
    fp = nonLa_image_metadata_sample.image_fp[i]
    # Download image
    # timer delay (15 seconds)
    time.sleep(15)
    download_image(expanded_url, fp, file_name, ua_header)
### Verifying File Names Correspond to the Dataset (Some Images Unable to be Downloaded)
#checking that the filepath / naming conventions I used are consistent
file_exists = []
for i in range(len(nonLa_image_fpaths)):
    file_exists.append(exists(nonLa_image_fpaths.image_fp[i]))
nonLa_image_fpaths['file_downloaded'] = file_exists
### Saving the files edites / created in this NB
presentnonLa_image_fpaths = nonLa_image_fpaths.where(nonLa_image_fpaths.file_downloaded == True).dropna(how='all')
missingnonLa_image_fpaths = nonLa_image_fpaths.where(nonLa_image_fpaths.file_downloaded == False).dropna(how='all')
#### Saving the files to their directories
presentnonLa_image_fpaths.to_csv('../../../data_samples/nonLaArt/presentnonLa_image_fpaths_sample.csv', index=False)
missingnonLa_image_fpaths.to_csv('../../../data_samples/nonLaArt/missingnonLa_image_fpaths_sample.csv', index=False)
print('CSV Created: ../../../data_samples/nonLaArt/presentnonLa_image_fpaths_sample.csv')
print('CSV Created: ../../../data_samples/nonLaArt/missingnonLa_image_fpaths_sample.csv')
nonLa_image_metadata_sample.to_csv('../../../data_samples/nonLaArt/non_latinamerican_art_sample.csv', index=False)
print('CSV Edited: ../../../data_samples/nonLaArt/non_latinamerican_art_sample.csv')

perc_exists = nonLa_image_fpaths.file_downloaded.sum()/len(file_exists)
total = nonLa_image_fpaths.shape[0]
whole_num_exists = perc_exists * total
text = 'The amount of images downloaded is {} percent. Which means {} is amount downloaded, out of {} in latinamerican_art_sample.csv'
print(text.format(perc_exists, whole_num_exists, total))
print("download_nonLaArt.py finished.")