#! /bin/bash
#this line creates the initial table & features
#python3 extract_nonLaArt.py

#the directory needs to be created before the downloads-
#this line downloads the images and moves them into the above
python3 download_nonLaArt.py

#this line transforms the data exported from download_LaArt.py, making it more M.L friendly
#python3 cleaning_nonLaArt.py