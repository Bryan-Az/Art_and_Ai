#! /bin/bash
#these make the directory structure for the images
#mkdir '../latinamerican-2-imagefolder-split/'
#mkdir '../latinamerican-2-imagefolder-split/train'
#mkdir '../latinamerican-2-imagefolder-split/test'
#these lines run the laart pipe
bash ./add_LaArt/add_LaArt.sh
#this line runs the nonlaart pipe
bash ./add_nonLaArt/add_nonLaArt.sh
