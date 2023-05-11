#! /bin/bash
#this line creates the initial table & features
python3 extract_LaArt.py

#these make the directory structure for the images
mkdir '../latinamerican-2-imagefolder-split/'
mkdir '../latinamerican-2-imagefolder-split/train'
mkdir '../latinamerican-2-imagefolder-split/test'

#this line downloads the images and moves them into the above
python3 download_LaArt.py

#this line transforms the data exported from download_LaArt.py, making it more M.L friendly
python3 cleaning_LaArt.py
