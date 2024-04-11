#! /bin/bash
cd ./add_nonLaArt
#this line creates the initial table & features
# the sample is modified to make the sample less than 9,500 
# as the download stage is dropped when connection is held for this long
python3 extract_nonLaArt.py

#the directory needs to be created before the downloads-
#this line downloads the images and moves them into the above
python3 download_nonLaArt.py 

#this line transforms the data exported from download_LaArt.py, making it more M.L friendly
# TODO
#python3 cleaning_nonLaArt.py