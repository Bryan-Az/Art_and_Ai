### Step 1 of the La Art Pipeline
### Input is 3 files: (1) constituent_nationalities.csv (2) latin_art.csv
### Output is 2 files: la_geographicStatistics.csv & latinamerican_art.csv
import pandas as pd
import numpy as np
import pycountry
import pycountry_convert as pc
import matplotlib

nationalities = pd.read_csv('../../../data_samples/LaArt/constituents_nationalities.csv')
artist_origin = nationalities.value_counts(normalize=True)

### List of American Continent Codes for Determining which Latin American countries are present in the Gallery (cleaning)
cname_alpha_2 = []
cname_alpha_3 = []
for country in pycountry.countries:
    cname_alpha_2.append(country.alpha_2)
    cname_alpha_3.append(country.alpha_3)
cname_alpha_2 = pd.Series(cname_alpha_2)
cname_alpha_3 = pd.Series(cname_alpha_3)
error_list = ['AQ', 'TF', 'EH', 'PN', 'SX', 'TL', 'UM', 'VA']
continent_names = cname_alpha_2.apply(lambda x: pc.country_alpha2_to_continent_code(x) if x not in error_list else 'non-transformable')
country_and_continent = pd.DataFrame([cname_alpha_2, continent_names], index= ['Country', 'Continent']).T
total_by_continent = country_and_continent.groupby('Continent').count()
# Some codes not available in pycountry package (?)
remove_from_index = ['non-transformable']
total_by_continent.index = pd.Series(list(total_by_continent.index)).apply(lambda x: pc.convert_continent_code_to_continent_name(x) if x not in remove_from_index else x)

### Distribution of Countries by Continent, World Wide (data prep)
country_and_continent['Country Name'] = country_and_continent.Country.apply(pc.country_alpha2_to_country_name)
country_and_continent['Continent Name'] = country_and_continent.Continent.apply(lambda x: pc.convert_continent_code_to_continent_name(x) if x != 'non-transformable' else x)
# 'NA' string translates to null in many data structures, so code changed to use 'NoAm' string instead
country_and_continent['Continent'] = country_and_continent.Continent.apply(lambda x: 'NoAm' if x == 'NA' else x)
Latin_in_NA = ['BZ', 'CR', 'CU', 'DO', 'SV', 'GT', 'HT', 'HN', 'JM', 'MX', 'NI', 'PA', 'LC']
latin_in_NA_map = country_and_continent.Country.apply(lambda x: x in Latin_in_NA)
latin_in_SA_map = country_and_continent.Continent.apply(lambda x: x == 'SA')
latins = country_and_continent.where(latin_in_SA_map | latin_in_NA_map).dropna()
latins.name = 'Latin Countries'
latins.reset_index(inplace=True, drop=True)
latins['Country Name'] = latins.Country.apply(pc.country_alpha2_to_country_name)

### Latin American Group (Feature Engineering)
artist_origin.index = [x[0] for x in list(artist_origin.index)]
# TODO: Fix Hard-coded list of demonyms (name for people living in a certain country; Used in NGA dataset) 
latins['demonym'] = ['Argentinean', 'Belizean', 'Bolivian', 'Brazilian', 'Chilean', 'Colombian', 'Costa Rican', 'Cuban', 'Dominican', 'Ecuadorian', 'Falkland Islander', 'Guatemalan', 'Guianese', 'Guyanese', 'Honduran', 'Haitian', 'Jamaican', 'Saint Lucian', 'Mexican', 'Nicaraguan', 'Panamanian', 'Peruvian', 'Paraguayan', 'South Georgian', 'Salvadoran', 'Surinamese', 'Uruguayan', 'Venezuelan']
artist_origin = artist_origin.reset_index()
artist_origin.columns = ['demonym', 'pct_country_NGA']
### Output Latin American Art data present within the NGA database (Data Prep)
# Important: This file is used to add geographic data to other tables in DB
la_geographicStatistics = pd.merge(artist_origin, latins, how='inner', on ='demonym')
la_geographicStatistics.to_csv('../../../data_samples/LaArt/la_geographicStatistics.csv')
latinamerican_art = pd.read_csv('../../../data_samples/LaArt/latin_art.csv', on_bad_lines='skip')
# SQL Ran: (1) latin_art_people.sql (2) latin_art_urls.sql (3) latin_art.sql
#converts the iiifurl to return the full image size
latinamerican_art['expanded_url'] = latinamerican_art.iiifthumburl.apply(lambda x: x.replace('!200,200', '!256,256'))
latinamerican_art.to_csv('../../../data_samples/LaArt/latinamerican_art.csv', index=False)
