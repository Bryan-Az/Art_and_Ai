### Step 1 of the nonLaArt Pipeline
### Input is 2 files: (1) pa_nonLa_art.csv (2) la_geographicStatistics
### Output is 1 file: (1) nonLa_art_sample.csv
## TODO: Find replacement table for (1) since 1 is missing and it was created with SQL. Since it was based off of the LA sql queries, I will have to recreate the non-LA SQL queries.
import pandas as pd
import numpy as np
import pycountry
import pycountry_convert as pc
import random

nonLa_art = pd.read_csv('../../data_samples/results/whole_set_results/pa_nonLa_art.csv')
la_geographicStatistics = pd.read_csv('../../data_samples/la_geographicStatistics.csv')