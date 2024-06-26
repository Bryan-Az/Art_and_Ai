#! /bin/bash
#run this from root (Art_and_Ai) folder
#the SQL scripts in 'insert_data' zip were created running MySQL>=8.0 DB
#the "la_art_tables" zip will be placed into the data_samples/LaArt directory to be used by the add_LaArt.sh script since it has CSV and is a data sample
#building the data directory the pytorch model will be using that uses the csv taken from the database (stored in art_tables.zip as of now)
cd scripts/sql_scripts
mv art_tables.zip ../../data_samples/
unzip ../../data_samples/art_tables.zip -d ../../data_samples/
# within this folder there is 2 tables (1 for LA art/1 for nonLA)
mv ../../data_samples/art_tables/latinamerican_art.csv ../../data_samples/LaArt
mv ../../data_samples/art_tables/non_latinamerican_art.csv ../../data_samples/nonLaArt
rm -r ../../data_samples/art_tables
#these are used in the db
#assumes zip package installed on ubuntu
unzip ./insert_data.zip -d ./
unzip ./query_tables.zip -d ./