import pandas as pd
import os
import re
#-- This File is Step 2 of the LaArt Pipeline --
#import the metadata for La Art (this is a result of a MySql Database query script)
la_image_metadata = pd.read_csv('../data_samples/latinamerican_art.csv')
#dropping unneccessary columns
la_image_metadata = la_image_metadata.drop(['accessioned', 'displaydate'], axis = 1)


#creating country demographic statistics
proportion_ofCountry = la_image_metadata['Country Name'].value_counts(normalize=True)
la_image_metadata['percent_fromCountry'] = la_image_metadata['Country Name'].apply(lambda x: proportion_ofCountry[x])
la_image_metadata = la_image_metadata.rename({'Percent_in_NGA': 'percent_fromArtist'}, axis=1)


#setting path to send images during download (in step 3: download_LaArt)
la_image_directory = '../latinamerican-2-imagefolder-split/'
la_image_metadata['directory'] = [la_image_directory] * len(la_image_metadata)
la_image_metadata.to_csv('test_metadata.csv', index=False)

## for next code section in notebook, it is dependent on images being downloaded
## since rename notebook was created during testing, and this is a production script, 
## we assume no images are downloaded and image_fp in pa_latin_art is not set yet
