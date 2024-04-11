### Step 1 of the nonLaArt Pipeline
### Input is 2 files: (1) pa_nonLa_art.csv (2) la_geographicStatistics
### Output is 1 file: (1) nonLa_art_sample.csv
## TODO: Find replacement table for (1) since 1 is missing and it was created with SQL. Since it was based off of the LA sql queries, I will have to recreate the non-LA SQL queries.
print('extract_nonLaArt.py started')
import pandas as pd
import numpy as np
import pycountry
import pycountry_convert as pc
import random
#this should be taken as non_latin_art.csv from scripts/source-sql
#new version expects dtype on import however as of now only 1 row is impacted
non_latinamerican_art = pd.read_csv('../../../data_samples/nonLaArt/non_latinamerican_art.csv', low_memory=False, on_bad_lines='skip')
#Step 2 of the La Art Pipeline: Feature Engineering new geographical features
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
#This is an important aspect of the data as it will pair the countries with their continents and the nationalities of the artists in the dataset
total_by_continent = country_and_continent.groupby('Continent').count()['Country'].copy()
### Distribution of Countries by Continent, World Wide
country_and_continent['Country Name'] = country_and_continent.Country.apply(pc.country_alpha2_to_country_name)
country_and_continent['Continent Name'] = country_and_continent.Continent.apply(lambda x: pc.convert_continent_code_to_continent_name(x) if x != 'non-transformable' else x)
constituent_nationalities = non_latinamerican_art.nationality.copy()
nonla_artist_origin = constituent_nationalities.value_counts(normalize=True)
# Adding information to select for non_latinamerican_art (todo- write script to create the change in the DB)
Latin_in_NA = ['BZ', 'CR', 'CU', 'DO', 'SV', 'GT', 'HT', 'HN', 'JM', 'MX', 'NI', 'PA', 'LC']
latin_in_NA_map = country_and_continent.Country.apply(lambda x: x in Latin_in_NA)
latin_in_SA_map = country_and_continent.Continent.apply(lambda x: x == 'SA')
latins = country_and_continent.where(latin_in_SA_map | latin_in_NA_map).dropna()
latins.name = 'Latin Countries'
latins.reset_index(inplace=True, drop=True)
latins['Country Name'] = latins.Country.apply(pc.country_alpha2_to_country_name)
#the assistance of an outside demonyms table which has a key to connect Country to Demonym
demonyms = pd.read_csv('../../../data_samples/results/processed_subset_results/demonyms.csv')
latins['demonym'] = ['Argentinean', 'Belizean', 'Bolivian', 'Brazilian', 'Chilean', 'Colombian', 'Costa Rican', 'Cuban', 'Dominican', 'Ecuadorian', 'Falkland Islander', 'Guatemalan', 'Guianese', 'Guyanese', 'Honduran', 'Haitian', 'Jamaican', 'Saint Lucian', 'Mexican', 'Nicaraguan', 'Panamanian', 'Peruvian', 'Paraguayan', 'South Georgian', 'Salvadoran', 'Surinamese', 'Uruguayan', 'Venezuelan']
nonla_artist_origin = nonla_artist_origin.reset_index(drop=False)
nonla_artist_origin.columns = ['demonym', 'pct_country_NGA']
#### This will remove the subset of data that is latin american from nonlatines and thus nonla_geographicStatistics
non_latines = pd.merge(country_and_continent, demonyms, how='inner', on ='Country Name')
non_latines = non_latines.astype({'Country':'string','Continent':'string','Country Name':'string','Continent Name':'string','demonym':'string'})
latins = latins.astype({'Country':'string','Continent':'string','Country Name':'string','Continent Name':'string','demonym':'string'})
non_latines = non_latines.where(non_latines['Country Name'].apply(lambda x: not latins['Country Name'].isin([x]).any())).dropna(how='all')
#### TODO: Some of the North American / Carribean countries may be considered part of latinamerica. South America was completely removed after seperation which is expected.
nonla_artist_origin = nonla_artist_origin.where(nonla_artist_origin['demonym'].apply(lambda x: not latins['demonym'].isin([x]).any())).dropna(how='all')
nonla_geographicStatistics = pd.merge(nonla_artist_origin, non_latines, on='demonym')
nonla_geographicStatistics = nonla_geographicStatistics.sort_values(by='Country Name')
nonla_geographicStatistics.reset_index(drop=True, inplace=True)
### Proportion of Countries per Continent
#Real vs Non-LA Dataset Distributions
remove_from_index = ['non-transformable']
total_by_continent.index = pd.Series(list(total_by_continent.index)).apply(lambda x: pc.convert_continent_code_to_continent_name(x) if x not in remove_from_index else x)
actual_proportion_of_countries = total_by_continent/ total_by_continent.sum()
total_by_continent = pd.DataFrame({'Countries':total_by_continent,'proportion_of_countries':actual_proportion_of_countries})
total_by_continent.name = 'Actual Distribution'
nonla_geographicStatistics['Continent'] = nonla_geographicStatistics['Continent'].replace('NA', 'NoA')
nonla_continentCounts = nonla_geographicStatistics.groupby('Continent Name').apply(lambda x: len(x))
# After using the demonym dataset to link the geographic naming Data
# with the pct_country_NGA data, some datapoints were lots. (sum of pct is now ~96%) and the # number of countries was reduced to ~ 52 (one duplicate)
nonla_continentCounts.name = 'Countrys_in_Continents'
#### Adding pct_continent_in_NGA to nonla_ContinentCounts using the pct_in_NGA column and Continent Name from nonla_geographicStatistics
pct_continent_NGA = nonla_geographicStatistics.groupby('Continent Name')['pct_country_NGA'].sum()
#### No artists in the NGA dataset were credited as having Antarctic/South American (after LatinAmerican data was removed) nationality & the non-transformable index was leftover from try-catching the PyCountry transformation of ISO codes, so they will be removed.
total_by_continent.drop('Antarctica', inplace=True)
total_by_continent.drop('non-transformable', inplace=True)
total_by_continent.drop('South America', inplace=True)
nonla_continentCounts = pd.DataFrame({'countries_present':nonla_continentCounts, 'proportion_of_continent': (nonla_continentCounts / total_by_continent['Countries'])})
#### The total by continent table shows world-wide share of countries and their proportion out of the total number of countries.
#### This nonla_continentCounts table shows countries and continents present in the NGA dataset and the proportion of countries present from the continent.
nonla_continentCounts['pct_continent_NGA'] = pct_continent_NGA
#### To find out how many continents are not included in the NGA dataset, I will subtract the total for ALL countries included in the PyCountry library, and subtract the countries visible within the dataset per continent. The different will be called nonla_continentCounts_missing.
nonla_continentCounts_missing = total_by_continent['Countries'] - nonla_continentCounts['countries_present']
nonla_continentCounts_missing.name = 'Missing_from_Actual_Distribution'
nonla_continentCounts_missing = pd.DataFrame({'countries_missing':nonla_continentCounts_missing, 'proportion_of_continent': (nonla_continentCounts_missing / total_by_continent['Countries'])})
nonla_continentCounts_missing = nonla_continentCounts_missing.reset_index(drop=False)
nonla_continentCounts_missing.columns = ['Continent Name', 'countries_missing', 'proportion_of_continent']
#### The number of columns before adding information about the specific geographical details of the artists' nationalities as well as additional statistical information about the countries and continents representation within the dataset
nonla_geographicStatistics = pd.merge(nonla_geographicStatistics, nonla_continentCounts_missing.loc[:, ['Continent Name','countries_missing']], how='inner', on='Continent Name')
nonla_continentCounts.reset_index(drop=False, inplace=True)
nonla_geographicStatistics = pd.merge(nonla_continentCounts, nonla_geographicStatistics, on='Continent Name')
#inner join of nonla_geographicStatistics and non_latinamerican_art
non_latinamerican_art = pd.merge(non_latinamerican_art, nonla_geographicStatistics, how='inner', left_on='nationality', right_on='demonym')
#### Feature Engineering IIIFUrl Links to view the data at the desired resolution
#converts the iiifurl to return the full image size
non_latinamerican_art['expanded_url'] = non_latinamerican_art.iiifthumburl.apply(lambda x: x.replace('!200,200', '!640,640'))
# After merging the main non_latinamerican_art dataset with the external geographical information that I created, I will write the updated dataset back to the original filepath and overwrite it as it contains valuable information
### Step 3 - Sampling from the large dataset for batch training
#Sampling from the full dataset (200073 rows), 500 rows for training  & 200 (for validation/testing == 700 total for one iteration of sample (1/100 of total dataset) // make sure not being selected with replacement to remove duplicates
matching_distribution = np.random.choice(non_latinamerican_art.index, p= non_latinamerican_art.pct_continent_NGA / non_latinamerican_art.pct_continent_NGA.sum(), size=700, replace=False)
index_matching = list(matching_distribution)
subsample_nonla = non_latinamerican_art.iloc[index_matching, :]
subsample_geography = subsample_nonla.groupby('Country Name').apply(lambda x: len(x))
subsample_geography = pd.DataFrame({'counts': subsample_geography,'proportion':subsample_geography / subsample_geography.sum()})
### Using the normalized probabilities in pct_continent_NGA to sample 10%, made the sample a little less representative to overall dataset. Since this is only a 10% sample, it is not fully representative, but I expect to train with more samples/batches.
subsample_geography.sort_values(by='proportion', ascending=False)
### Step 3 - Outputting the final combined NGA/FE data
non_latinamerican_art.to_csv('../../../data_samples/nonLaArt/modified_non_latinamerican_art.csv', index=False)
print('Saved the file modified_non_latinamerican_art.csv file to ../../../data_samples/nonLaArt')
subsample_nonla.reset_index(drop=True, inplace=True)
nonla_geographicStatistics.to_csv('../../../data_samples/nonLaArt/nonla_geographicStatistics.csv', index=False)
print('Saved the nonla_geographicStatistics.csv file to ../../../data_samples/nonLaArt/')
subsample_nonla.to_csv('../../../data_samples/results/processed_subset_results/non_latinamericanart_sample.csv', index=False)
print('Saved the non_latinamericanart_sample.csv file to ../../../data_samples/results/processed_subset_results/')
print('extract_nonLaArt.py finished.')