import numpy as np
import pandas as pd
from IPython.display import display, HTML
import re
import torch
import torch.nn.functional as fun
from sklearn.feature_extraction.text import CountVectorizer
import scipy.stats as stats
### Step 3: Cleaning the data for input into a M.L algorithm.
latinamerican_art = pd.read_csv('../data_samples/latinamerican_art.csv')

imagefp_exists = pd.read_csv('../data_samples/validLa_image_fpaths.csv')

stored_la_art = imagefp_exists.where(imagefp_exists.imagefp_exists == True).dropna(how='all')
stored_la_art.reset_index(drop = True, inplace=True)

valid_image_paths = stored_la_art.shape[0]
la_art_total = latinamerican_art.shape[0]
print('After step 2: downloading, the amount of latin american images downloaded and successfully stored is {} out of {} starting records. The '.format(valid_image_paths, la_art_total))

# Creating a new table of latinamerican art with valid fpaths
latinamerican_art_stored = pd.merge(left=latinamerican_art, right=stored_la_art, on = 'objectid', how = 'inner')

### Feature Engineering
### 1. text_classification notebook in TorchTextModel TBD
### 2. image_classification notebook tbd

## Word Vectors for Text/Categorical FE
text_dict = {}
for entry in latinamerican_art_stored.title:
    entry_words = entry.split(' ')
    for word in entry_words:
        word = word.strip(')([],\./')
        word = word.lower()
        if word in text_dict.keys():
            text_dict[word] += 1
        else:
            text_dict[word] = 1
title_occurrences = pd.Series(text_dict).sort_values(ascending=False)
titles = latinamerican_art_stored.title.copy()

# Prepares words for vectorization by converting titles to words
def clean_words(text):
    def strip(string):
        return re.sub('(?:^[{\W}]+)|(?:[{\W}]+$)', '', string)
    text_arr = text.split(' ')
    words = []
    for word in text_arr:
        edited = strip(word)
        words.append(edited.lower())
    return ' '.join(words)

#cleaning and formatting the data to give uniformity and clarity
titles = titles.apply(clean_words)

one_hot_vectorizer = CountVectorizer(binary=True)
one_hot = one_hot_vectorizer.fit_transform(titles)

title_oh = pd.DataFrame(one_hot.toarray().tolist(), columns=one_hot_vectorizer.get_feature_names_out())

one_hot = one_hot_vectorizer.fit_transform(latinamerican_art_stored.medium)
# Handling Duplicate Token Names in Columns (OH)
medium_cols = [x + ' (medium)' for x in one_hot_vectorizer.get_feature_names_out()]
medium_oh = pd.DataFrame(one_hot.toarray().tolist(), columns = medium_cols)

one_hot = one_hot_vectorizer.fit_transform(latinamerican_art_stored['artists_country'], )
# Handling Duplicate Token Names in Columns (OH)
country_cols = [x + ' (country)' for x in one_hot_vectorizer.get_feature_names_out()]
country_oh = pd.DataFrame(one_hot.toarray().tolist(), columns = country_cols)

one_hot = one_hot_vectorizer.fit_transform(latinamerican_art_stored['forwarddisplayname'])
# Handling Duplicate Token Names in Columns (OH)
name_cols = [x + ' (artist)' for x in one_hot_vectorizer.get_feature_names_out()]
artist_oh = pd.DataFrame(one_hot.toarray().tolist(), columns = name_cols)

oh_collection = pd.concat([title_oh, medium_oh, artist_oh, country_oh], axis=1)

## Numerical FE
percent_by_artist = latinamerican_art_stored.forwarddisplayname.value_counts(normalize='True')
artist_zscore = stats.zscore(percent_by_artist)
latinamerican_art_stored['artist_zscore'] = latinamerican_art_stored.forwarddisplayname.apply(lambda x: artist_zscore[x])
latinamerican_art_stored['percent_by_artist'] = latinamerican_art_stored.forwarddisplayname.apply(lambda x: percent_by_artist[x])
latinamerican_art_stored['log_percent_by_artist'] = latinamerican_art_stored['percent_by_artist'].apply(lambda x: np.log(x + 1))
latinamerican_art_stored['log_width'] = latinamerican_art_stored['width'].apply(lambda x: np.log(x + 1))
latinamerican_art_stored['log_height'] = latinamerican_art_stored['height'].apply(lambda x: np.log(x + 1))
numerical_cols = ['log_width', 'log_height', 'log_percent_by_artist']
numerical_data = latinamerican_art_stored.loc[:, numerical_cols]

### Saving Final Collection of Transformed Data
imagefp_features = ['imagefp_exists','objectid']
la_image_data = latinamerican_art_stored.loc[:, imagefp_features]
print('Merging the following: ')
print('imagefp data shape: ', la_image_data.shape)
print('one-hot data shape: ', oh_collection.shape)
print('numerical data shape: ', numerical_data.shape)
transformed_data = pd.concat([la_image_data, oh_collection, numerical_data], axis=1)
transformed_data.to_csv('../data_samples/results/transformed_la_art.csv', index=False)
print('CSV Created: ../data_samples/results/transformed_la_art.csv')
print('Final shape of transformed data (including imagefp_exists and objectid columns)', transformed_data.shape)